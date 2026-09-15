package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record AgriculteurRequest(
        @NotBlank String numeroIdentite,
        @NotBlank String nom,
        @NotBlank String prenom,
        String telephone,
        @NotNull Long collineId,
        Boolean estCooperative) {
}
