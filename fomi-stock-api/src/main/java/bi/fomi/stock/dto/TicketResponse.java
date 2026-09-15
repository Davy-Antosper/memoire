package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.StatutTicket;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public record TicketResponse(
        Long id,
        String numeroTicket,
        Long agriculteurId,
        String agriculteurNomComplet,
        String engraisTypeCode,
        Integer quantiteCommandee,
        Integer quantiteServie,
        Integer quantiteRestante,
        BigDecimal montantPaye,
        LocalDate datePaiement,
        String depotRetraitCode,
        StatutTicket statut,
        String saison,
        BigDecimal superficieHa,
        LocalDateTime dateCreation) {
}
