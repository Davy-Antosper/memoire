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
        assertThat(array.size()).isEqualTo(3);
        JsonNode gitega = null;
        for (JsonNode p : array) {
            if ("GIT".equals(p.get("code").asText())) {
                gitega = p;
            }
        }
        assertThat(gitega).isNotNull();
        assertThat(gitega.get("nom").asText()).isEqualTo("Gitega");
    }

    @Test
    void listerZones() throws Exception {
        MvcResult result = apiGet("/api/zones", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(4);
    }

    @Test
    void zonesDuneProvince() throws Exception {
        MvcResult result = apiGet("/api/provinces/1/zones", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(2);
        assertThat(array.get(0).get("provinceNom").asText()).isEqualTo("Gitega");
    }

    @Test
    void listerCollines() throws Exception {
        MvcResult result = apiGet("/api/collines", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(6);
    }

    @Test
    void collinesDuneZone() throws Exception {
        MvcResult result = apiGet("/api/zones/1/collines", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(2);
        assertThat(array.get(0).get("zoneNom").asText()).isEqualTo("Gitega Centre");
    }

    @Test
    void listerEngraisTypesActifs() throws Exception {
        MvcResult result = apiGet("/api/engrais-types", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(3);
        for (JsonNode e : array) {
            assertThat(e.get("actif").asBoolean()).isTrue();
        }
        JsonNode uree = null;
        for (JsonNode e : array) {
            if ("UREE".equals(e.get("code").asText())) {
                uree = e;
            }
        }
        assertThat(uree).isNotNull();
        assertThat(uree.get("prixSubventionne").asDouble()).isEqualTo(25000.0);
        assertThat(uree.get("poidsSacKg").asDouble()).isEqualTo(50.0);
    }

    @Test
    void geoAccessibleParAgent() throws Exception {
        MvcResult result = apiGet("/api/provinces", token("agent.colline"));
        assertThat(code(result)).isEqualTo(200);
    }
}
