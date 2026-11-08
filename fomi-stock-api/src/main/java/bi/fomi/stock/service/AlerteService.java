package bi.fomi.stock.service;

import bi.fomi.stock.model.entity.Alerte;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.EngraisType;
import bi.fomi.stock.model.entity.SeuilAlerte;
import bi.fomi.stock.model.entity.Stock;
import bi.fomi.stock.model.entity.StockLot;
import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.model.enums.NiveauAlerte;
import bi.fomi.stock.model.enums.StatutTicket;
import bi.fomi.stock.model.enums.TypeAlerte;
import bi.fomi.stock.repository.AlerteRepository;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.MouvementRepository;
import bi.fomi.stock.repository.SeuilAlerteRepository;
import bi.fomi.stock.repository.StockLotRepository;
import bi.fomi.stock.repository.StockRepository;
import bi.fomi.stock.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class AlerteService {

    private static final int DELAI_JOURS = 30;

    private final AlerteRepository alerteRepository;
    private final StockRepository stockRepository;
    private final TicketRepository ticketRepository;
    private final SeuilAlerteRepository seuilAlerteRepository;
    private final StockLotRepository stockLotRepository;
    private final MouvementRepository mouvementRepository;
    private final DepotRepository depotRepository;

    @Transactional
    public void verifierDepot(Depot depot, EngraisType engraisType) {
        int stock = stockRepository.findByDepotIdAndEngraisTypeId(depot.getId(), engraisType.getId())
                .map(Stock::getQuantiteDisponible)
                .orElse(0);

        SeuilAlerte seuil = seuilAlerteRepository.findByDepotIdAndEngraisTypeId(depot.getId(), engraisType.getId())
                .orElse(null);
        int seuilMin = seuil != null ? seuil.getSeuilMin() : depot.getSeuilAlerteMin();
        NiveauAlerte niveauStockBas = seuil != null && "CRITICAL".equals(seuil.getCriticite())
                ? NiveauAlerte.CRITICAL : NiveauAlerte.WARNING;

        if (stock == 0) {
            creerSiAbsente(depot, engraisType, TypeAlerte.RUPTURE, NiveauAlerte.CRITICAL,
                    "Stock " + engraisType.getNom() + " épuisé au dépôt " + depot.getNom());
        } else if (stock < seuilMin) {
            creerSiAbsente(depot, engraisType, TypeAlerte.STOCK_BAS, niveauStockBas,
                    "Stock " + engraisType.getNom() + " (" + stock + " sacs) sous le seuil de " + seuilMin
                            + " au dépôt " + depot.getNom());
        }

        List<StockLot> stockLots = stockLotRepository
                .findByDepotIdAndLotEngraisTypeIdOrderByLotDateReceptionFomiAsc(depot.getId(), engraisType.getId());
        for (StockLot sl : stockLots) {
            if (sl.getLot().getDatePeremption() != null
                    && sl.getLot().getDatePeremption().isBefore(LocalDate.now())) {
                creerSiAbsente(depot, engraisType, TypeAlerte.PEREMPTION, NiveauAlerte.CRITICAL,
                        "Lot " + sl.getLot().getNumeroLot() + " (" + engraisType.getNom()
                                + ") périmé le " + sl.getLot().getDatePeremption()
                                + " au dépôt " + depot.getNom());
            }
        }

        long demande = ticketRepository
                .findNonServisByDepot(depot.getId(), List.of(StatutTicket.PAYE, StatutTicket.EN_ATTENTE,
                        StatutTicket.PARTIEL, StatutTicket.ACTIF, StatutTicket.EN_ATTENTE_DE_VALIDATION,
                        StatutTicket.ARRIERE))
                .stream()
                .filter(t -> t.getEngraisType().getId().equals(engraisType.getId()))
                .mapToLong(t -> t.getQuantiteCommandee() - t.getQuantiteServie())
                .sum();
        if (demande > stock) {
            creerSiAbsente(depot, engraisType, TypeAlerte.DEMANDE_SUP_STOCK, NiveauAlerte.WARNING,
                    "Demande non servie (" + demande + " sacs) dépasse le stock disponible (" + stock + " sacs) au dépôt "
                            + depot.getNom());
        }
    }

    @Transactional
    public void verifierDelaisDepasse() {
        List<Ticket> enRetard = ticketRepository.findAll().stream()
                .filter(t -> t.getQuantiteServie() < t.getQuantiteCommandee())
                .filter(t -> switch (t.getStatut()) {
                    case ANNULE, REJETE, EXPIRE, ARRIERE -> false;
                    default -> true;
                })
                .filter(t -> ChronoUnit.DAYS.between(t.getDatePaiement(), LocalDate.now()) > DELAI_JOURS)
                .toList();

        Map<Long, List<Ticket>> parDepot = enRetard.stream()
                .collect(Collectors.groupingBy(t -> t.getDepotRetrait().getId()));

        parDepot.forEach((depotId, tickets) -> {
            Depot depot = tickets.get(0).getDepotRetrait();
            EngraisType type = tickets.get(0).getEngraisType();
            long nonServis = tickets.stream().mapToLong(t -> t.getQuantiteCommandee() - t.getQuantiteServie()).sum();
            creerSiAbsente(depot, type, TypeAlerte.DELAI_DEPASSE, NiveauAlerte.WARNING,
                    nonServis + " sacs non servis pour " + tickets.size() + " tickets en retard (délai > " + DELAI_JOURS
                            + " jours) au dépôt " + depot.getNom());
        });
        log.info("Vérification des délais dépassés terminée : {} tickets en retard", enRetard.size());
    }

    @Scheduled(cron = "0 0 6 * * *")
    public void scheduledDelais() {
        verifierDelaisDepasse();
    }

    @Transactional
    public void verifierInactivite() {
        LocalDateTime ilYADixSeptJours = LocalDateTime.now().minusDays(7);
        Set<Long> depotsAvecMouvement = mouvementRepository.findAll().stream()
                .filter(m -> m.getDateMouvement().isAfter(ilYADixSeptJours))
                .filter(m -> !Boolean.TRUE.equals(m.getAnnule()))
                .flatMap(m -> {
                    java.util.stream.Stream.Builder<Long> ids = java.util.stream.Stream.builder();
                    if (m.getDepotSource() != null) ids.add(m.getDepotSource().getId());
                    if (m.getDepotDest() != null) ids.add(m.getDepotDest().getId());
                    return ids.build();
                })
                .collect(Collectors.toSet());

        depotRepository.findAll().stream()
                .filter(d -> Boolean.TRUE.equals(d.getActif()))
                .filter(d -> !depotsAvecMouvement.contains(d.getId()))
                .forEach(depot -> {
                    List<Stock> stocks = stockRepository.findByDepotIdOrderByEngraisTypeCode(depot.getId());
                    if (stocks.isEmpty()) {
                        creerSiAbsente(depot, null, TypeAlerte.INACTIVITE, NiveauAlerte.WARNING,
                                "Aucun mouvement au dépôt " + depot.getNom() + " depuis 7 jours");
                    } else {
                        for (Stock s : stocks) {
                            creerSiAbsente(depot, s.getEngraisType(), TypeAlerte.INACTIVITE, NiveauAlerte.WARNING,
                                    "Aucun mouvement de " + s.getEngraisType().getNom()
                                            + " au dépôt " + depot.getNom() + " depuis 7 jours");
                        }
                    }
                });
        log.info("Vérification de l'inactivité terminée");
    }

    @Scheduled(cron = "0 30 6 * * *")
    public void scheduledInactivite() {
        verifierInactivite();
    }

    private void creerSiAbsente(Depot depot, EngraisType engraisType, TypeAlerte type, NiveauAlerte niveau,
                                String message) {
        Long depotId = depot.getId();
        Long engraisTypeId = engraisType != null ? engraisType.getId() : null;
        boolean existe = engraisTypeId != null
                && !alerteRepository
                        .findByDepotIdAndEngraisTypeIdAndTypeAndTraiteeFalse(depotId, engraisTypeId, type)
                        .isEmpty();
        if (!existe) {
            alerteRepository.save(Alerte.builder()
                    .depot(depot)
                    .engraisType(engraisType)
                    .type(type)
                    .niveau(niveau)
                    .message(message)
                    .traitee(false)
                    .build());
        }
    }
}
