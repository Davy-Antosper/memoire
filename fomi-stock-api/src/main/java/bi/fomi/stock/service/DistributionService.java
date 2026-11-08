package bi.fomi.stock.service;

import bi.fomi.stock.dto.DistributionResponse;
import bi.fomi.stock.dto.DistributionRequest;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.Distribution;
import bi.fomi.stock.model.entity.Mouvement;
import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.model.entity.Utilisateur;
import bi.fomi.stock.model.enums.RoleUtilisateur;
import bi.fomi.stock.model.enums.StatutTicket;
import bi.fomi.stock.model.enums.TypeMouvement;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.DistributionRepository;
import bi.fomi.stock.repository.MouvementRepository;
import bi.fomi.stock.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class DistributionService {

    private final TicketRepository ticketRepository;
    private final DepotRepository depotRepository;
    private final MouvementRepository mouvementRepository;
    private final DistributionRepository distributionRepository;
    private final StockService stockService;
    private final AlerteService alerteService;
    private final AuditLogService auditLogService;
    private final EmailNotificationService emailNotificationService;

    @Transactional
    public List<DistributionResponse> distribuer(DistributionRequest req, Utilisateur agent) {
        Ticket ticket = ticketRepository.findByIdForUpdate(req.ticketId())
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + req.ticketId()));
        Depot depot = depotRepository.findById(req.depotId())
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + req.depotId()));

        verifierPerimetreAgent(agent, depot);

        if (!List.of(StatutTicket.ACTIF, StatutTicket.PAYE, StatutTicket.EN_ATTENTE, StatutTicket.PARTIEL)
                .contains(ticket.getStatut())) {
            throw new BusinessException("Distribution impossible : statut du ticket = " + ticket.getStatut());
        }
        int restant = ticket.getQuantiteCommandee() - ticket.getQuantiteServie();
        if (restant < req.quantite()) {
            throw new BusinessException("Quantité demandée (" + req.quantite() + ") supérieure au restant du ticket ("
                    + restant + ")");
        }

        List<LotSortie> sorties = stockService.sortirFifo(depot, ticket.getEngraisType(), req.quantite(), req.lotId());

        List<DistributionResponse> reponses = new ArrayList<>();
        for (LotSortie sortie : sorties) {
            Mouvement mouvement = Mouvement.builder()
                    .type(TypeMouvement.DISTRIBUTION)
                    .lot(sortie.lot())
                    .engraisType(ticket.getEngraisType())
                    .depotSource(depot)
                    .depotDest(null)
                    .quantite(sortie.quantite())
                    .agent(agent)
                    .ticket(ticket)
                    .commentaire(req.commentaire())
                    .dateMouvement(LocalDateTime.now())
                    .build();
            mouvementRepository.save(mouvement);

            Distribution distribution = distributionRepository.save(Distribution.builder()
                    .ticket(ticket)
                    .lot(sortie.lot())
                    .depot(depot)
                    .quantite(sortie.quantite())
                    .agent(agent)
                    .dateDistribution(LocalDateTime.now())
                    .referenceMouvement(mouvement)
                    .build());

            reponses.add(new DistributionResponse(distribution.getId(), ticket.getNumeroTicket(),
                    sortie.lot().getNumeroLot(), depot.getCode(), sortie.quantite(), agent.getUsername(),
                    distribution.getDateDistribution()));
        }

        ticket.setQuantiteServie(ticket.getQuantiteServie() + req.quantite());
        ticket.mettreAJourStatut();
        ticketRepository.save(ticket);

        alerteService.verifierDepot(depot, ticket.getEngraisType());
        auditLogService.log("DISTRIBUTION_CREATE", "Ticket", ticket.getId(),
                "{\"depot\":\"" + depot.getCode() + "\",\"quantite\":" + req.quantite() + ",\"reste\":"
                        + ticket.getQuantiteRestante() + "}");
        String precision = "Distribution de " + req.quantite() + " kg effectuée au dépôt "
                + depot.getCode() + ". "
                + (ticket.getStatut() == StatutTicket.SERVI
                        ? "Votre ticket est entièrement servi."
                        : "Il vous reste " + ticket.getQuantiteRestante() + " kg à retirer.");
        emailNotificationService.notifierTicket(ticket, "DISTRIBUTION", precision);
        return reponses;
    }

    private void verifierPerimetreAgent(Utilisateur agent, Depot depot) {
        if (agent.getRole() == RoleUtilisateur.AGENT_COLLINE) {
            if (agent.getDepot() == null || !agent.getDepot().getId().equals(depot.getId())) {
                throw new BusinessException("Un agent colline ne peut distribuer que sur son propre dépôt ("
                        + agent.getNomComplet() + ")");
            }
        }
        if (agent.getRole() == RoleUtilisateur.AGENT_ZONE) {
            if (agent.getZone() == null || !dansZone(depot, agent.getZone().getId())) {
                throw new BusinessException("Un agent zone ne peut distribuer que dans sa zone ("
                        + agent.getNomComplet() + ")");
            }
        }
    }

    private boolean dansZone(Depot depot, Long zoneId) {
        return depot.getZone() != null && zoneId.equals(depot.getZone().getId());
    }
}
