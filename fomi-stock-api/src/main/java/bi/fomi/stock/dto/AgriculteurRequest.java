package bi.fomi.stock.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record AgriculteurRequest(
        @NotBlank String numeroIdentite,
        @NotBlank String nom,
        @NotBlank String prenom,
        String telephone,
        @Email @Size(max = 150) String email,
        @NotNull Long collineId,
        Boolean estCooperative) {
}
