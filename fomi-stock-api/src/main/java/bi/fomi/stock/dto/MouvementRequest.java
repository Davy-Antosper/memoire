package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record MouvementRequest(
        @NotNull Long lotId,
        @NotNull @Positive Integer quantite,
        Long depotSourceId,
        @NotNull Long depotDestId,
        String commentaire,
        String idempotencyKey) {
}
