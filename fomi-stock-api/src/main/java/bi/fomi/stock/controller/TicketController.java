package bi.fomi.stock.controller;

import bi.fomi.stock.dto.RejetTicketRequest;
import bi.fomi.stock.dto.TicketRequest;
import bi.fomi.stock.dto.TicketResponse;
import bi.fomi.stock.model.enums.StatutTicket;
import bi.fomi.stock.service.TicketService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tickets")
@RequiredArgsConstructor
public class TicketController {

    private final TicketService ticketService;

    @GetMapping
    public Page<TicketResponse> lister(@RequestParam(required = false) Long depotId,
                                       @RequestParam(required = false) StatutTicket statut,
                                       @RequestParam(required = false) String saison,
                                       @RequestParam(defaultValue = "0") int page,
                                       @RequestParam(defaultValue = "50") int size) {
        return ticketService.lister(depotId, statut, saison, PageRequest.of(page, Math.min(size, 200)));
    }

    @GetMapping("/{id}")
    public TicketResponse getById(@PathVariable Long id) {
        return ticketService.getById(id);
    }

    @PostMapping
    public TicketResponse creer(@Valid @RequestBody TicketRequest request) {
        return ticketService.creer(request);
    }

    @PutMapping("/{id}")
    public TicketResponse modifier(@PathVariable Long id, @Valid @RequestBody TicketRequest request) {
        return ticketService.modifier(id, request);
    }

    @PatchMapping("/{id}/activer")
    public TicketResponse activer(@PathVariable Long id) {
        return ticketService.activer(id);
    }

    @PatchMapping("/{id}/rejeter")
    public TicketResponse rejeter(@PathVariable Long id, @Valid @RequestBody RejetTicketRequest request) {
        return ticketService.rejeter(id, request.motif());
    }

    /**
     * Clôture une saison : les tickets non entièrement servis passent en
     * arriéré (reliquat dû à l'agriculteur) et les agriculteurs sont notifiés.
     */
    @PostMapping("/expirer")
    public java.util.Map<String, Object> expirer(@RequestParam String saison) {
        int expires = ticketService.expirerTickets(saison);
        return java.util.Map.of("saison", saison, "ticketsArrieres", expires);
    }
}
