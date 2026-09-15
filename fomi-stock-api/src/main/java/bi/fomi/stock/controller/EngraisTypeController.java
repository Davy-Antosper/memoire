package bi.fomi.stock.controller;

import bi.fomi.stock.dto.EngraisTypeRequest;
import bi.fomi.stock.dto.EngraisTypeResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.EngraisType;
import bi.fomi.stock.repository.EngraisTypeRepository;
import bi.fomi.stock.service.AuditLogService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/engrais-types")
@RequiredArgsConstructor
public class EngraisTypeController {

    private final EngraisTypeRepository engraisTypeRepository;
    private final AuditLogService auditLogService;

    @GetMapping
    public List<EngraisTypeResponse> lister() {
        return engraisTypeRepository.findAll().stream().map(this::toResponse).toList();
    }

    @GetMapping("/{id}")
    public EngraisTypeResponse getById(@PathVariable Long id) {
        EngraisType e = engraisTypeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable : " + id));
        return toResponse(e);
    }

    @PostMapping
    public EngraisTypeResponse creer(@Valid @RequestBody EngraisTypeRequest req) {
        if (engraisTypeRepository.findByCode(req.code()).isPresent()) {
            throw new BusinessException("Code type d'engrais déjà utilisé : " + req.code());
        }
        EngraisType e = EngraisType.builder()
                .code(req.code())
                .nom(req.nom())
                .poidsSacKg(req.poidsSacKg())
                .prixSubventionne(req.prixSubventionne())
                .actif(req.actif() != null ? req.actif() : true)
                .build();
        EngraisType saved = engraisTypeRepository.save(e);
        auditLogService.log("ENGRAIS_TYPE_CREATE", "EngraisType", saved.getId(),
                "{\"code\":\"" + saved.getCode() + "\",\"nom\":\"" + saved.getNom() + "\"}");
        return toResponse(saved);
    }

    @PutMapping("/{id}")
    public EngraisTypeResponse modifier(@PathVariable Long id, @Valid @RequestBody EngraisTypeRequest req) {
        EngraisType e = engraisTypeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable : " + id));
        engraisTypeRepository.findByCode(req.code())
                .filter(existant -> !existant.getId().equals(id))
                .ifPresent(existant -> {
                    throw new BusinessException("Code type d'engrais déjà utilisé : " + req.code());
                });
        e.setCode(req.code());
        e.setNom(req.nom());
        e.setPoidsSacKg(req.poidsSacKg());
        e.setPrixSubventionne(req.prixSubventionne());
        if (req.actif() != null) e.setActif(req.actif());
        EngraisType saved = engraisTypeRepository.save(e);
        auditLogService.log("ENGRAIS_TYPE_UPDATE", "EngraisType", saved.getId(),
                "{\"code\":\"" + saved.getCode() + "\"}");
        return toResponse(saved);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> supprimer(@PathVariable Long id) {
        EngraisType e = engraisTypeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable : " + id));
        e.setActif(false);
        engraisTypeRepository.save(e);
        auditLogService.log("ENGRAIS_TYPE_DEACTIVATE", "EngraisType", id,
                "{\"code\":\"" + e.getCode() + "\"}");
        return ResponseEntity.noContent().build();
    }

    private EngraisTypeResponse toResponse(EngraisType e) {
        return new EngraisTypeResponse(e.getId(), e.getCode(), e.getNom(),
                e.getPoidsSacKg(), e.getPrixSubventionne(), e.getActif());
    }
}
