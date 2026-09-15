package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.NiveauDepot;

public record DepotResponse(
        Long id,
        String code,
        String nom,
        NiveauDepot niveau,
        Long provinceId,
        String provinceNom,
        Long zoneId,
        String zoneNom,
        Long collineId,
        String collineNom,
        Integer seuilAlerteMin,
        Integer capaciteMax,
        Boolean actif) {
}
