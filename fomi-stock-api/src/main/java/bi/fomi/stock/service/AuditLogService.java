package bi.fomi.stock.service;

import bi.fomi.stock.model.entity.AuditLog;
import bi.fomi.stock.model.entity.Utilisateur;
import bi.fomi.stock.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

@Service
@RequiredArgsConstructor
public class AuditLogService {

    private final AuditLogRepository auditLogRepository;

    public void log(String action, String entityType, Long entityId, String detailsJson) {
        Utilisateur user = SecurityUtils.currentUserOrNull();
        String ip = null;
        if (RequestContextHolder.getRequestAttributes() instanceof ServletRequestAttributes attrs) {
            ip = attrs.getRequest().getRemoteAddr();
        }
        auditLogRepository.save(AuditLog.builder()
                .utilisateur(user)
                .action(action)
                .entityType(entityType)
                .entityId(entityId)
                .ipAddress(ip)
                .detailsJson(detailsJson)
                .build());
    }

    public void log(String action, String entityType, Long entityId) {
        log(action, entityType, entityId, null);
    }
}
