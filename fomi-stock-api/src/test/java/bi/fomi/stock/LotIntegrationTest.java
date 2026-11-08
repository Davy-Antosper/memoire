package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpHeaders;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class LotIntegrationTest extends BaseIntegrationTest {

    @Test
    void listeLesLotsSansAuthNecessaire() throws Exception {
        mvc.perform(get("/api/lots").header(HttpHeaders.AUTHORIZATION, "Bearer " + tokenAdmin()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$[0].numeroLot").isNotEmpty())
                .andExpect(jsonPath("$[0].engraisTypeCode").isNotEmpty());
    }

    @Test
    void filtreParTypeEngrais() throws Exception {
        mvc.perform(get("/api/lots").param("engraisTypeId", "1")
                        .header(HttpHeaders.AUTHORIZATION, "Bearer " + tokenAdmin()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray());
    }

    @Test
    void rechercheParNumero() throws Exception {
        mvc.perform(get("/api/lots/recherche").param("numero", "LOT-IMBURA")
                        .header(HttpHeaders.AUTHORIZATION, "Bearer " + tokenAdmin()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].numeroLot").value("LOT-IMBURA-2026-001"));
    }

    @Test
    void adminCreeUnLot() throws Exception {
        MvcResult result = apiPost("/api/lots", tokenAdmin(), Map.of(
                "numeroLot", "LOT-UREE-2026-002",
                "engraisTypeId", 2,
                "quantiteInitiale", 1000,
                "dateFabrication", "2026-07-01",
                "datePeremption", "2027-07-01"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode lot = node(result);
        assertThat(lot.get("numeroLot").asText()).isEqualTo("LOT-UREE-2026-002");
        assertThat(lot.get("engraisTypeCode").asText()).isEqualTo("UREE");
    }

    @Test
    void numeroLotDupliqueRefuse() throws Exception {
        MvcResult result = apiPost("/api/lots", tokenAdmin(), Map.of(
                "numeroLot", "LOT-IMBURA-2026-001",
                "engraisTypeId", 1,
                "quantiteInitiale", 100));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void agentCollineNePeutPasCreerDeLot() throws Exception {
        MvcResult result = apiPost("/api/lots", token("agent.colline"), Map.of(
                "numeroLot", "LOT-NPK-2026-003",
                "engraisTypeId", 2,
                "quantiteInitiale", 100));
        assertThat(code(result)).isEqualTo(403);
    }
}
