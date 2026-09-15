package bi.fomi.stock.service;

import bi.fomi.stock.dto.MouvementResponse;
import bi.fomi.stock.dto.MouvementRequest;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.Distribution;
import bi.fomi.stock.model.entity.Lot;
import bi.fomi.stock.model.entity.Mouvement;
import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.model.entity.Utilisateur;
import bi.fomi.stock.model.enums.TypeMouvement;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.DistributionRepository;
import bi.fomi.stock.repository.LotRepository;
import bi.fomi.stock.repository.MouvementRepository;
import bi.fomi.stock.repository.StockLotRepository;
import bi.fomi.stock.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class MouvementService {

    private final DepotRepository depotRepository;
    private final LotRepository lotRepository;
    private final MouvementRepository mouvementRepository;
    private final StockLotRepository stockLotRepository;
    private final StockService stockService;
    private final AlerteService alerteService;
    private final AuditLogService auditLogService;
    private final DistributionRepository distributionRepository;
    private final TicketRepository ticketRepository;

    @Transactional
    public MouvementResponse reception(MouvementRequest req, Utilisateur agent) {
        if (req.idempotencyKey() != null && mouvementRepository.findByIdempotencyKey(req.idempotencyKey()).isPresent()) {
            throw new BusinessException("Mouvement déjà enregistré (idempotency)");
        }
        Depot dest = depot(req.depotDestId());
        Lot lot = lotRepository.findByIdForUpdate(req.lotId())
                .orElseThrow(() -> new ResourceNotFoundException("Lot introuvable : " + req.lotId()));
        if (req.quantite() + stockLotRepository.sumQuantiteByLot(lot.getId()) > lot.getQuantiteInitiale()) {
            throw new BusinessException("Quantité reçue supérieure au disponible du lot " + lot.getNumeroLot());
        }

        Mouvement mouvement = nouveau(TypeMouvement.RECEPTION_FOMI, lot, null, dest, req.quantite(), agent, null,
                req.commentaire(), req.idempotencyKey());
        mouvementRepository.save(mouvement);

        stockService.ajouter(dest, lot, req.quantite());
        alerteService.verifierDepot(dest, lot.getEngraisType());
        auditLogService.log("MOUVEMENT_RECEPTION", "Mouvement", mouvement.getId(),
                "{\"lot\":\"" + lot.getNumeroLot() + "\",\"depot\":\"" + dest.getCode() + "\",\"quantite\":"
                        + req.quantite() + "}");
        return toResponse(mouvement);
    }

    @Transactional
    public List<MouvementResponse> transfert(MouvementRequest req, Utilisateur agent) {
        Depot source = depot(req.depotSourceId());
        Depot dest = depot(req.depotDestId());
        if (source.getId().equals(dest.getId())) {
            throw new BusinessException("Le dépôt source et le dépôt destination doivent être différents");
        }
        Lot lot = lot(req.lotId());

        List<LotSortie> sorties = stockService.sortirFifo(source, lot.getEngraisType(), req.quantite(), lot.getId());
        List<MouvementResponse> reponses = new ArrayList<>();
        for (LotSortie sortie : sorties) {
            stockService.ajouter(dest, sortie.lot(), sortie.quantite());
            Mouvement mouvement = nouveau(TypeMouvement.TRANSFERT, sortie.lot(), source, dest, sortie.quantite(), agent,
                    null, req.commentaire(), null);
            mouvementRepository.save(mouvement);
            reponses.add(toResponse(mouvement));
        }
        alerteService.verifierDepot(source, lot.getEngraisType());
        alerteService.verifierDepot(dest, lot.getEngraisType());
        auditLogService.log("MOUVEMENT_TRANSFERT", "Mouvement", null,
                "{\"source\":\"" + source.getCode() + "\",\"dest\":\"" + dest.getCode() + "\",\"quantite\":"
                        + req.quantite() + "}");
        return reponses;
    }

    @Transactional
    public MouvementResponse annuler(Long mouvementId, String motif, Utilisateur agent) {
        Mouvement mouvement = mouvementRepository.findById(mouvementId)
                .orElseThrow(() -> new ResourceNotFoundException("Mouvement introuvable : " + mouvementId));
        if (Boolean.TRUE.equals(mouvement.getAnnule())) {
            throw new BusinessException("Ce mouvement est déjà annulé");
        }
        if (mouvement.getType() == TypeMouvement.RECEPTION_FOMI) {
            throw new BusinessException("Une réception FOMI ne peut pas être annulée (mouvement permanent)");
        }
        if (mouvement.getType() == TypeMouvement.AJUSTEMENT) {
            throw new BusinessException("Un ajustement ne peut pas être annulé");
        }

        if (mouvement.getType() == TypeMouvement.DISTRIBUTION) {
            if (mouvement.getDepotDest() != null) {
                stockService.sortirFifo(mouvement.getDepotDest(), mouvement.getEngraisType(),
                        mouvement.getQuantite(), mouvement.getLot().getId());
            }
            if (mouvement.getTicket() != null) {
                Ticket ticket = mouvement.getTicket();
                ticket.setQuantiteServie(ticket.getQuantiteServie() - mouvement.getQuantite());
                ticket.mettreAJourStatut();
                ticketRepository.save(ticket);
            }
            Distribution distribution = distributionRepository.findByLotId(mouvement.getLot().getId()).stream()
                    .filter(d -> d.getReferenceMouvement().getId().equals(mouvementId))
                    .findFirst()
                    .orElse(null);
            if (distribution != null) {
                distributionRepository.delete(distribution);
            }
        } else if (mouvement.getType() == TypeMouvement.TRANSFERT) {
            if (mouvement.getDepotSource() != null) {
                stockService.ajouter(mouvement.getDepotSource(), mouvement.getLot(), mouvement.getQuantite());
            }
            if (mouvement.getDepotDest() != null) {
                stockService.sortirFifo(mouvement.getDepotDest(), mouvement.getEngraisType(),
                        mouvement.getQuantite(), mouvement.getLot().getId());
            }
        }

        Mouvement ajustement = nouveau(TypeMouvement.AJUSTEMENT, mouvement.getLot(),
                mouvement.getDepotDest(), mouvement.getDepotSource(), mouvement.getQuantite(),
                agent, null, "Annulation mouvement #" + mouvementId
                        + (motif != null ? " - " + motif : ""), null);
        ajustement.setReferenceAnnulation(mouvement);
        mouvementRepository.save(ajustement);

        mouvement.setAnnule(true);
        mouvement.setMotifAnnulation(motif);
        mouvement.setAnnulePar(agent);
        mouvementRepository.save(mouvement);

        if (mouvement.getDepotSource() != null) {
            alerteService.verifierDepot(mouvement.getDepotSource(), mouvement.getEngraisType());
        }
        if (mouvement.getDepotDest() != null) {
            alerteService.verifierDepot(mouvement.getDepotDest(), mouvement.getEngraisType());
        }
        auditLogService.log("MOUVEMENT_ANNULATION", "Mouvement", mouvement.getId(),
                "{\"type\":\"" + mouvement.getType() + "\",\"motif\":\""
                        + (motif != null ? motif.replace("\"", "'") : "") + "\",\"ajustementId\":"
                        + ajustement.getId() + "}");
        return toResponse(mouvement);
    }

    private Mouvement nouveau(TypeMouvement type, Lot lot, Depot source, Depot dest, int quantite, Utilisateur agent,
                              bi.fomi.stock.model.entity.Ticket ticket, String commentaire, String idempotencyKey) {
        return Mouvement.builder()
                .type(type)
                .lot(lot)
                .engraisType(lot.getEngraisType())
                .depotSource(source)
                .depotDest(dest)
                .quantite(quantite)
                .agent(agent)
                .ticket(ticket)
                .commentaire(commentaire)
                .idempotencyKey(idempotencyKey)
                .dateMouvement(LocalDateTime.now())
                .build();
    }

    private Depot depot(Long id) {
        return depotRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + id));
    }

    private Lot lot(Long id) {
        return lotRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Lot introuvable : " + id));
    }

    private MouvementResponse toResponse(Mouvement m) {
        return new MouvementResponse(m.getId(), m.getType(), m.getLot().getNumeroLot(),
                m.getEngraisType().getCode(),
                m.getDepotSource() != null ? m.getDepotSource().getCode() : null,
                m.getDepotDest() != null ? m.getDepotDest().getCode() : null,
                m.getQuantite(), m.getAgent().getUsername(),
                m.getTicket() != null ? m.getTicket().getNumeroTicket() : null,
                m.getCommentaire(), m.getDateMouvement());
    }
}
