package bi.fomi.stock.service;

import bi.fomi.stock.dto.DepotRequest;
import bi.fomi.stock.dto.DepotResponse;
import bi.fomi.stock.dto.StockResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Colline;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.Province;
import bi.fomi.stock.model.entity.Zone;
import bi.fomi.stock.model.enums.NiveauDepot;
import bi.fomi.stock.repository.CollineRepository;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.ProvinceRepository;
import bi.fomi.stock.repository.StockRepository;
import bi.fomi.stock.repository.ZoneRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DepotService {

    private final DepotRepository depotRepository;
    private final ProvinceRepository provinceRepository;
    private final ZoneRepository zoneRepository;
    private final CollineRepository collineRepository;
    private final StockRepository stockRepository;
    private final AuditLogService auditLogService;

    @Transactional(readOnly = true)
    public List<StockResponse> listerStock(Long depotId) {
        Depot depot = depotRepository.findById(depotId)
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + depotId));
        return stockRepository.findByDepotIdOrderByEngraisTypeCode(depotId).stream()
                .map(s -> new StockResponse(depot.getId(), depot.getCode(), depot.getNom(),
                        s.getEngraisType().getId(), s.getEngraisType().getCode(), s.getEngraisType().getNom(),
                        s.getQuantiteDisponible(), depot.getSeuilAlerteMin(), s.getUpdatedAt()))
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
        Colline colline = null;

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
            case COLLINE -> {
                if (req.collineId() == null) {
                    throw new BusinessException("Un dépôt COLLINE doit être rattaché à une colline");
                }
                colline = collineRepository.findById(req.collineId())
                        .orElseThrow(() -> new ResourceNotFoundException("Colline introuvable"));
            }
        }

        depot.setCode(req.code());
        depot.setNom(req.nom());
        depot.setNiveau(niveau);
        depot.setProvince(province);
        depot.setZone(zone);
        depot.setColline(colline);
        depot.setSeuilAlerteMin(req.seuilAlerteMin() != null ? req.seuilAlerteMin() : 100);
        depot.setCapaciteMax(req.capaciteMax());
    }

    private DepotResponse toResponse(Depot d) {
        return new DepotResponse(d.getId(), d.getCode(), d.getNom(), d.getNiveau(),
                d.getProvince() != null ? d.getProvince().getId() : null,
                d.getProvince() != null ? d.getProvince().getNom() : null,
                d.getZone() != null ? d.getZone().getId() : null,
                d.getZone() != null ? d.getZone().getNom() : null,
                d.getColline() != null ? d.getColline().getId() : null,
                d.getColline() != null ? d.getColline().getNom() : null,
                d.getSeuilAlerteMin(), d.getCapaciteMax(), d.getActif());
    }
}
