package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record RejetTicketRequest(
        @NotBlank(message = "Le motif de rejet est obligatoire")
        @Size(max = 500, message = "Le motif de rejet ne peut pas dépasser 500 caractères")
        String motif) {
}
