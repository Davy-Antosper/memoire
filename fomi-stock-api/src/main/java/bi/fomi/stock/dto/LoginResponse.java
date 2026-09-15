package bi.fomi.stock.dto;

public record LoginResponse(
        String token,
        String type,
        String username,
        String nomComplet,
        String role,
        Long depotId) {
}
