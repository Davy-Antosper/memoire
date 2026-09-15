package bi.fomi.stock.dto;

import java.time.LocalDateTime;

public record StockResponse(
        Long depotId,
        String depotCode,
        String depotNom,
        Long engraisTypeId,
        String engraisCode,
        String engraisNom,
        Integer quantiteDisponible,
        Integer seuilAlerteMin,
        LocalDateTime updatedAt) {
}
