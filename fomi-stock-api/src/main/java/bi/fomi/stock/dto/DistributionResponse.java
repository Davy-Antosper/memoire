package bi.fomi.stock.dto;

import java.time.LocalDateTime;

public record DistributionResponse(
        Long id,
        String ticketNumero,
        String lotNumero,
        String depotCode,
        Integer quantite,
        String agentUsername,
        LocalDateTime dateDistribution) {
}
