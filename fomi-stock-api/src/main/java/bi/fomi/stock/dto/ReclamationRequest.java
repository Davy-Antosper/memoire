package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;

public record ReclamationRequest(
        @NotNull Long ticketId,
        @NotBlank @Size(max = 200) String motif,
        @Size(max = 1000) String description,
        @PositiveOrZero Integer quantiteManquante) {
}
