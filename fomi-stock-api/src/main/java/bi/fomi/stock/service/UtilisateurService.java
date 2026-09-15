package bi.fomi.stock.service;

import bi.fomi.stock.dto.UserRequest;
import bi.fomi.stock.dto.UserResponse;
import bi.fomi.stock.exception.BusinessException;
import bi.fomi.stock.exception.ResourceNotFoundException;
import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.entity.Province;
import bi.fomi.stock.model.entity.Utilisateur;
import bi.fomi.stock.model.entity.Zone;
import bi.fomi.stock.repository.DepotRepository;
import bi.fomi.stock.repository.ProvinceRepository;
import bi.fomi.stock.repository.UtilisateurRepository;
import bi.fomi.stock.repository.ZoneRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UtilisateurService {

    private final UtilisateurRepository utilisateurRepository;
    private final DepotRepository depotRepository;
    private final ZoneRepository zoneRepository;
    private final ProvinceRepository provinceRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuditLogService auditLogService;

    @Transactional(readOnly = true)
    public List<UserResponse> lister() {
        return utilisateurRepository.findAll().stream().map(this::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public UserResponse getById(Long id) {
        return utilisateurRepository.findById(id)
                .map(this::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable : " + id));
    }

    @Transactional
    public UserResponse creer(UserRequest req) {
        if (utilisateurRepository.existsByUsername(req.username())) {
            throw new BusinessException("Nom d'utilisateur déjà utilisé : " + req.username());
        }
        if (req.password() == null || req.password().isBlank()) {
            throw new BusinessException("Le mot de passe est obligatoire à la création");
        }
        Utilisateur user = Utilisateur.builder()
                .username(req.username())
                .passwordHash(passwordEncoder.encode(req.password()))
                .nomComplet(req.nomComplet())
                .role(req.role())
                .actif(Boolean.TRUE.equals(req.actif()) || req.actif() == null)
                .build();
        appliquerAncrages(req, user);
        user = utilisateurRepository.save(user);
        auditLogService.log("USER_CREATE", "Utilisateur", user.getId(),
                "{\"username\":\"" + user.getUsername() + "\",\"role\":\"" + user.getRole() + "\"}");
        return toResponse(user);
    }

    @Transactional
    public UserResponse modifier(Long id, UserRequest req) {
        Utilisateur user = utilisateurRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable : " + id));
        utilisateurRepository.findByUsername(req.username())
                .filter(existant -> !existant.getId().equals(id))
                .ifPresent(existant -> {
                    throw new BusinessException("Nom d'utilisateur déjà utilisé : " + req.username());
                });
        user.setUsername(req.username());
        if (req.password() != null && !req.password().isBlank()) {
            user.setPasswordHash(passwordEncoder.encode(req.password()));
        }
        user.setNomComplet(req.nomComplet());
        user.setRole(req.role());
        user.setActif(Boolean.TRUE.equals(req.actif()) || req.actif() == null);
        appliquerAncrages(req, user);
        auditLogService.log("USER_UPDATE", "Utilisateur", user.getId(),
                "{\"username\":\"" + user.getUsername() + "\",\"actif\":" + user.getActif() + "}");
        return toResponse(utilisateurRepository.save(user));
    }

    private void appliquerAncrages(UserRequest req, Utilisateur user) {
        Depot depot = req.depotId() != null
                ? depotRepository.findById(req.depotId())
                .orElseThrow(() -> new ResourceNotFoundException("Dépôt introuvable : " + req.depotId()))
                : null;
        Zone zone = req.zoneId() != null
                ? zoneRepository.findById(req.zoneId())
                .orElseThrow(() -> new ResourceNotFoundException("Zone introuvable : " + req.zoneId()))
                : null;
        Province province = req.provinceId() != null
                ? provinceRepository.findById(req.provinceId())
                .orElseThrow(() -> new ResourceNotFoundException("Province introuvable : " + req.provinceId()))
                : null;
        user.setDepot(depot);
        user.setZone(zone);
        user.setProvince(province);
    }

    private UserResponse toResponse(Utilisateur u) {
        return new UserResponse(u.getId(), u.getUsername(), u.getNomComplet(), u.getRole(),
                u.getDepot() != null ? u.getDepot().getId() : null,
                u.getZone() != null ? u.getZone().getId() : null,
                u.getProvince() != null ? u.getProvince().getId() : null,
                u.getActif(), u.getCreatedAt());
    }
}
