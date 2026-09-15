package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.StatutTicket;

import java.time.LocalDate;
import java.time.LocalDateTime;

public record PublicTicketResponse(
        String numeroTicket,
        String agriculteurNomComplet,
        String engraisTypeCode,
        String engraisTypeNom,
        Integer quantiteCommandee,
        Integer quantiteServie,
        Integer quantiteRestante,
        StatutTicket statut,
        LocalDate datePaiement,
        String depotRetraitCode,
        String saison,
        LocalDateTime dateCreation) {
}
