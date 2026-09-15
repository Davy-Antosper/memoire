package bi.fomi.stock.controller;

import bi.fomi.stock.dto.DepotRequest;
import bi.fomi.stock.dto.DepotResponse;
import bi.fomi.stock.dto.StockResponse;
import bi.fomi.stock.service.DepotService;
import bi.fomi.stock.service.StockService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/depots")
@RequiredArgsConstructor
public class DepotController {

    private final DepotService depotService;
    private final StockService stockService;

    @GetMapping
    public List<DepotResponse> lister() {
        return depotService.lister();
    }

    @GetMapping("/{id}")
    public DepotResponse getById(@PathVariable Long id) {
        return depotService.getById(id);
    }

    @PostMapping
    public DepotResponse creer(@Valid @RequestBody DepotRequest request) {
        return depotService.creer(request);
    }

    @PutMapping("/{id}")
    public DepotResponse modifier(@PathVariable Long id, @Valid @RequestBody DepotRequest request) {
        return depotService.modifier(id, request);
    }

    @GetMapping("/{id}/stock")
    public List<StockResponse> stockDuDepot(@PathVariable Long id) {
        return depotService.listerStock(id);
    }
}
