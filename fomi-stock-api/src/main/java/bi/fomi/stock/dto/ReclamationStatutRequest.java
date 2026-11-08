package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ReclamationStatutRequest(
        @NotBlank String statut,
        @Size(max = 1000) String resolution) {
}
