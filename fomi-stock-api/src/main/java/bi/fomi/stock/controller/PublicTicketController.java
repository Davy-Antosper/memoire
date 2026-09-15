package bi.fomi.stock.controller;

import bi.fomi.stock.dto.PublicTicketResponse;
import bi.fomi.stock.service.TicketService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/public")
@RequiredArgsConstructor
public class PublicTicketController {

    private final TicketService ticketService;

    @GetMapping("/tickets/{numero}")
    public PublicTicketResponse consulterTicket(@PathVariable String numero) {
        return ticketService.getPublicByNumero(numero);
    }
}
