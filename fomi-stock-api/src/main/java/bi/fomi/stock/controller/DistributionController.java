package bi.fomi.stock.controller;

import bi.fomi.stock.dto.DistributionRequest;
import bi.fomi.stock.dto.DistributionResponse;
import bi.fomi.stock.repository.DistributionRepository;
import bi.fomi.stock.service.DistributionService;
import bi.fomi.stock.service.SecurityUtils;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/distributions")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class DistributionController {

    private final DistributionService distributionService;
    private final DistributionRepository distributionRepository;

    @PostMapping
    @Transactional
    public List<DistributionResponse> distribuer(@Valid @RequestBody DistributionRequest request) {
        return distributionService.distribuer(request, SecurityUtils.currentUser());
    }

    @GetMapping("/ticket/{ticketId}")
    public List<DistributionResponse> parTicket(@PathVariable Long ticketId) {
        return distributionRepository.findByTicketId(ticketId).stream()
                .map(d -> new DistributionResponse(d.getId(), d.getTicket().getNumeroTicket(),
                        d.getLot().getNumeroLot(), d.getDepot().getCode(), d.getQuantite(),
                        d.getAgent().getUsername(), d.getDateDistribution()))
                .toList();
    }
}
