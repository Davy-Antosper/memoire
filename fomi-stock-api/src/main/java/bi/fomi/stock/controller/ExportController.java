package bi.fomi.stock.controller;

import bi.fomi.stock.model.entity.Mouvement;
import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.model.enums.StatutTicket;
import bi.fomi.stock.repository.MouvementRepository;
import bi.fomi.stock.repository.TicketRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.nio.charset.StandardCharsets;
import java.util.List;

@RestController
@RequestMapping("/api/export")
@RequiredArgsConstructor
public class ExportController {

    private static final String SEPARATOR = ";";
    private static final String LINE_BREAK = "\r\n";

    private final TicketRepository ticketRepository;
    private final MouvementRepository mouvementRepository;

    @GetMapping(value = "/tickets.csv", produces = "text/csv;charset=UTF-8")
    @Transactional(readOnly = true)
    public byte[] exportTickets(@RequestParam(required = false) Long depotId,
                                @RequestParam(required = false) StatutTicket statut) {
        List<Ticket> tickets;
        if (depotId != null && statut != null) {
            tickets = ticketRepository.findByDepotRetraitIdAndStatut(depotId, statut, PageRequest.of(0, 100000))
                    .getContent();
        } else if (depotId != null) {
            tickets = ticketRepository.findByDepotRetraitId(depotId, PageRequest.of(0, 100000)).getContent();
        } else if (statut != null) {
            tickets = ticketRepository.findByStatut(statut, PageRequest.of(0, 100000)).getContent();
        } else {
            tickets = ticketRepository.findAll(PageRequest.of(0, 100000)).getContent();
        }

        StringBuilder sb = new StringBuilder();
        sb.append("Numéro").append(SEPARATOR).append("Agriculteur").append(SEPARATOR).append("Engrais")
                .append(SEPARATOR).append("Commandé").append(SEPARATOR).append("Servi").append(SEPARATOR)
                .append("Restant").append(SEPARATOR).append("Montant payé").append(SEPARATOR).append("Date paiement")
                .append(SEPARATOR).append("Dépôt retrait").append(SEPARATOR).append("Statut").append(SEPARATOR)
                .append("Date création").append(LINE_BREAK);
        for (Ticket t : tickets) {
            sb.append(escape(t.getNumeroTicket())).append(SEPARATOR)
                    .append(t.getAgriculteur() != null
                            ? escape(t.getAgriculteur().getNom() + " " + t.getAgriculteur().getPrenom()) : "").append(SEPARATOR)
                    .append(t.getEngraisType() != null ? escape(t.getEngraisType().getCode()) : "").append(SEPARATOR)
                    .append(t.getQuantiteCommandee() != null ? t.getQuantiteCommandee() : "").append(SEPARATOR)
                    .append(t.getQuantiteServie() != null ? t.getQuantiteServie() : "").append(SEPARATOR)
                    .append(t.getQuantiteRestante()).append(SEPARATOR)
                    .append(t.getMontantPaye() != null ? t.getMontantPaye().toPlainString() : "").append(SEPARATOR)
                    .append(t.getDatePaiement()).append(SEPARATOR)
                    .append(t.getDepotRetrait() != null ? escape(t.getDepotRetrait().getCode()) : "").append(SEPARATOR)
                    .append(t.getStatut()).append(SEPARATOR)
                    .append(t.getDateCreation()).append(LINE_BREAK);
        }
        return sb.toString().getBytes(StandardCharsets.UTF_8);
    }

    @GetMapping(value = "/mouvements.csv", produces = "text/csv;charset=UTF-8")
    @Transactional(readOnly = true)
    public byte[] exportMouvements(@RequestParam(required = false) Long depotId) {
        List<Mouvement> mouvements = depotId != null
                ? mouvementRepository.findByDepotSourceIdOrDepotDestIdOrderByDateMouvementAsc(depotId, depotId)
                : mouvementRepository.findAll();

        StringBuilder sb = new StringBuilder();
        sb.append("Type").append(SEPARATOR).append("Lot").append(SEPARATOR).append("Engrais").append(SEPARATOR)
                .append("Source").append(SEPARATOR).append("Destination").append(SEPARATOR).append("Quantité")
                .append(SEPARATOR).append("Agent").append(SEPARATOR).append("Ticket").append(SEPARATOR)
                .append("Commentaire").append(SEPARATOR).append("Date").append(LINE_BREAK);
        for (Mouvement m : mouvements) {
            sb.append(m.getType()).append(SEPARATOR)
                    .append(m.getLot() != null ? escape(m.getLot().getNumeroLot()) : "").append(SEPARATOR)
                    .append(m.getEngraisType() != null ? escape(m.getEngraisType().getCode()) : "").append(SEPARATOR)
                    .append(m.getDepotSource() != null ? escape(m.getDepotSource().getCode()) : "").append(SEPARATOR)
                    .append(m.getDepotDest() != null ? escape(m.getDepotDest().getCode()) : "").append(SEPARATOR)
                    .append(m.getQuantite()).append(SEPARATOR)
                    .append(m.getAgent() != null ? escape(m.getAgent().getUsername()) : "").append(SEPARATOR)
                    .append(m.getTicket() != null ? escape(m.getTicket().getNumeroTicket()) : "").append(SEPARATOR)
                    .append(m.getCommentaire() != null ? escape(m.getCommentaire()) : "").append(SEPARATOR)
                    .append(m.getDateMouvement()).append(LINE_BREAK);
        }
        return sb.toString().getBytes(StandardCharsets.UTF_8);
    }

    private String escape(String value) {
        if (value == null) {
            return "";
        }
        if (value.contains(";") || value.contains("\"") || value.contains("\n")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }
}
