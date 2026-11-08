package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import static org.assertj.core.api.Assertions.assertThat;

class GeoIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerProvinces() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiGet("/api/provinces", token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(5);
        JsonNode gitega = null;
        for (JsonNode p : array) {
            if ("GIT".equals(p.get("code").asText())) {
                gitega = p;
            }
        }
        assertThat(gitega).isNotNull();
        assertThat(gitega.get("nom").asText()).isEqualTo("Gitega");

        MvcResult communes = apiGet("/api/communes", token);
        assertThat(code(communes)).isEqualTo(200);
        JsonNode communesArray = node(communes);
        assertThat(communesArray.size()).isEqualTo(42);
        boolean gitegaCommune = false;
        for (JsonNode c : communesArray) {
            if ("GIT-CO-GITEGA".equals(c.get("code").asText())) {
                gitegaCommune = true;
                assertThat(c.get("provinceNom").asText()).isEqualTo("Gitega");
            }
        }
        assertThat(gitegaCommune).isTrue();
    }

    @Test
    void listerZones() throws Exception {
        MvcResult result = apiGet("/api/zones", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(39);
        assertThat(array.get(0).get("communeNom").asText()).isNotBlank();
        assertThat(array.get(0).get("provinceNom").asText()).isNotBlank();
    }

    @Test
    void zonesDuneProvince() throws Exception {
        MvcResult result = apiGet("/api/provinces/1/zones", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(19);
        assertThat(array.get(0).get("provinceNom").asText()).isEqualTo("Gitega");

        MvcResult communes = apiGet("/api/provinces/1/communes", tokenAdmin());
        assertThat(code(communes)).isEqualTo(200);
        JsonNode communesArray = node(communes);
        assertThat(communesArray.size()).isEqualTo(9);
        // Toutes les communes ne disposent pas encore de zones saisies :
        // on cible la commune de Gitega, qui en compte 12 dans le référentiel.
        long communeId = -1;
        for (JsonNode c : communesArray) {
            if ("Gitega".equals(c.get("nom").asText())) {
                communeId = c.get("id").asLong();
            }
        }
        assertThat(communeId).isPositive();

        MvcResult zonesOfCommune = apiGet("/api/communes/" + communeId + "/zones", tokenAdmin());
        assertThat(code(zonesOfCommune)).isEqualTo(200);
        assertThat(node(zonesOfCommune).size()).isGreaterThanOrEqualTo(1);
    }

    @Test
    void listerCollines() throws Exception {
        MvcResult result = apiGet("/api/collines", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(73);
    }

    @Test
    void collinesDuneZone() throws Exception {
        MvcResult result = apiGet("/api/zones/1/collines", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(5);
        assertThat(array.get(0).get("zoneNom").asText()).isEqualTo("Buhevyi");
    }

    @Test
    void listerEngraisTypesActifs() throws Exception {
        MvcResult result = apiGet("/api/engrais-types", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(4);
        for (JsonNode e : array) {
            assertThat(e.get("actif").asBoolean()).isTrue();
        }
        JsonNode imbura = null;
        for (JsonNode e : array) {
            if ("IMBURA".equals(e.get("code").asText())) {
                imbura = e;
            }
        }
        assertThat(imbura).isNotNull();
        assertThat(imbura.get("prixSubventionne").asDouble()).isEqualTo(31000.0);
        assertThat(imbura.get("poidsSacKg").asDouble()).isEqualTo(25.0);
        assertThat(imbura.get("prixAConfirmer").asBoolean()).isFalse();
    }

    @Test
    void geoAccessibleParAgent() throws Exception {
        MvcResult result = apiGet("/api/provinces", token("agent.colline"));
        assertThat(code(result)).isEqualTo(200);
    }
}
