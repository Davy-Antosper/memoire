package bi.fomi.stock.controller;

import bi.fomi.stock.dto.RuptureResponse;
import bi.fomi.stock.dto.StockParZoneResponse;
import bi.fomi.stock.dto.TauxServiceZoneResponse;
import bi.fomi.stock.service.StatsService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/statistiques")
@RequiredArgsConstructor
public class StatsController {

    private final StatsService statsService;

    @GetMapping("/taux-service")
    public List<TauxServiceZoneResponse> tauxService() {
        return statsService.tauxServiceParZone();
    }

    @GetMapping("/stocks-par-province")
    public List<StockParZoneResponse> stocksParProvince() {
        return statsService.stockParProvince();
    }

    @GetMapping("/ruptures")
    public List<RuptureResponse> ruptures() {
        return statsService.ruptures();
    }

    @GetMapping("/tickets-non-servis-par-colline")
    public List<Map<String, Object>> ticketsNonServisParColline() {
        return statsService.ticketsNonServisParColline().stream()
                .map(row -> Map.<String, Object>of(
                        "collineId", row[0],
                        "collineNom", row[1] != null ? row[1] : "",
                        "zoneNom", row[2] != null ? row[2] : "",
                        "nombreTickets", row[3],
                        "quantiteCommandee", row[4],
                        "quantiteServie", row[5],
                        "quantiteRestante", row[6]))
                .toList();
    }

    @GetMapping("/taux-service-par-province")
    public List<Map<String, Object>> tauxServiceParProvince() {
        return statsService.tauxServiceParProvince().stream()
                .map(row -> {
                    long commande = ((Number) row[3]).longValue();
                    long servi = ((Number) row[2]).longValue();
                    double taux = commande == 0 ? 0 : (double) servi / commande;
                    return Map.<String, Object>of(
                            "provinceId", row[0],
                            "provinceNom", row[1],
                            "quantiteServie", row[2],
                            "quantiteCommandee", row[3],
                            "tauxService", taux);
                })
                .toList();
    }

    @GetMapping("/mouvements-par-agent/{agentId}")
    public List<Map<String, Object>> mouvementsParAgent(@PathVariable Long agentId) {
        return statsService.mouvementsParAgent(agentId).stream()
                .map(row -> Map.<String, Object>of(
                        "type", row[0],
                        "nombre", row[1],
                        "quantiteTotale", row[2]))
                .toList();
    }
}
