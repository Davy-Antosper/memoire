package bi.fomi.stock.controller;

import bi.fomi.stock.dto.CollineResponse;
import bi.fomi.stock.dto.CommuneResponse;
import bi.fomi.stock.dto.ProvinceResponse;
import bi.fomi.stock.dto.ZoneResponse;
import bi.fomi.stock.model.entity.Colline;
import bi.fomi.stock.model.entity.Commune;
import bi.fomi.stock.model.entity.Province;
import bi.fomi.stock.model.entity.Zone;
import bi.fomi.stock.repository.CollineRepository;
import bi.fomi.stock.repository.CommuneRepository;
import bi.fomi.stock.repository.ProvinceRepository;
import bi.fomi.stock.repository.ZoneRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class GeoController {

    private final ProvinceRepository provinceRepository;
    private final CommuneRepository communeRepository;
    private final ZoneRepository zoneRepository;
    private final CollineRepository collineRepository;

    @GetMapping("/provinces")
    public List<ProvinceResponse> provinces() {
        return provinceRepository.findAll().stream().map(GeoController::toProvince).toList();
    }

    @GetMapping("/communes")
    public List<CommuneResponse> communes() {
        return communeRepository.findAll().stream().map(GeoController::toCommune).toList();
    }

    @GetMapping("/provinces/{id}/communes")
    public List<CommuneResponse> communesOf(@PathVariable Long id) {
        return communeRepository.findByProvinceId(id).stream().map(GeoController::toCommune).toList();
    }

    @GetMapping("/zones")
    public List<ZoneResponse> zones() {
        return zoneRepository.findAll().stream().map(GeoController::toZone).toList();
    }

    @GetMapping("/provinces/{id}/zones")
    public List<ZoneResponse> zonesOf(@PathVariable Long id) {
        return zoneRepository.findByCommuneProvinceId(id).stream().map(GeoController::toZone).toList();
    }

    @GetMapping("/communes/{id}/zones")
    public List<ZoneResponse> zonesOfCommune(@PathVariable Long id) {
        return zoneRepository.findByCommuneId(id).stream().map(GeoController::toZone).toList();
    }

    @GetMapping("/collines")
    public List<CollineResponse> collines() {
        return collineRepository.findAll().stream().map(GeoController::toColline).toList();
    }

    @GetMapping("/zones/{id}/collines")
    public List<CollineResponse> collinesOf(@PathVariable Long id) {
        return collineRepository.findByZoneId(id).stream().map(GeoController::toColline).toList();
    }

    private static ProvinceResponse toProvince(Province p) {
        return new ProvinceResponse(p.getId(), p.getCode(), p.getNom());
    }

    private static CommuneResponse toCommune(Commune c) {
        return new CommuneResponse(c.getId(), c.getCode(), c.getNom(),
                c.getProvince().getId(), c.getProvince().getNom());
    }

    private static ZoneResponse toZone(Zone z) {
        Commune commune = z.getCommune();
        Province province = commune.getProvince();
        return new ZoneResponse(z.getId(), z.getCode(), z.getNom(),
                commune.getId(), commune.getNom(),
                province.getId(), province.getNom());
    }

    private static CollineResponse toColline(Colline c) {
        return new CollineResponse(c.getId(), c.getCode(), c.getNom(),
                c.getZone().getId(), c.getZone().getNom());
    }
}
