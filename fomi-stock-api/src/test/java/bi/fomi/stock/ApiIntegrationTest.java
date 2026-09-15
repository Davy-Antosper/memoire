package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@AutoConfigureMockMvc
class ApiIntegrationTest extends BaseIntegrationTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper om;

    private String login(String username) throws Exception {
        MvcResult result = mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"" + username + "\",\"password\":\"password\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").isNotEmpty())
                .andReturn();
        return om.readTree(result.getResponse().getContentAsString()).get("token").asText();
    }

    @Test
    void loginAdminReussi() throws Exception {
        MvcResult result = mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"admin\",\"password\":\"password\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.role").value("ADMIN"))
                .andReturn();
        JsonNode body = om.readTree(result.getResponse().getContentAsString());
        assertThat(body.get("token").asText()).isNotBlank();
    }

    @Test
    void loginMotDePasseErroneRefuse() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"admin\",\"password\":\"mauvais\"}"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void accesSansTokenRefuse() throws Exception {
        mvc.perform(get("/api/depots"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void endpointSantePublic() throws Exception {
        mvc.perform(get("/actuator/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test
    void distributionCompleteLeTicket() throws Exception {
        String token = login("agent.colline");
        mvc.perform(post("/api/distributions")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"ticketId\":1,\"depotId\":6,\"quantite\":2}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].ticketNumero").value("TKT-2026-1247"));

        mvc.perform(get("/api/tickets/1").header("Authorization", "Bearer " + login("admin")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.statut").value("SERVI"))
                .andExpect(jsonPath("$.quantiteServie").value(5));
    }

    @Test
    void agentCollineLimiteASonDepot() throws Exception {
        String token = login("agent.colline");
        mvc.perform(post("/api/distributions")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"ticketId\":2,\"depotId\":7,\"quantite\":1}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void distributionQuantiteSuperieureAuRestantRefusee() throws Exception {
        String token = login("agent.colline");
        mvc.perform(post("/api/distributions")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"ticketId\":2,\"depotId\":6,\"quantite\":999}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void superviseurLitLesStatsMaisPasLesEcritures() throws Exception {
        String token = login("superviseur");
        mvc.perform(get("/api/statistiques/ruptures").header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray());

        mvc.perform(post("/api/mouvements/reception")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"lotId\":1,\"depotDestId\":2,\"quantite\":10}"))
                .andExpect(status().isForbidden());
    }

    @Test
    void transfertMetAJourLesStocks() throws Exception {
        String token = login("admin");
        mvc.perform(post("/api/mouvements/transfert")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"lotId\":1,\"depotSourceId\":1,\"depotDestId\":5,\"quantite\":100}"))
                .andExpect(status().isOk());

        mvc.perform(get("/api/depots/5/stock").header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].quantiteDisponible").value(100));
    }
}
