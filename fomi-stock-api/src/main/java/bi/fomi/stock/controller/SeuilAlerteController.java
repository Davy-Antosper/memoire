package bi.fomi.stock.controller;

import bi.fomi.stock.dto.SeuilAlerteRequest;
import bi.fomi.stock.dto.SeuilAlerteResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.EngraisType;
import bi.fomi.stock.model.entity.SeuilAlerte;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.EngraisTypeRepository;
import bi.fomi.stock.repository.SeuilAlerteRepository;
import bi.fomi.stock.service.AuditLogService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/seuils-alerte")
@RequiredArgsConstructor
public class SeuilAlerteController {

    private final SeuilAlerteRepository seuilAlerteRepository;
    private final DepotRepository depotRepository;
    private final EngraisTypeRepository engraisTypeRepository;
    private final AuditLogService auditLogService;

    @GetMapping
    public List<SeuilAlerteResponse> lister(@RequestParam(required = false) Long depotId) {
        List<SeuilAlerte> list = depotId != null
                ? seuilAlerteRepository.findByDepotId(depotId)
                : seuilAlerteRepository.findAll();
        return list.stream().map(this::toResponse).toList();
    }

    @PostMapping
    public SeuilAlerteResponse creer(@Valid @RequestBody SeuilAlerteRequest req) {
        Depot depot = depotRepository.findById(req.depotId())
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable"));
        EngraisType engraisType = engraisTypeRepository.findById(req.engraisTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable"));
        if (seuilAlerteRepository.findByDepotIdAndEngraisTypeId(req.depotId(), req.engraisTypeId()).isPresent()) {
            throw new BusinessException("Un seuil existe déjà pour ce dépôt et ce type d'engrais");
        }
        SeuilAlerte seuil = SeuilAlerte.builder()
                .depot(depot)
                .engraisType(engraisType)
                .seuilMin(req.seuilMin())
                .criticite(req.criticite())
                .build();
        SeuilAlerte saved = seuilAlerteRepository.save(seuil);
        auditLogService.log("SEUIL_ALERT_CREATE", "SeuilAlerte", saved.getId(),
                "{\"depot\":\"" + depot.getCode() + "\",\"engrais\":\"" + engraisType.getCode()
                        + "\",\"seuil\":" + req.seuilMin() + "}");
        return toResponse(saved);
    }

    @PutMapping("/{id}")
    public SeuilAlerteResponse modifier(@PathVariable Long id, @Valid @RequestBody SeuilAlerteRequest req) {
        SeuilAlerte seuil = seuilAlerteRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Seuil introuvable"));
        seuil.setSeuilMin(req.seuilMin());
        seuil.setCriticite(req.criticite());
        SeuilAlerte saved = seuilAlerteRepository.save(seuil);
        auditLogService.log("SEUIL_ALERT_UPDATE", "SeuilAlerte", id, null);
        return toResponse(saved);
    }

    @DeleteMapping("/{id}")
    public void supprimer(@PathVariable Long id) {
        seuilAlerteRepository.deleteById(id);
        auditLogService.log("SEUIL_ALERT_DELETE", "SeuilAlerte", id, null);
    }

    private SeuilAlerteResponse toResponse(SeuilAlerte s) {
        return new SeuilAlerteResponse(s.getId(), s.getDepot().getId(), s.getDepot().getCode(),
                s.getEngraisType().getId(), s.getEngraisType().getCode(),
                s.getSeuilMin(), s.getCriticite());
    }
}
