package bi.fomi.stock.controller;

import bi.fomi.stock.dto.StockResponse;
import bi.fomi.stock.model.entity.SeuilAlerte;
import bi.fomi.stock.model.entity.Stock;
import bi.fomi.stock.repository.SeuilAlerteRepository;
import bi.fomi.stock.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/stocks")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StockController {

    private final StockRepository stockRepository;
    private final SeuilAlerteRepository seuilAlerteRepository;

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
        return stocks.stream().map(this::toResponse).toList();
    }

    @GetMapping("/disponibles")
    public List<StockResponse> disponibles(@RequestParam Long engraisTypeId) {
        return stockRepository.findByEngraisTypeIdAndQuantiteDisponibleGreaterThan(engraisTypeId, 0).stream()
                .map(this::toResponse)
                .toList();
    }

    private StockResponse toResponse(Stock s) {
        Long depotId = s.getDepot().getId();
        Long engraisTypeId = s.getEngraisType().getId();
        // Seuil propre au couple dépôt + produit, avec repli sur le seuil du dépôt.
        Map<Long, Integer> seuils = seuilAlerteRepository.findByDepotId(depotId).stream()
                .collect(Collectors.toMap(
                        sa -> sa.getEngraisType().getId(),
                        SeuilAlerte::getSeuilMin,
                        (a, b) -> a));
        return new StockResponse(depotId, s.getDepot().getCode(), s.getDepot().getNom(),
                engraisTypeId, s.getEngraisType().getCode(), s.getEngraisType().getNom(),
                s.getQuantiteDisponible(),
                seuils.getOrDefault(engraisTypeId, s.getDepot().getSeuilAlerteMin()),
                s.getUpdatedAt());
    }
}
