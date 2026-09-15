package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record DistributionRequest(
        @NotNull Long ticketId,
        @NotNull Long depotId,
        @NotNull @Positive Integer quantite,
        Long lotId,
        String commentaire) {
}
