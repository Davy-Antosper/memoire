package bi.fomi.stock.service;

import bi.fomi.stock.model.entity.Utilisateur;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public final class SecurityUtils {

    private SecurityUtils() {
    }

    public static Utilisateur currentUser() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof Utilisateur user) {
            return user;
        }
        throw new org.springframework.security.access.AccessDeniedException("Utilisateur non identifié");
    }

    public static Utilisateur currentUserOrNull() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof Utilisateur user) {
            return user;
        }
        return null;
    }
}
