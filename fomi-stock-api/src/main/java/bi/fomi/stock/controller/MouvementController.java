package bi.fomi.stock.controller;

import bi.fomi.stock.dto.AnnulationRequest;
import bi.fomi.stock.dto.MouvementRequest;
import bi.fomi.stock.dto.MouvementResponse;
import bi.fomi.stock.model.entity.Mouvement;
import bi.fomi.stock.model.enums.TypeMouvement;
import bi.fomi.stock.repository.MouvementRepository;
import bi.fomi.stock.service.MouvementService;
import bi.fomi.stock.service.SecurityUtils;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@RestController
@RequestMapping("/api/mouvements")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MouvementController {

    private final MouvementService mouvementService;
    private final MouvementRepository mouvementRepository;

    @PostMapping("/reception")
    @Transactional
    public MouvementResponse reception(@Valid @RequestBody MouvementRequest request) {
        return mouvementService.reception(request, SecurityUtils.currentUser());
    }

    @PostMapping("/transfert")
    @Transactional
    public List<MouvementResponse> transfert(@Valid @RequestBody MouvementRequest request) {
        return mouvementService.transfert(request, SecurityUtils.currentUser());
    }

    @PostMapping("/{id}/annuler")
    @Transactional
    public MouvementResponse annuler(@PathVariable Long id, @Valid @RequestBody AnnulationRequest request) {
        return mouvementService.annuler(id, request.motif(), SecurityUtils.currentUser());
    }

    @GetMapping
    public Page<MouvementResponse> lister(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size,
            @RequestParam(required = false) TypeMouvement type,
            @RequestParam(required = false) Long agentId,
            @RequestParam(required = false) Long depotId,
            @RequestParam(required = false) String from,
            @RequestParam(required = false) String to) {
        PageRequest pageable = PageRequest.of(page, Math.min(size, 200), Sort.by(Sort.Direction.DESC, "dateMouvement"));
        boolean hasFilter = type != null || agentId != null || depotId != null
                || (from != null && !from.isBlank()) || (to != null && !to.isBlank());
        Page<Mouvement> result = hasFilter
                ? mouvementRepository.findAllFiltered(
                        type != null ? type.name() : null, agentId, depotId,
                        parseDateTime(from), parseDateTime(to), pageable)
                : mouvementRepository.findAll(pageable);
        return result.map(MouvementController::toResponse);
    }

    @GetMapping("/lot/{lotId}")
    public List<MouvementResponse> parLot(@PathVariable Long lotId) {
        return mouvementRepository.findByLotIdOrderByDateMouvementAsc(lotId).stream()
                .map(MouvementController::toResponse)
                .toList();
    }

    private static LocalDateTime parseDateTime(String s) {
        if (s == null || s.isBlank()) return null;
        return LocalDateTime.parse(s, DateTimeFormatter.ISO_LOCAL_DATE_TIME);
    }

    private static MouvementResponse toResponse(Mouvement m) {
        return new MouvementResponse(m.getId(), m.getType(), m.getLot().getNumeroLot(),
                m.getEngraisType().getCode(),
                m.getDepotSource() != null ? m.getDepotSource().getCode() : null,
                m.getDepotDest() != null ? m.getDepotDest().getCode() : null,
                m.getQuantite(), m.getAgent().getUsername(),
                m.getTicket() != null ? m.getTicket().getNumeroTicket() : null,
                m.getCommentaire(), m.getDateMouvement());
    }
}
