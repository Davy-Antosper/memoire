package bi.fomi.stock.service;

import bi.fomi.stock.dto.PublicTicketResponse;
import bi.fomi.stock.dto.TicketRequest;
import bi.fomi.stock.dto.TicketResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Agriculteur;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.EngraisType;
import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.model.enums.StatutTicket;
import bi.fomi.stock.repository.AgriculteurRepository;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.EngraisTypeRepository;
import bi.fomi.stock.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class TicketService {

    private static final BigDecimal KG_PAR_HECTARE = new BigDecimal("150");

    private final TicketRepository ticketRepository;
    private final AgriculteurRepository agriculteurRepository;
    private final DepotRepository depotRepository;
    private final EngraisTypeRepository engraisTypeRepository;
    private final AuditLogService auditLogService;
    private final EmailNotificationService emailNotificationService;

    @Transactional
    public TicketResponse creer(TicketRequest req) {
        if (ticketRepository.findByNumeroTicket(req.numeroTicket()).isPresent()) {
            throw new BusinessException("Numéro de ticket déjà utilisé : " + req.numeroTicket());
        }
        Agriculteur agriculteur = agriculteurRepository.findById(req.agriculteurId())
                .orElseThrow(() -> new ResourceNotFoundException("Agriculteur introuvable"));
        EngraisType engraisType = engraisTypeRepository.findById(req.engraisTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable"));
        Depot depot = depotRepository.findById(req.depotRetraitId())
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt de retrait introuvable"));

        // R22 : vérification des quotas par superficie (superficie × 150 kg/ha)
        BigDecimal superficie = req.superficieHa() != null ? req.superficieHa()
                : (agriculteur.getSuperficieHa() != null ? agriculteur.getSuperficieHa() : null);
        if (superficie != null && superficie.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal plafond = superficie.multiply(KG_PAR_HECTARE).setScale(0, RoundingMode.DOWN);
            if (req.quantiteCommandee().compareTo(plafond.intValue()) > 0) {
                throw new BusinessException("La quantité commandée (" + req.quantiteCommandee()
                        + " kg) dépasse le plafond autorisé pour cet agriculteur (" + plafond + " kg). "
                        + "Plafond calculé : superficie × 150 kg/ha");
            }
            // Vérifier le cumul des tickets actifs pour la même saison
            List<Ticket> existants = ticketRepository.findByAgriculteurId(req.agriculteurId()).stream()
                    .filter(t -> t.getSaison() != null && t.getSaison().equals(req.saison()))
                    .filter(t -> List.of(StatutTicket.EN_ATTENTE_DE_VALIDATION, StatutTicket.ACTIF,
                            StatutTicket.PAYE, StatutTicket.PARTIEL, StatutTicket.EN_ATTENTE)
                            .contains(t.getStatut()))
                    .toList();
            int cumul = existants.stream().mapToInt(Ticket::getQuantiteCommandee).sum();
            if (cumul + req.quantiteCommandee() > plafond.intValue()) {
                throw new BusinessException("Le cumul des tickets pour la saison " + req.saison()
                        + " (" + (cumul + req.quantiteCommandee()) + " kg) dépasse le plafond autorisé ("
                        + plafond + " kg). Déjà commandé : " + cumul + " kg");
            }
            // R6 : vérifier qu'il n'y a pas déjà un ticket pour même saison + même type engrais
            boolean doublon = existants.stream().anyMatch(t ->
                    t.getEngraisType().getId().equals(engraisType.getId()));
            if (doublon) {
                throw new BusinessException("Un ticket existe déjà pour cet agriculteur pour cette saison"
                        + " et ce type d'engrais");
            }
        }

        Ticket ticket = Ticket.builder()
                .numeroTicket(req.numeroTicket())
                .agriculteur(agriculteur)
                .engraisType(engraisType)
                .quantiteCommandee(req.quantiteCommandee())
                .quantiteServie(0)
                .montantPaye(req.montantPaye())
                .datePaiement(req.datePaiement())
                .depotRetrait(depot)
                .statut(StatutTicket.EN_ATTENTE_DE_VALIDATION)
                .saison(req.saison())
                .superficieHa(superficie)
                .build();

        ticket = ticketRepository.save(ticket);
        auditLogService.log("TICKET_CREATE", "Ticket", ticket.getId(),
                "{\"numero\":\"" + ticket.getNumeroTicket() + "\",\"agriculteur\":\""
                        + agriculteur.getNumeroIdentite() + "\",\"quantite\":" + req.quantiteCommandee()
                        + ",\"saison\":\"" + req.saison() + "\"}");
        emailNotificationService.notifierTicket(ticket, "TICKET_CREE", null);
        return toResponse(ticket);
    }

    @Transactional
    public TicketResponse modifier(Long id, TicketRequest req) {
        Ticket ticket = ticketRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + id));
        if (ticket.getSupprime() != null && ticket.getSupprime()) {
            throw new BusinessException("Ticket supprimé : édition impossible");
        }
        if (ticket.getQuantiteServie() > 0) {
            throw new BusinessException("Ticket déjà servi : édition impossible");
        }
        if (ticket.getStatut() == StatutTicket.ANNULE) {
            throw new BusinessException("Ticket annulé : édition impossible");
        }
        EngraisType engraisType = engraisTypeRepository.findById(req.engraisTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable"));
        Depot depot = depotRepository.findById(req.depotRetraitId())
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt de retrait introuvable"));

        ticket.setQuantiteCommandee(req.quantiteCommandee());
        ticket.setMontantPaye(req.montantPaye());
        ticket.setDatePaiement(req.datePaiement());
        ticket.setEngraisType(engraisType);
        ticket.setDepotRetrait(depot);
        ticket.setSaison(req.saison());
        ticket.setSuperficieHa(req.superficieHa());
        ticket.setStatut(StatutTicket.EN_ATTENTE_DE_VALIDATION);

        auditLogService.log("TICKET_UPDATE", "Ticket", ticket.getId(),
                "{\"numero\":\"" + ticket.getNumeroTicket() + "\",\"quantite\":" + req.quantiteCommandee()
                        + ",\"statut\":\"" + StatutTicket.EN_ATTENTE_DE_VALIDATION + "\"}");
        return toResponse(ticketRepository.save(ticket));
    }

    @Transactional
    public TicketResponse activer(Long id) {
        Ticket ticket = ticketRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + id));
        if (ticket.getStatut() != StatutTicket.EN_ATTENTE_DE_VALIDATION) {
            throw new BusinessException("Seul un ticket en attente de validation peut être activé (statut actuel : "
                    + ticket.getStatut() + ")");
        }
        ticket.setStatut(StatutTicket.ACTIF);
        auditLogService.log("TICKET_ACTIVATE", "Ticket", ticket.getId(),
                "{\"numero\":\"" + ticket.getNumeroTicket() + "\",\"statut\":\"" + StatutTicket.ACTIF + "\"}");
        ticket = ticketRepository.save(ticket);
        emailNotificationService.notifierTicket(ticket, "TICKET_VALIDE",
                "Votre ticket est désormais actif : vous pouvez retirer votre engrais au dépôt indiqué.");
        return toResponse(ticket);
    }

    @Transactional
    public TicketResponse rejeter(Long id, String motif) {
        Ticket ticket = ticketRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + id));
        if (ticket.getStatut() != StatutTicket.EN_ATTENTE_DE_VALIDATION) {
            throw new BusinessException("Seul un ticket en attente de validation peut être rejeté (statut actuel : "
                    + ticket.getStatut() + ")");
        }
        ticket.setStatut(StatutTicket.REJETE);
        String details = "{\"numero\":\"" + ticket.getNumeroTicket() + "\",\"statut\":\"" + StatutTicket.REJETE + "\""
                + (motif != null && !motif.isBlank() ? ",\"motif\":\"" + motif.replace("\"", "'") + "\"" : "") + "}";
        auditLogService.log("TICKET_REJECT", "Ticket", ticket.getId(), details);
        ticket = ticketRepository.save(ticket);
        emailNotificationService.notifierTicket(ticket, "TICKET_REJETE",
                (motif != null && !motif.isBlank() ? "Motif du rejet : " + motif : null));
        return toResponse(ticket);
    }

    @Transactional
    public int expirerTickets(String saison) {
        List<Ticket> tickets = ticketRepository.findBySaisonAndStatutNotIn(saison,
                List.of(StatutTicket.ANNULE, StatutTicket.REJETE, StatutTicket.EXPIRE, StatutTicket.SERVI));
        int expires = 0;
        for (Ticket ticket : tickets) {
            if (ticket.getQuantiteServie() < ticket.getQuantiteCommandee()) {
                ticket.setStatut(StatutTicket.EXPIRE);
                auditLogService.log("TICKET_EXPIRE", "Ticket", ticket.getId(),
                        "{\"numero\":\"" + ticket.getNumeroTicket() + "\",\"saison\":\"" + saison + "\"}");
                emailNotificationService.notifierTicket(ticket, "TICKET_EXPIRE",
                        "La saison " + saison + " est clôturée : votre ticket n'a pas été entièrement servi.");
                expires++;
            }
        }
        return expires;
    }

    @Transactional(readOnly = true)
    public TicketResponse getByNumero(String numero) {
        return ticketRepository.findByNumeroTicket(numero)
                .map(this::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + numero));
    }

    @Transactional(readOnly = true)
    public PublicTicketResponse getPublicByNumero(String numero) {
        return ticketRepository.findByNumeroTicket(numero)
                .map(t -> new PublicTicketResponse(t.getNumeroTicket(),
                        t.getAgriculteur().getNom() + " " + t.getAgriculteur().getPrenom(),
                        t.getEngraisType().getCode(), t.getEngraisType().getNom(),
                        t.getQuantiteCommandee(), t.getQuantiteServie(), t.getQuantiteRestante(),
                        t.getStatut(), t.getDatePaiement(), t.getDepotRetrait().getCode(),
                        t.getSaison(), t.getDateCreation()))
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + numero));
    }

    @Transactional(readOnly = true)
    public TicketResponse getById(Long id) {
        return ticketRepository.findById(id)
                .map(this::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket introuvable : " + id));
    }

    @Transactional(readOnly = true)
    public Page<TicketResponse> lister(Long depotId, StatutTicket statut, String saison, Pageable pageable) {
        String saisonFiltre = (saison == null || saison.isBlank()) ? null : saison.trim();
        Page<Ticket> tickets;
        if (depotId != null && statut != null && saisonFiltre != null) {
            tickets = ticketRepository.findByDepotRetraitIdAndStatutAndSaison(depotId, statut, saisonFiltre, pageable);
        } else if (depotId != null && saisonFiltre != null) {
            tickets = ticketRepository.findByDepotRetraitIdAndSaison(depotId, saisonFiltre, pageable);
        } else if (depotId != null && statut != null) {
            tickets = ticketRepository.findByDepotRetraitIdAndStatut(depotId, statut, pageable);
        } else if (depotId != null) {
            tickets = ticketRepository.findByDepotRetraitId(depotId, pageable);
        } else if (statut != null && saisonFiltre != null) {
            tickets = ticketRepository.findByStatutAndSaison(statut, saisonFiltre, pageable);
        } else if (statut != null) {
            tickets = ticketRepository.findByStatut(statut, pageable);
        } else if (saisonFiltre != null) {
            tickets = ticketRepository.findBySaison(saisonFiltre, pageable);
        } else {
            tickets = ticketRepository.findAll(pageable);
        }
        return tickets.map(this::toResponse);
    }

    private TicketResponse toResponse(Ticket t) {
        return new TicketResponse(t.getId(), t.getNumeroTicket(), t.getAgriculteur().getId(),
                t.getAgriculteur().getNom() + " " + t.getAgriculteur().getPrenom(),
                t.getEngraisType().getCode(), t.getQuantiteCommandee(), t.getQuantiteServie(),
                t.getQuantiteRestante(), t.getMontantPaye(), t.getDatePaiement(),
                t.getDepotRetrait().getCode(), t.getStatut(), t.getSaison(),
                t.getSuperficieHa(), t.getDateCreation());
    }
}
