package bi.fomi.stock.controller;

import bi.fomi.stock.dto.ReclamationRequest;
import bi.fomi.stock.dto.ReclamationResponse;
import bi.fomi.stock.dto.ReclamationStatutRequest;
import bi.fomi.stock.service.ReclamationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reclamations")
@RequiredArgsConstructor
public class ReclamationController {

    private final ReclamationService reclamationService;

    @GetMapping
    public List<ReclamationResponse> lister(@RequestParam(required = false) String statut) {
        return reclamationService.lister(statut);
    }

    @PostMapping
    public ReclamationResponse creer(@Valid @RequestBody ReclamationRequest request) {
        return reclamationService.creer(request);
    }

    @PatchMapping("/{id}/statut")
    public ReclamationResponse changerStatut(@PathVariable Long id,
                                             @Valid @RequestBody ReclamationStatutRequest request) {
        return reclamationService.changerStatut(id, request.statut(), request.resolution());
    }
}
