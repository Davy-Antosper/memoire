package bi.fomi.stock.dto;

public record TauxServiceZoneResponse(
        Long zoneId,
        String zoneNom,
        double tauxService,
        long commande,
        long servi) {
}
