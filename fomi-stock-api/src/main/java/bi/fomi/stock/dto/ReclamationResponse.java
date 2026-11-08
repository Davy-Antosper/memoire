package bi.fomi.stock.dto;

import java.time.LocalDateTime;

public record ReclamationResponse(
        Long id,
        Long ticketId,
        String ticketNumero,
        String agriculteurNomComplet,
        String motif,
        String description,
        Integer quantiteManquante,
        String statut,
        String resolution,
        LocalDateTime dateCreation,
        LocalDateTime dateResolution,
        Boolean estDemo) {
}
