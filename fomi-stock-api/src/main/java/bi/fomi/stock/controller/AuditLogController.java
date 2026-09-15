package bi.fomi.stock.controller;

import bi.fomi.stock.dto.AuditLogResponse;
import bi.fomi.stock.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/audit-logs")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AuditLogController {

    private final AuditLogRepository auditLogRepository;

    @GetMapping
    public Page<AuditLogResponse> lister(@RequestParam(required = false) String action,
                                         @RequestParam(required = false) String entityType,
                                         @RequestParam(required = false) Long entityId,
                                         @RequestParam(required = false) Long utilisateurId,
                                         @RequestParam(defaultValue = "0") int page,
                                         @RequestParam(defaultValue = "50") int size) {
        return auditLogRepository.search(action, entityType, entityId, utilisateurId,
                        PageRequest.of(page, Math.min(size, 200)))
                .map(log -> new AuditLogResponse(log.getId(),
                        log.getUtilisateur() != null ? log.getUtilisateur().getUsername() : null,
                        log.getAction(), log.getEntityType(), log.getEntityId(), log.getIpAddress(),
                        log.getDetailsJson(), log.getCreatedAt()));
    }
}
