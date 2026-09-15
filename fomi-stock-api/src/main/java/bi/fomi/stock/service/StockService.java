package bi.fomi.stock.service;

import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.EngraisType;
import bi.fomi.stock.model.entity.Lot;
import bi.fomi.stock.model.entity.Stock;
import bi.fomi.stock.model.entity.StockLot;
import bi.fomi.stock.repository.StockLotRepository;
import bi.fomi.stock.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class StockService {

    private final StockRepository stockRepository;
    private final StockLotRepository stockLotRepository;

    @Transactional
    public void ajouter(Depot depot, Lot lot, int quantite) {
        if (lot.getDatePeremption() != null && lot.getDatePeremption().isBefore(LocalDate.now())) {
            throw new BusinessException("Lot périmé : impossible de l'ajouter au stock");
        }

        StockLot stockLot = stockLotRepository.findByDepotIdAndLotId(depot.getId(), lot.getId())
                .orElseGet(() -> StockLot.builder()
                        .depot(depot)
                        .lot(lot)
                        .quantite(0)
                        .build());
        stockLot.setQuantite(stockLot.getQuantite() + quantite);
        stockLotRepository.save(stockLot);

        Stock stock = getOrCreate(depot, lot.getEngraisType());
        stock.setQuantiteDisponible(stock.getQuantiteDisponible() + quantite);
        stockRepository.save(stock);
    }

    @Transactional
    public List<LotSortie> sortirFifo(Depot depot, EngraisType engraisType, int quantite, Long lotIdForce) {
        List<StockLot> lots;

        if (lotIdForce != null) {
            StockLot forced = stockLotRepository.findByDepotIdAndLotId(depot.getId(), lotIdForce)
                    .orElseThrow(() -> new BusinessException("Lot " + lotIdForce + " absent de ce dépôt"));
            if (!forced.getLot().getEngraisType().getId().equals(engraisType.getId())) {
                throw new BusinessException("Le lot " + forced.getLot().getNumeroLot() + " n'est pas de type " + engraisType.getNom());
            }
            if (forced.getQuantite() < quantite) {
                throw new BusinessException("Quantité insuffisante pour le lot " + forced.getLot().getNumeroLot());
            }
            lots = List.of(forced);
        } else {
            lots = stockLotRepository
                    .findByDepotIdAndLotEngraisTypeIdAndQuantiteGreaterThanOrderByLotDateReceptionFomiAsc(
                            depot.getId(), engraisType.getId(), 0);
            lots = lots.stream()
                    .filter(sl -> sl.getLot().getDatePeremption() == null || !sl.getLot().getDatePeremption().isBefore(LocalDate.now()))
                    .collect(Collectors.toList());
        }

        if (lots.isEmpty()) {
            throw new BusinessException("Stock insuffisant au dépôt " + depot.getNom()
                    + " (" + engraisType.getNom() + ") : aucun lot disponible (tous périmés)");
        }

        int restant = quantite;
        List<LotSortie> sorties = new ArrayList<>();
        for (StockLot stockLot : lots) {
            if (restant <= 0) {
                break;
            }
            int pris = Math.min(stockLot.getQuantite(), restant);
            stockLot.setQuantite(stockLot.getQuantite() - pris);
            restant -= pris;
            sorties.add(new LotSortie(stockLot.getLot(), pris));
        }
        if (restant > 0) {
            throw new BusinessException("Stock insuffisant au dépôt " + depot.getNom()
                    + " (" + engraisType.getNom() + ") : manque " + restant + " sacs");
        }

        Stock stock = getOrCreate(depot, engraisType);
        stock.setQuantiteDisponible(stock.getQuantiteDisponible() - quantite);
        stockRepository.save(stock);
        return sorties;
    }

    @Transactional(readOnly = true)
    public int disponibilite(Depot depot, EngraisType engraisType) {
        return stockRepository.findByDepotIdAndEngraisTypeId(depot.getId(), engraisType.getId())
                .map(Stock::getQuantiteDisponible)
                .orElse(0);
    }

    private Stock getOrCreate(Depot depot, EngraisType engraisType) {
        return stockRepository.findByDepotIdAndEngraisTypeId(depot.getId(), engraisType.getId())
                .orElseGet(() -> Stock.builder()
                        .depot(depot)
                        .engraisType(engraisType)
                        .quantiteDisponible(0)
                        .build());
    }
}
