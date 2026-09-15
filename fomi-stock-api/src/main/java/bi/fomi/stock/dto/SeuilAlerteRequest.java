package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record SeuilAlerteRequest(
        @NotNull Long depotId,
        @NotNull Long engraisTypeId,
        @NotNull @Positive Integer seuilMin,
        @NotBlank String criticite) {
}
