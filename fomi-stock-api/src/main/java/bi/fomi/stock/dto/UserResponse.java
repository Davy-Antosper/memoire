package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.RoleUtilisateur;

import java.time.LocalDateTime;

public record UserResponse(
        Long id,
        String username,
        String nomComplet,
        RoleUtilisateur role,
        Long depotId,
        Long zoneId,
        Long provinceId,
        Boolean actif,
        LocalDateTime createdAt) {
}
