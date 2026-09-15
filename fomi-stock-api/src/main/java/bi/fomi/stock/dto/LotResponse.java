package bi.fomi.stock.dto;

import java.time.LocalDate;
import java.time.LocalDateTime;

public record LotResponse(
        Long id,
        String numeroLot,
        String engraisTypeCode,
        String engraisTypeNom,
        Integer quantiteInitiale,
        LocalDate dateFabrication,
        LocalDate datePeremption,
        LocalDateTime dateReceptionFomi) {
}
