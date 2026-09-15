package bi.fomi.stock.dto;

import java.time.LocalDateTime;

public record AuditLogResponse(
        Long id,
        String utilisateurUsername,
        String action,
        String entityType,
        Long entityId,
        String ipAddress,
        String detailsJson,
        LocalDateTime createdAt) {
}
