package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.NiveauDepot;

public record DepotResponse(
        Long id,
        String code,
        String nom,
        NiveauDepot niveau,
        Long provinceId,
        String provinceNom,
        Long communeId,
        String communeNom,
        Long zoneId,
        String zoneNom,
        Integer seuilAlerteMin,
        Integer capaciteMax,
        Boolean actif) {
}
