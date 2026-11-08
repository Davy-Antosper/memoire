package bi.fomi.stock.dto;

import java.math.BigDecimal;

public record EngraisTypeResponse(Long id, String code, String nom, BigDecimal poidsSacKg,
                                  BigDecimal prixSubventionne, Boolean prixAConfirmer, Boolean actif) {
}
