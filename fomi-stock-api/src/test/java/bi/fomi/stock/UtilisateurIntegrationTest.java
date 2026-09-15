package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.LinkedHashMap;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class UtilisateurIntegrationTest extends BaseIntegrationTest {

    private long creerUtilisateur(String username, String role, Map<String, Object> extra) throws Exception {
        Map<String, Object> corps = new LinkedHashMap<>();
        corps.put("username", username);
        corps.put("password", "secret123");
        corps.put("nomComplet", "Nouvel Agent " + username);
        corps.put("role", role);
        corps.putAll(extra);
        MvcResult result = apiPost("/api/utilisateurs", tokenAdmin(), corps);
        assertThat(code(result)).isEqualTo(200);
        return node(result).get("id").asLong();
    }

    @Test
    void listerUtilisateurs() throws Exception {
        MvcResult result = apiGet("/api/utilisateurs", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isGreaterThanOrEqualTo(4);
        boolean adminPresent = false;
        for (JsonNode u : array) {
            if ("admin".equals(u.get("username").asText())) {
                adminPresent = true;
                assertThat(u.get("role").asText()).isEqualTo("ADMIN");
            }
        }
        assertThat(adminPresent).isTrue();
    }

    @Test
    void getById() throws Exception {
        long id = creerUtilisateur("agent.a", "AGENT_COLLINE", Map.of("depotId", 6L));
        JsonNode u = node(apiGet("/api/utilisateurs/" + id, tokenAdmin()));
        assertThat(u.get("username").asText()).isEqualTo("agent.a");
        assertThat(u.get("role").asText()).isEqualTo("AGENT_COLLINE");
        assertThat(u.get("depotId").asLong()).isEqualTo(6);
        assertThat(u.get("actif").asBoolean()).isTrue();
    }

    @Test
    void getByIdInexistant() throws Exception {
        MvcResult result = apiGet("/api/utilisateurs/999999", tokenAdmin());
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void creerUtilisateurPuisLogin() throws Exception {
        long id = creerUtilisateur("agent.nouveau", "AGENT_ZONE", Map.of("zoneId", 1L));
        assertThat(id).isGreaterThan(0);

        MvcResult connexion = login("agent.nouveau", "secret123");
        assertThat(code(connexion)).isEqualTo(200);
        String token = node(connexion).get("token").asText();
        MvcResult acces = apiGet("/api/alertes", token);
        assertThat(code(acces)).isEqualTo(200);
    }

    @Test
    void creerUsernameDoublonRefuse() throws Exception {
        creerUtilisateur("agent.b", "AGENT_COLLINE", Map.of("depotId", 6L));
        MvcResult result = apiPost("/api/utilisateurs", tokenAdmin(), Map.of(
                "username", "agent.b",
                "password", "secret123",
                "nomComplet", "Doublon",
                "role", "AGENT_COLLINE",
                "depotId", 6L));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerSansMotDePasseRefuse() throws Exception {
        MvcResult result = apiPost("/api/utilisateurs", tokenAdmin(), Map.of(
                "username", "agent.c",
                "nomComplet", "Sans mot de passe",
                "role", "ADMIN"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerDepotInexistantRefuse() throws Exception {
        MvcResult result = apiPost("/api/utilisateurs", tokenAdmin(), Map.of(
                "username", "agent.d",
                "password", "secret123",
                "nomComplet", "Mauvais dépôt",
                "role", "AGENT_COLLINE",
                "depotId", 999999L));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void nonAdminInterditCRUD() throws Exception {
        String token = token("agent.zone");
        MvcResult liste = apiGet("/api/utilisateurs", token);
        assertThat(code(liste)).isEqualTo(403);
        MvcResult creation = apiPost("/api/utilisateurs", token, Map.of(
                "username", "intrus",
                "password", "secret123",
                "nomComplet", "Intrus",
                "role", "ADMIN"));
        assertThat(code(creation)).isEqualTo(403);
    }

    @Test
    void modifierUtilisateur() throws Exception {
        long id = creerUtilisateur("agent.e", "AGENT_COLLINE", Map.of("depotId", 6L));

        Map<String, Object> corps = new LinkedHashMap<>();
        corps.put("username", "agent.e");
        corps.put("nomComplet", "Agent Renommé");
        corps.put("role", "AGENT_ZONE");
        corps.put("zoneId", 1L);
        corps.put("actif", false);
        MvcResult result = apiPut("/api/utilisateurs/" + id, tokenAdmin(), corps);
        assertThat(code(result)).isEqualTo(200);
        JsonNode u = node(result);
        assertThat(u.get("nomComplet").asText()).isEqualTo("Agent Renommé");
        assertThat(u.get("role").asText()).isEqualTo("AGENT_ZONE");
        assertThat(u.get("actif").asBoolean()).isFalse();
    }

    @Test
    void modifierUsernameDoublonRefuse() throws Exception {
        long id = creerUtilisateur("agent.f", "AGENT_COLLINE", Map.of("depotId", 6L));

        Map<String, Object> corps = new LinkedHashMap<>();
        corps.put("username", "agent.zone");
        corps.put("nomComplet", "Doublon");
        corps.put("role", "AGENT_COLLINE");
        MvcResult result = apiPut("/api/utilisateurs/" + id, tokenAdmin(), corps);
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void utilisateurDesactiveNePeutPlusSeConnecter() throws Exception {
        long id = creerUtilisateur("agent.g", "AGENT_COLLINE", Map.of("depotId", 6L));
        assertThat(code(login("agent.g", "secret123"))).isEqualTo(200);

        Map<String, Object> corps = new LinkedHashMap<>();
        corps.put("username", "agent.g");
        corps.put("nomComplet", "Désactivé");
        corps.put("role", "AGENT_COLLINE");
        corps.put("actif", false);
        assertThat(code(apiPut("/api/utilisateurs/" + id, tokenAdmin(), corps))).isEqualTo(200);

        assertThat(code(login("agent.g", "secret123"))).isEqualTo(401);
    }
}
