package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class DepotIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerDepots() throws Exception {
        MvcResult result = apiGet("/api/depots", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(9);
    }

    @Test
    void getById() throws Exception {
        MvcResult result = apiGet("/api/depots/1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode d = node(result);
        assertThat(d.get("code").asText()).isEqualTo("DEP-GIT-P");
        assertThat(d.get("nom").asText()).isEqualTo("Dépôt logistique provincial Gitega");
        assertThat(d.get("niveau").asText()).isEqualTo("PROVINCE");
        assertThat(d.get("provinceNom").asText()).isEqualTo("Gitega");
        assertThat(d.get("seuilAlerteMin").asInt()).isEqualTo(500);
        assertThat(d.get("actif").asBoolean()).isTrue();
    }

    @Test
    void getByIdInexistant() throws Exception {
        MvcResult result = apiGet("/api/depots/999999", tokenAdmin());
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void stockDuDepot() throws Exception {
        MvcResult result = apiGet("/api/depots/1/stock", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(3);
        for (JsonNode s : array) {
            if ("IMBURA".equals(s.get("engraisCode").asText())) {
                assertThat(s.get("quantiteDisponible").asInt()).isEqualTo(1500);
            }
            if ("TOTAHAZA".equals(s.get("engraisCode").asText())) {
                assertThat(s.get("quantiteDisponible").asInt()).isEqualTo(800);
            }
            if ("DOLOMIE".equals(s.get("engraisCode").asText())) {
                assertThat(s.get("quantiteDisponible").asInt()).isEqualTo(120);
            }
        }
    }

    @Test
    void stockDepotInexistant() throws Exception {
        MvcResult result = apiGet("/api/depots/999999/stock", tokenAdmin());
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void creerDepotProvince() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-NEW-P",
                "nom", "Nouveau Provincial",
                "niveau", "PROVINCE",
                "provinceId", 2,
                "seuilAlerteMin", 250));
        assertThat(code(result)).isEqualTo(200);
        JsonNode d = node(result);
        assertThat(d.get("code").asText()).isEqualTo("DEP-NEW-P");
        assertThat(d.get("niveau").asText()).isEqualTo("PROVINCE");
        assertThat(d.get("provinceNom").asText()).isEqualTo("Bujumbura");
        assertThat(d.get("seuilAlerteMin").asInt()).isEqualTo(250);
    }

    @Test
    void creerDepotZone() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-NEW-Z",
                "nom", "Nouveau Zone",
                "niveau", "ZONE",
                "zoneId", 1));
        assertThat(code(result)).isEqualTo(200);
        JsonNode d = node(result);
        assertThat(d.get("niveau").asText()).isEqualTo("ZONE");
        assertThat(d.get("zoneNom").asText()).isEqualTo("Buhevyi");
        assertThat(d.get("communeNom").asText()).isEqualTo("Gitega");
        assertThat(d.get("provinceNom").asText()).isEqualTo("Gitega");
    }

    @Test
    void creerDepotCollineRefuse() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-NEW-C",
                "nom", "Nouveau Colline",
                "niveau", "COLLINE",
                "collineId", 3));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerProvinceSansAncrageRefuse() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-NEW-X",
                "nom", "Sans ancrage",
                "niveau", "PROVINCE"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerCodeDoublonRefuse() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-GIT-P",
                "nom", "Doublon",
                "niveau", "PROVINCE",
                "provinceId", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerSansNomRefuse() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-NEW-Y",
                "niveau", "PROVINCE",
                "provinceId", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void modifierDepot() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiPut("/api/depots/9", token, Map.of(
                "code", "DEP-MIV",
                "nom", "Dépôt de distribution Mivo (modifié)",
                "niveau", "ZONE",
                "zoneId", 4,
                "seuilAlerteMin", 75));
        assertThat(code(result)).isEqualTo(200);
        JsonNode d = node(result);
        assertThat(d.get("nom").asText()).isEqualTo("Dépôt de distribution Mivo (modifié)");
        assertThat(d.get("seuilAlerteMin").asInt()).isEqualTo(75);
        assertThat(d.get("zoneNom").asText()).isEqualTo("Mivo");
        assertThat(d.get("communeNom").asText()).isEqualTo("Ngozi");
    }

    @Test
    void modifierCodeDoublonRefuse() throws Exception {
        MvcResult result = apiPut("/api/depots/9", tokenAdmin(), Map.of(
                "code", "DEP-GIT-P",
                "nom", "Doublon",
                "niveau", "ZONE",
                "zoneId", 4));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void modifierInexistant() throws Exception {
        MvcResult result = apiPut("/api/depots/999999", tokenAdmin(), Map.of(
                "code", "DEP-XX",
                "nom", "X",
                "niveau", "PROVINCE",
                "provinceId", 1));
        assertThat(code(result)).isEqualTo(404);
    }
}
