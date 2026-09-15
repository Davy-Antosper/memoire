package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;

public record AnnulationRequest(@NotBlank String motif) {
}
