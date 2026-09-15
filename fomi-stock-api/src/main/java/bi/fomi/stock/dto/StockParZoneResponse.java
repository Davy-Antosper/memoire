package bi.fomi.stock.dto;

public record StockParZoneResponse(
        String nom,
        long stock,
        long distribue,
        long reste) {
}
