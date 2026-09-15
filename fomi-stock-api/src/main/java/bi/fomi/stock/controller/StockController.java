package bi.fomi.stock.controller;

import bi.fomi.stock.dto.StockResponse;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Stock;
import bi.fomi.stock.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/stocks")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StockController {

    private final StockRepository stockRepository;

    @GetMapping
    public List<StockResponse> lister(@RequestParam(required = false) Long depotId,
                                      @RequestParam(required = false) Long engraisTypeId) {
        List<Stock> stocks;
        if (depotId != null) {
            stocks = stockRepository.findByDepotIdOrderByEngraisTypeCode(depotId);
        } else if (engraisTypeId != null) {
            stocks = stockRepository.findAll().stream()
                    .filter(s -> s.getEngraisType().getId().equals(engraisTypeId))
                    .toList();
        } else {
            stocks = stockRepository.findAll();
        }
        return stocks.stream().map(StockController::toResponse).toList();
    }

    @GetMapping("/disponibles")
    public List<StockResponse> disponibles(@RequestParam Long engraisTypeId) {
        return stockRepository.findByEngraisTypeIdAndQuantiteDisponibleGreaterThan(engraisTypeId, 0).stream()
                .map(StockController::toResponse)
                .toList();
    }

    private static StockResponse toResponse(Stock s) {
        return new StockResponse(s.getDepot().getId(), s.getDepot().getCode(), s.getDepot().getNom(),
                s.getEngraisType().getId(), s.getEngraisType().getCode(), s.getEngraisType().getNom(),
                s.getQuantiteDisponible(), s.getDepot().getSeuilAlerteMin(), s.getUpdatedAt());
    }
}
