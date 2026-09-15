package bi.fomi.stock.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.math.BigDecimal;

public record EngraisTypeRequest(
        @NotBlank String code,
        @NotBlank String nom,
        @NotNull @Positive BigDecimal poidsSacKg,
        @NotNull @DecimalMin("0.01") BigDecimal prixSubventionne,
        Boolean actif) {
}
