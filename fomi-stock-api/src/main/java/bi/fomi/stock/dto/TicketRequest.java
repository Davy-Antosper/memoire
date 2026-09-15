package bi.fomi.stock.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.math.BigDecimal;
import java.time.LocalDate;

public record TicketRequest(
        @NotBlank String numeroTicket,
        @NotNull Long agriculteurId,
        @NotNull Long engraisTypeId,
        @NotNull @Positive Integer quantiteCommandee,
        @NotNull @DecimalMin("0.01") BigDecimal montantPaye,
        @NotNull LocalDate datePaiement,
        @NotNull Long depotRetraitId,
        @NotBlank String saison,
        BigDecimal superficieHa) {
}
