package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.time.LocalDate;

public record LotRequest(
        String numeroLot,
        @NotNull Long engraisTypeId,
        @NotNull @Positive Integer quantiteInitiale,
        LocalDate dateFabrication,
        LocalDate datePeremption) {
}
