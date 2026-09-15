package bi.fomi.stock.dto;

import bi.fomi.stock.model.enums.TypeMouvement;

import java.time.LocalDateTime;

public record MouvementResponse(
        Long id,
        TypeMouvement type,
        String lotNumero,
        String engraisTypeCode,
        String depotSourceCode,
        String depotDestCode,
        Integer quantite,
        String agentUsername,
        String ticketNumero,
        String commentaire,
        LocalDateTime dateMouvement) {
}
