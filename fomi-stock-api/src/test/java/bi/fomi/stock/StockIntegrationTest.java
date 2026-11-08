package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import static org.assertj.core.api.Assertions.assertThat;

class StockIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerTousLesStocks() throws Exception {
        MvcResult result = apiGet("/api/stocks", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(8);
    }

    @Test
    void listerParDepot() throws Exception {
        MvcResult result = apiGet("/api/stocks?depotId=1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(3);
        for (JsonNode s : array) {
            assertThat(s.get("depotId").asLong()).isEqualTo(1);
        }
    }

    @Test
    void listerParEngraisType() throws Exception {
        MvcResult result = apiGet("/api/stocks?engraisTypeId=1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(6);
        for (JsonNode s : array) {
            assertThat(s.get("engraisTypeId").asLong()).isEqualTo(1);
            assertThat(s.get("engraisCode").asText()).isEqualTo("IMBURA");
        }
    }

    @Test
    void listerDisponibles() throws Exception {
        MvcResult result = apiGet("/api/stocks/disponibles?engraisTypeId=1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(5);
        for (JsonNode s : array) {
            assertThat(s.get("quantiteDisponible").asInt()).isGreaterThan(0);
        }
    }

    @Test
    void listerDisponiblesSansStock() throws Exception {
        MvcResult result = apiGet("/api/stocks/disponibles?engraisTypeId=3", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(0);
    }

    @Test
    void stockContientMetadonnees() throws Exception {
        MvcResult result = apiGet("/api/stocks?depotId=3", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode s = node(result).get(0);
        assertThat(s.get("quantiteDisponible").asInt()).isEqualTo(0);
        // Le seuil affiché est celui du couple dépôt + produit (seuil_alerte),
        // et non le seuil générique du dépôt (200).
        assertThat(s.get("seuilAlerteMin").asInt()).isEqualTo(150);
        assertThat(s.get("depotCode").asText()).isEqualTo("DEP-BUT-P");
    }
}
