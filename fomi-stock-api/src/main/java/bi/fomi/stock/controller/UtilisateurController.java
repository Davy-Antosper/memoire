package bi.fomi.stock.controller;

import bi.fomi.stock.dto.UserRequest;
import bi.fomi.stock.dto.UserResponse;
import bi.fomi.stock.service.UtilisateurService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/utilisateurs")
@RequiredArgsConstructor
public class UtilisateurController {

    private final UtilisateurService utilisateurService;

    @GetMapping
    public List<UserResponse> lister() {
        return utilisateurService.lister();
    }

    @GetMapping("/{id}")
    public UserResponse getById(@PathVariable Long id) {
        return utilisateurService.getById(id);
    }

    @PostMapping
    public UserResponse creer(@Valid @RequestBody UserRequest request) {
        return utilisateurService.creer(request);
    }

    @PutMapping("/{id}")
    public UserResponse modifier(@PathVariable Long id, @Valid @RequestBody UserRequest request) {
        return utilisateurService.modifier(id, request);
    }
}
