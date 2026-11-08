package bi.fomi.stock.service;

import bi.fomi.stock.dto.DepotRequest;
import bi.fomi.stock.dto.DepotResponse;
import bi.fomi.stock.dto.StockResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.Province;
import bi.fomi.stock.model.entity.Zone;
import bi.fomi.stock.model.enums.NiveauDepot;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.ProvinceRepository;
import bi.fomi.stock.repository.SeuilAlerteRepository;
import bi.fomi.stock.repository.StockRepository;
import bi.fomi.stock.repository.ZoneRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class DepotService {

    private final DepotRepository depotRepository;
    private final ProvinceRepository provinceRepository;
    private final ZoneRepository zoneRepository;
    private final StockRepository stockRepository;
    private final SeuilAlerteRepository seuilAlerteRepository;
    private final AuditLogService auditLogService;

    @Transactional(readOnly = true)
    public List<StockResponse> listerStock(Long depotId) {
        Depot depot = depotRepository.findById(depotId)
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + depotId));
        Map<Long, Integer> seuils = seuilAlerteRepository.findByDepotId(depotId).stream()
                .collect(Collectors.toMap(s -> s.getEngraisType().getId(), s -> s.getSeuilMin()));
        return stockRepository.findByDepotIdOrderByEngraisTypeCode(depotId).stream()
                .map(s -> new StockResponse(depot.getId(), depot.getCode(), depot.getNom(),
                        s.getEngraisType().getId(), s.getEngraisType().getCode(), s.getEngraisType().getNom(),
                        s.getQuantiteDisponible(),
                        seuils.getOrDefault(s.getEngraisType().getId(), depot.getSeuilAlerteMin()),
                        s.getUpdatedAt()))
                .toList();
    }

    @Transactional(readOnly = true)
    public List<DepotResponse> lister() {
        return depotRepository.findAll().stream().map(this::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public DepotResponse getById(Long id) {
        return depotRepository.findById(id).map(this::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + id));
    }

    @Transactional
    public DepotResponse creer(DepotRequest req) {
        if (depotRepository.findByCode(req.code()).isPresent()) {
            throw new BusinessException("Code dépôt déjà utilisé : " + req.code());
        }
        Depot depot = new Depot();
        appliquer(req, depot);
        Depot saved = depotRepository.save(depot);
        auditLogService.log("DEPOT_CREATE", "Depot", saved.getId(),
                "{\"code\":\"" + saved.getCode() + "\",\"niveau\":\"" + saved.getNiveau()
                        + "\",\"seuilAlerteMin\":" + saved.getSeuilAlerteMin()
                        + ",\"capaciteMax\":" + saved.getCapaciteMax() + "}");
        return toResponse(saved);
    }

    @Transactional
    public DepotResponse modifier(Long id, DepotRequest req) {
        Depot depot = depotRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + id));
        depotRepository.findByCode(req.code())
                .filter(existant -> !existant.getId().equals(id))
                .ifPresent(existant -> {
                    throw new BusinessException("Code dépôt déjà utilisé : " + req.code());
                });
        appliquer(req, depot);
        Depot saved = depotRepository.save(depot);
        auditLogService.log("DEPOT_UPDATE", "Depot", saved.getId(),
                "{\"code\":\"" + saved.getCode() + "\",\"niveau\":\"" + saved.getNiveau()
                        + "\",\"seuilAlerteMin\":" + saved.getSeuilAlerteMin() + "}");
        return toResponse(saved);
    }

    private void appliquer(DepotRequest req, Depot depot) {
        NiveauDepot niveau = req.niveau();
        Province province = null;
        Zone zone = null;

        switch (niveau) {
            case PROVINCE -> {
                if (req.provinceId() == null) {
                    throw new BusinessException("Un dépôt PROVINCE doit être rattaché à une province");
                }
                province = provinceRepository.findById(req.provinceId())
                        .orElseThrow(() -> new ResourceNotFoundException("Province introuvable"));
            }
            case ZONE -> {
                if (req.zoneId() == null) {
                    throw new BusinessException("Un dépôt ZONE doit être rattaché à une zone");
                }
                zone = zoneRepository.findById(req.zoneId())
                        .orElseThrow(() -> new ResourceNotFoundException("Zone introuvable"));
            }
        }

        depot.setCode(req.code());
        depot.setNom(req.nom());
        depot.setNiveau(niveau);
        depot.setProvince(province);
        depot.setZone(zone);
        depot.setSeuilAlerteMin(req.seuilAlerteMin() != null ? req.seuilAlerteMin() : 100);
        depot.setCapaciteMax(req.capaciteMax());
    }

    private DepotResponse toResponse(Depot d) {
        Province province = d.getProvince();
        if (province == null && d.getZone() != null && d.getZone().getCommune() != null) {
            province = d.getZone().getCommune().getProvince();
        }
        Long communeId = d.getZone() != null && d.getZone().getCommune() != null
                ? d.getZone().getCommune().getId() : null;
        String communeNom = d.getZone() != null && d.getZone().getCommune() != null
                ? d.getZone().getCommune().getNom() : null;
        return new DepotResponse(d.getId(), d.getCode(), d.getNom(), d.getNiveau(),
                province != null ? province.getId() : null,
                province != null ? province.getNom() : null,
                communeId, communeNom,
                d.getZone() != null ? d.getZone().getId() : null,
                d.getZone() != null ? d.getZone().getNom() : null,
                d.getSeuilAlerteMin(), d.getCapaciteMax(), d.getActif());
    }
}
