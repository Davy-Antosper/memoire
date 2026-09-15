package bi.fomi.stock.controller;

import bi.fomi.stock.dto.AlerteResponse;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Alerte;
import bi.fomi.stock.repository.AlerteRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/alertes")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AlerteController {

    private final AlerteRepository alerteRepository;

    @GetMapping
    public List<AlerteResponse> lister(@RequestParam(required = false) Boolean nonTraitees) {
        List<Alerte> alertes = Boolean.TRUE.equals(nonTraitees)
                ? alerteRepository.findByTraiteeFalseOrderByCreatedAtDesc()
                : alerteRepository.findAll();
        return alertes.stream().map(AlerteController::toResponse).toList();
    }

    @GetMapping("/depot/{depotId}")
    public List<AlerteResponse> parDepot(@PathVariable Long depotId) {
        return alerteRepository.findByDepotIdOrderByCreatedAtDesc(depotId).stream()
                .map(AlerteController::toResponse)
                .toList();
    }

    @Transactional
    @PatchMapping("/{id}/traiter")
    public AlerteResponse traiter(@PathVariable Long id) {
        Alerte alerte = alerteRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Alerte introuvable : " + id));
        alerte.setTraitee(true);
        return toResponse(alerteRepository.save(alerte));
    }

    private static AlerteResponse toResponse(Alerte a) {
        return new AlerteResponse(a.getId(), a.getDepot().getCode(), a.getDepot().getNom(),
                a.getEngraisType().getCode(), a.getType(), a.getMessage(), a.getNiveau(),
                a.getTraitee(), a.getCreatedAt());
    }
}
