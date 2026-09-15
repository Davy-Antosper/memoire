package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.testcontainers.containers.PostgreSQLContainer;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@AutoConfigureMockMvc
class StockConcurrenceIntegrationTest {

    static final PostgreSQLContainer<?> POSTGRES = BaseIntegrationTest.POSTGRES;

    @DynamicPropertySource
    static void properties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", POSTGRES::getJdbcUrl);
        registry.add("spring.datasource.username", POSTGRES::getUsername);
        registry.add("spring.datasource.password", POSTGRES::getPassword);
    }

    @Autowired
    private MockMvc mvc;

    @Autowired
    private JdbcTemplate jdbc;

    private final List<String> numerosCrees = new ArrayList<>();
    private long ticketId;
    private int stockAvant;
    private int stockLotAvant;

    @AfterEach
    void restaurer() {
        for (String numero : numerosCrees) {
            try {
                Long id = jdbc.queryForObject(
                        "SELECT id FROM ticket WHERE numero_ticket = ?", Long.class, numero);
                if (id == null) {
                    continue;
                }
                jdbc.update("DELETE FROM distribution WHERE ticket_id = ?", id);
                jdbc.update("DELETE FROM mouvement WHERE ticket_id = ?", id);
                jdbc.update("DELETE FROM audit_log WHERE entity_type = 'Ticket' AND entity_id = ?", id);
                jdbc.update("DELETE FROM ticket WHERE id = ?", id);
            } catch (org.springframework.dao.EmptyResultDataAccessException ignored) {
                // ticket non créé : rien à nettoyer
            }
        }
        jdbc.update("DELETE FROM alerte WHERE depot_id = 1 AND engrais_type_id = 1 AND type <> 'RUPTURE'");
        jdbc.update("UPDATE stock SET quantite_disponible = ? WHERE depot_id = 1 AND engrais_type_id = 1", stockAvant);
        jdbc.update("UPDATE stock_lot SET quantite = ? WHERE depot_id = 1 AND lot_id = 1", stockLotAvant);
    }

    @Test
    void distributionsSimultaneesNeSurvendentPas() throws Exception {
        stockAvant = jdbc.queryForObject(
                "SELECT quantite_disponible FROM stock WHERE depot_id = 1 AND engrais_type_id = 1", Integer.class);
        stockLotAvant = jdbc.queryForObject(
                "SELECT quantite FROM stock_lot WHERE depot_id = 1 AND lot_id = 1", Integer.class);

        String token = login();
        ticketId = creerTicket(token, "TKT-CONC-001", 500);

        int threads = 20;
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        CountDownLatch depart = new CountDownLatch(1);
        List<Future<MvcResult>> resultats = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            resultats.add(pool.submit(() -> {
                depart.await();
                return distribuer(token, ticketId, 5);
            }));
        }
        depart.countDown();
        pool.shutdown();
        assertThat(pool.awaitTermination(60, TimeUnit.SECONDS)).isTrue();

        int reussies = 0;
        for (Future<MvcResult> future : resultats) {
            if (future.get().getResponse().getStatus() == 200) {
                reussies++;
            }
        }
        assertThat(reussies).as("les 20 distributions simultanées doivent réussir").isEqualTo(threads);

        JsonNode ticket = om(apiGet("/api/tickets/" + ticketId, token));
        assertThat(ticket.get("quantiteServie").asInt())
                .as("aucune mise à jour perdue sur le ticket malgré la concurrence")
                .isEqualTo(100);

        JsonNode stocks = om(apiGet("/api/depots/1/stock", token));
        long uree = -1;
        for (JsonNode s : stocks) {
            if ("UREE".equals(s.get("engraisCode").asText())) {
                uree = s.get("quantiteDisponible").asLong();
            }
        }
        assertThat(uree).as("le stock doit refléter exactement 100 sacs sortis").isEqualTo(stockAvant - 100);
    }

    private String login() throws Exception {
        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                .post("/api/auth/login")
                .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                .content("{\"username\":\"admin\",\"password\":\"password\"}")).andReturn();
        return om(result).get("token").asText();
    }

    private long creerTicket(String token, String numero, int quantite) throws Exception {
        numerosCrees.add(numero);
        MvcResult result = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", numero,
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", quantite,
                "montantPaye", quantite * 25000L,
                "datePaiement", "2026-04-01",
                "depotRetraitId", 1,
                "saison", "2026A"));
        assertThat(result.getResponse().getStatus()).isEqualTo(200);
        long id = om(result).get("id").asLong();
        MvcResult activate = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                .patch("/api/tickets/" + id + "/activer")
                .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token)).andReturn();
        assertThat(activate.getResponse().getStatus()).isEqualTo(200);
        return id;
    }

    private MvcResult distribuer(String token, long ticketId, int quantite) throws Exception {
        return apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", quantite));
    }

    private MvcResult apiPost(String url, String token, Object body) throws Exception {
        return mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .post(url)
                        .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token)
                        .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                        .content(new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(body)))
                .andReturn();
    }

    private MvcResult apiGet(String url, String token) throws Exception {
        return mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get(url)
                        .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .andReturn();
    }

    private JsonNode om(MvcResult result) throws Exception {
        return new com.fasterxml.jackson.databind.ObjectMapper().readTree(
                new String(result.getResponse().getContentAsByteArray(), java.nio.charset.StandardCharsets.UTF_8));
    }
}
