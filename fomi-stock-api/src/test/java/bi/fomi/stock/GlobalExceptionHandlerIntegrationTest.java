package bi.fomi.stock;

import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class GlobalExceptionHandlerIntegrationTest extends BaseIntegrationTest {

    @Test
    void corpsJsonIllisibleRenvoie400() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{invalid-json"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.erreur").value("Corps de requête invalide ou illisible"));
    }

    @Test
    void typeIncompatibleRenvoie400() throws Exception {
        mvc.perform(get("/api/tickets/{id}", "abc").header("Authorization", "Bearer " + tokenAdmin()))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.erreur").value("Paramètre 'id' : valeur invalide (abc)"));
    }

    @Test
    void parametreRequisManquantRenvoie400() throws Exception {
        mvc.perform(get("/api/agriculteurs/recherche").header("Authorization", "Bearer " + tokenAdmin()))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.erreur").value("Paramètre requis manquant : telephone"));
    }

    @Test
    void routeInexistanteRenvoie404() throws Exception {
        mvc.perform(get("/route-inexistante").header("Authorization", "Bearer " + tokenAdmin()))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.erreur").value("Ressource introuvable"));
    }

    @Test
    void methodeHttpNonSupporteRenvoie405() throws Exception {
        mvc.perform(get("/api/auth/login"))
                .andExpect(status().isMethodNotAllowed())
                .andExpect(jsonPath("$.erreur").value("Méthode HTTP non autorisée : GET"));
    }
}
