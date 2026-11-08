package bi.fomi.stock.service;

import bi.fomi.stock.dto.ReclamationRequest;
import bi.fomi.stock.dto.ReclamationResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Reclamation;
import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.repository.ReclamationRepository;
import bi.fomi.stock.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Set;

@Service
@RequiredArgsConstructor
public class ReclamationService {

    private static final Set<String> STATUTS_ACTIFS = Set.of("OUVERTE", "EN_INSTRUCTION");
    private static final Set<String> STATUTS_VALIDES = Set.of("OUVERTE", "EN_INSTRUCTION", "RESOLUE", "REJETEE");

    private final ReclamationRepository reclamationRepository;
    private final TicketRepository ticketRepository;
    private final AuditLogService auditLogService;

    @Transactional
    public ReclamationResponse creer(ReclamationRequest req) {
        Ticket ticket = ticketRepository.findById(req.ticketId())
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + req.ticketId()));
        if (Boolean.TRUE.equals(ticket.getSupprime())) {
            throw new BusinessException("Impossible de réclamer sur un ticket supprimé");
        }
        if (reclamationRepository.existsByTicketIdAndStatutIn(ticket.getId(), List.copyOf(STATUTS_ACTIFS))) {
            throw new BusinessException("Une réclamation est déjà ouverte pour ce ticket");
        }
        int restante = ticket.getQuantiteRestante();
        int manquante = req.quantiteManquante() != null ? req.quantiteManquante() : restante;
        if (manquante > restante) {
            throw new BusinessException("La quantité manquante (" + manquante
                    + " sacs) dépasse le reste à servir du ticket (" + restante + " sacs)");
        }
        Reclamation reclamation = Reclamation.builder()
                .ticket(ticket)
                .motif(req.motif().trim())
                .description(req.description())
                .quantiteManquante(manquante)
                .statut("OUVERTE")
                .estDemo(Boolean.TRUE.equals(ticket.getEstDemo()))
                .build();
        Reclamation saved = reclamationRepository.save(reclamation);
        auditLogService.log("RECLAMATION_CREATE", "Reclamation", saved.getId(),
                "{\"ticket\":\"" + ticket.getNumeroTicket() + "\",\"motif\":\""
                        + saved.getMotif().replace("\"", "'") + "\",\"manquante\":" + manquante + "}");
        return toResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<ReclamationResponse> lister(String statut) {
        List<Reclamation> list = (statut == null || statut.isBlank())
                ? reclamationRepository.findAllByOrderByDateCreationDesc()
                : reclamationRepository.findByStatutOrderByDateCreationDesc(statut.trim().toUpperCase());
        return list.stream().map(this::toResponse).toList();
    }

    @Transactional
    public ReclamationResponse changerStatut(Long id, String statut, String resolution) {
        if (statut == null || !STATUTS_VALIDES.contains(statut.trim().toUpperCase())) {
            throw new BusinessException("Statut de réclamation invalide. Valeurs autorisées : OUVERTE, "
                    + "EN_INSTRUCTION, RESOLUE, REJETEE");
        }
        String nouveau = statut.trim().toUpperCase();
        boolean cloture = "RESOLUE".equals(nouveau) || "REJETEE".equals(nouveau);
        if (cloture && (resolution == null || resolution.isBlank())) {
            throw new BusinessException("La résolution (ou le motif de rejet) est obligatoire pour clôturer une réclamation");
        }
        Reclamation reclamation = reclamationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Réclamation introuvable : " + id));
        reclamation.setStatut(nouveau);
        if (resolution != null && !resolution.isBlank()) {
            reclamation.setResolution(resolution.trim());
        }
        if (cloture) {
            reclamation.setDateResolution(LocalDateTime.now());
        }
        Reclamation saved = reclamationRepository.save(reclamation);
        auditLogService.log("RECLAMATION_" + nouveau, "Reclamation", id,
                "{\"ticket\":\"" + saved.getTicket().getNumeroTicket() + "\",\"statut\":\"" + nouveau + "\"}");
        return toResponse(saved);
    }

    private ReclamationResponse toResponse(Reclamation r) {
        Ticket t = r.getTicket();
        return new ReclamationResponse(r.getId(), t.getId(), t.getNumeroTicket(),
                t.getAgriculteur().getNom() + " " + t.getAgriculteur().getPrenom(),
                r.getMotif(), r.getDescription(), r.getQuantiteManquante(), r.getStatut(),
                r.getResolution(), r.getDateCreation(), r.getDateResolution(), r.getEstDemo());
    }
}
