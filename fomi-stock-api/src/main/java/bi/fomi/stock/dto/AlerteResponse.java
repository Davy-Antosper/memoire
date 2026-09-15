package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.NiveauAlerte;
import bi.fomi.stock.model.enums.TypeAlerte;

import java.time.LocalDateTime;

public record AlerteResponse(
        Long id,
        String depotCode,
        String depotNom,
        String engraisTypeCode,
        TypeAlerte type,
        String message,
        NiveauAlerte niveau,
        Boolean traitee,
        LocalDateTime createdAt) {
}
