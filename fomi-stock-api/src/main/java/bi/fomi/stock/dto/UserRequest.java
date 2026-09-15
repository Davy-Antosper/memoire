package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.RoleUtilisateur;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record UserRequest(
        @NotBlank @Size(min = 3, max = 50) String username,
        @Size(min = 6, max = 100) String password,
        @NotBlank @Size(max = 150) String nomComplet,
        @NotNull RoleUtilisateur role,
        Long depotId,
        Long zoneId,
        Long provinceId,
        Boolean actif) {
}
