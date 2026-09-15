package bi.fomi.stock.controller;

import bi.fomi.stock.dto.AgriculteurRequest;
import bi.fomi.stock.dto.AgriculteurResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Agriculteur;
import bi.fomi.stock.model.entity.Colline;
import bi.fomi.stock.repository.AgriculteurRepository;
import bi.fomi.stock.repository.CollineRepository;
import bi.fomi.stock.service.AuditLogService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/agriculteurs")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AgriculteurController {

    private final AgriculteurRepository agriculteurRepository;
    private final CollineRepository collineRepository;
    private final AuditLogService auditLogService;

    @GetMapping
    public Page<AgriculteurResponse> lister(@RequestParam(defaultValue = "0") int page,
                                            @RequestParam(defaultValue = "50") int size) {
        return agriculteurRepository.findAll(PageRequest.of(page, Math.min(size, 200)))
                .map(AgriculteurController::toResponse);
    }

    @GetMapping("/{id}")
    public AgriculteurResponse getById(@PathVariable Long id) {
        return agriculteurRepository.findById(id)
                .map(AgriculteurController::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Agriculteur introuvable : " + id));
    }

    @GetMapping("/recherche")
    public List<AgriculteurResponse> rechercher(@RequestParam String telephone) {
        return agriculteurRepository.findByTelephone(telephone).stream()
                .map(AgriculteurController::toResponse)
                .toList();
    }

    @PostMapping
    @Transactional
    public AgriculteurResponse creer(@Valid @RequestBody AgriculteurRequest request) {
        if (agriculteurRepository.findByNumeroIdentite(request.numeroIdentite()).isPresent()) {
            throw new BusinessException("Numéro d'identité déjà utilisé : " + request.numeroIdentite());
        }
        if (request.telephone() != null
                && !request.telephone().isBlank()
                && agriculteurRepository.existsByTelephone(request.telephone())) {
            throw new BusinessException("Téléphone déjà utilisé : " + request.telephone());
        }
        Colline colline = collineRepository.findById(request.collineId())
                .orElseThrow(() -> new ResourceNotFoundException("Colline introuvable"));
        Agriculteur agriculteur = agriculteurRepository.save(Agriculteur.builder()
                .numeroIdentite(request.numeroIdentite())
                .nom(request.nom())
                .prenom(request.prenom())
                .telephone(request.telephone())
                .colline(colline)
                .estCooperative(Boolean.TRUE.equals(request.estCooperative()))
                .build());
        auditLogService.log("AGRICULTEUR_CREATE", "Agriculteur", agriculteur.getId(),
                "{\"numeroIdentite\":\"" + agriculteur.getNumeroIdentite() + "\",\"telephone\":\""
                        + (agriculteur.getTelephone() != null ? agriculteur.getTelephone() : "") + "\"}");
        return toResponse(agriculteur);
    }

    @PutMapping("/{id}")
    @Transactional
    public AgriculteurResponse modifier(@PathVariable Long id, @Valid @RequestBody AgriculteurRequest request) {
        Agriculteur agriculteur = agriculteurRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Agriculteur introuvable : " + id));
        if (request.telephone() != null
                && !request.telephone().isBlank()
                && agriculteurRepository.findByTelephone(request.telephone()).stream()
                        .anyMatch(a -> !a.getId().equals(id))) {
            throw new BusinessException("Téléphone déjà utilisé : " + request.telephone());
        }
        Colline colline = collineRepository.findById(request.collineId())
                .orElseThrow(() -> new ResourceNotFoundException("Colline introuvable"));
        agriculteur.setNom(request.nom());
        agriculteur.setPrenom(request.prenom());
        agriculteur.setTelephone(request.telephone());
        agriculteur.setColline(colline);
        agriculteur.setEstCooperative(Boolean.TRUE.equals(request.estCooperative()));
        auditLogService.log("AGRICULTEUR_UPDATE", "Agriculteur", agriculteur.getId(),
                "{\"numeroIdentite\":\"" + agriculteur.getNumeroIdentite() + "\",\"telephone\":\""
                        + (agriculteur.getTelephone() != null ? agriculteur.getTelephone() : "") + "\"}");
        return toResponse(agriculteurRepository.save(agriculteur));
    }

    private static AgriculteurResponse toResponse(Agriculteur a) {
        return new AgriculteurResponse(a.getId(), a.getNumeroIdentite(), a.getNom(), a.getPrenom(), a.getTelephone(),
                a.getColline().getId(), a.getColline().getNom(),
                Boolean.TRUE.equals(a.getEstCooperative()));
    }
}
