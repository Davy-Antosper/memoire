package bi.fomi.stock.dto;

public record ZoneResponse(Long id, String code, String nom,
                           Long communeId, String communeNom,
                           Long provinceId, String provinceNom) {
}
