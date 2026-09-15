package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.NiveauDepot;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;

public record DepotRequest(
        @NotBlank String code,
        @NotBlank String nom,
        @NotNull NiveauDepot niveau,
        Long provinceId,
        Long zoneId,
        Long collineId,
        @PositiveOrZero Integer seuilAlerteMin,
        @PositiveOrZero Integer capaciteMax) {
}
