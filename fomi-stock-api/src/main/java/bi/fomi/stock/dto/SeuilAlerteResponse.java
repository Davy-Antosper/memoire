package bi.fomi.stock.dto;

public record SeuilAlerteResponse(
        Long id,
        Long depotId,
        String depotCode,
        Long engraisTypeId,
        String engraisCode,
        Integer seuilMin,
        String criticite) {
}
