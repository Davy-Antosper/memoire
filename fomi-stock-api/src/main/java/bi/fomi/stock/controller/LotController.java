package bi.fomi.stock.controller;

import bi.fomi.stock.dto.LotRequest;
import bi.fomi.stock.dto.LotResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.EngraisType;
import bi.fomi.stock.model.entity.Lot;
import bi.fomi.stock.repository.EngraisTypeRepository;
import bi.fomi.stock.repository.LotRepository;
import bi.fomi.stock.service.AuditLogService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;

@RestController
@RequestMapping("/api/lots")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class LotController {

    private final LotRepository lotRepository;
    private final EngraisTypeRepository engraisTypeRepository;
    private final AuditLogService auditLogService;

    @GetMapping
    public List<LotResponse> lister(@RequestParam(required = false) Long engraisTypeId) {
        List<Lot> lots = engraisTypeId != null
                ? lotRepository.findByEngraisTypeIdOrderByDateReceptionFomiAsc(engraisTypeId)
                : lotRepository.findAll();
        return lots.stream().map(LotController::toResponse).toList();
    }

    @GetMapping("/recherche")
    public List<LotResponse> rechercher(@RequestParam String numero) {
        String q = numero.trim().toLowerCase();
        return lotRepository.findAll().stream()
                .filter(l -> l.getNumeroLot().toLowerCase().contains(q))
                .map(LotController::toResponse)
                .toList();
    }

    @PostMapping
    @Transactional
    public LotResponse creer(@Valid @RequestBody LotRequest request) {
        String numero = request.numeroLot() != null && !request.numeroLot().isBlank()
                ? request.numeroLot().trim()
                : genererNumeroLot();
        if (lotRepository.findByNumeroLot(numero).isPresent()) {
            throw new BusinessException("Numéro de lot déjà utilisé : " + numero);
        }
        if (request.dateFabrication() != null && request.datePeremption() != null
                && request.datePeremption().isBefore(request.dateFabrication())) {
            throw new BusinessException("La date de péremption ne peut pas être antérieure à la date de fabrication");
        }
        if (request.datePeremption() != null && request.datePeremption().isBefore(LocalDate.now())) {
            throw new BusinessException("Lot périmé : la date de péremption est déjà dépassée");
        }
        EngraisType engraisType = engraisTypeRepository.findById(request.engraisTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Type d'engrais introuvable"));
        Lot lot = lotRepository.save(Lot.builder()
                .numeroLot(numero)
                .engraisType(engraisType)
                .quantiteInitiale(request.quantiteInitiale())
                .dateFabrication(request.dateFabrication())
                .datePeremption(request.datePeremption())
                .build());
        auditLogService.log("LOT_CREATE", "Lot", lot.getId(),
                "{\"numeroLot\":\"" + lot.getNumeroLot() + "\",\"engrais\":\"" + engraisType.getCode()
                        + "\",\"quantite\":" + request.quantiteInitiale() + "}");
        return toResponse(lot);
    }

    private String genererNumeroLot() {
        String prefix = "FOMI-" + LocalDate.now().getYear() + "-";
        int max = lotRepository.findAll().stream()
                .map(Lot::getNumeroLot)
                .filter(n -> n != null && n.startsWith(prefix))
                .map(n -> n.substring(prefix.length()))
                .filter(s -> s.chars().allMatch(Character::isDigit))
                .map(Integer::parseInt)
                .max(Comparator.naturalOrder())
                .orElse(0);
        return prefix + String.format("%04d", max + 1);
    }

    private static LotResponse toResponse(Lot l) {
        return new LotResponse(l.getId(), l.getNumeroLot(),
                l.getEngraisType().getCode(), l.getEngraisType().getNom(),
                l.getQuantiteInitiale(), l.getDateFabrication(), l.getDatePeremption(),
                l.getDateReceptionFomi());
    }
}
