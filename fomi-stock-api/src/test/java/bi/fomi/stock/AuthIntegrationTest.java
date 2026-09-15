package bi.fomi.stock;

import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class AuthIntegrationTest extends BaseIntegrationTest {

    @Test
    void loginAdminReussi() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"admin\",\"password\":\"password\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.role").value("ADMIN"))
                .andExpect(jsonPath("$.type").value("Bearer"))
                .andExpect(jsonPath("$.username").value("admin"))
                .andExpect(jsonPath("$.nomComplet").value("Administrateur FOMI"))
                .andExpect(jsonPath("$.token").isNotEmpty());
    }

    @Test
    void loginAgentCollineRetourneSonDepot() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"agent.colline\",\"password\":\"password\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.role").value("AGENT_COLLINE"))
                .andExpect(jsonPath("$.depotId").value(6));
    }

    @Test
    void loginAgentZoneRetourneSaZone() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"agent.zone\",\"password\":\"password\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.role").value("AGENT_ZONE"));
    }

    @Test
    void loginSuperviseurReussi() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"superviseur\",\"password\":\"password\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.role").value("SUPERVISEUR"));
    }

    @Test
    void loginMotDePasseIncorrectRefuse() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"admin\",\"password\":\"mauvais\"}"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.erreur").value("Identifiants invalides"));
    }

    @Test
    void loginUtilisateurInconnuRefuse() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"inconnu\",\"password\":\"password\"}"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void loginChampsVidesRefuse() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"\",\"password\":\"\"}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void accesSansTokenRefuse() throws Exception {
        mvc.perform(get("/api/depots"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void accesTokenInvalideRefuse() throws Exception {
        mvc.perform(get("/api/depots")
                        .header("Authorization", "Bearer token.invalide.123"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void agentCollineInterditStats() throws Exception {
        String token = token("agent.colline");
        mvc.perform(get("/api/statistiques/ruptures").header("Authorization", "Bearer " + token))
                .andExpect(status().isForbidden());
    }

    @Test
    void agentCollineInterditTraiterAlerte() throws Exception {
        String token = token("agent.colline");
        mvc.perform(patch("/api/alertes/1/traiter").header("Authorization", "Bearer " + token))
                .andExpect(status().isForbidden());
    }

    @Test
    void agentCollinePeutLireAlertes() throws Exception {
        String token = token("agent.colline");
        MvcResult result = apiGet("/api/alertes", token);
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void agentZoneInterditStats() throws Exception {
        String token = token("agent.zone");
        MvcResult result = apiGet("/api/statistiques/ruptures", token);
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void agentZoneInterditReception() throws Exception {
        String token = token("agent.zone");
        MvcResult result = apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void agentZonePeutLireAlertes() throws Exception {
        String token = token("agent.zone");
        MvcResult result = apiGet("/api/alertes", token);
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void superviseurPeutLireStats() throws Exception {
        String token = token("superviseur");
        MvcResult result = apiGet("/api/statistiques/ruptures", token);
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void swaggerAccessibleSansToken() throws Exception {
        mvc.perform(get("/api-docs"))
                .andExpect(status().isOk());

        MvcResult ui = mvc.perform(get("/swagger-ui/index.html")).andReturn();
        assertThat(ui.getResponse().getStatus()).isNotEqualTo(401);
    }
}
