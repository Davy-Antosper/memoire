package bi.fomi.stock.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record NotificationRequest(
        @NotBlank @Size(max = 150) String sujet,
        @NotBlank @Size(max = 4000) String message) {
}
