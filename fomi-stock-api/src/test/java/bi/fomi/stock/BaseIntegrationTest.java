package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.transaction.annotation.Transactional;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;

import java.nio.charset.StandardCharsets;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
public abstract class BaseIntegrationTest {

    /**
     * Par défaut les tests démarrent un conteneur PostgreSQL (Testcontainers).
     * En l'absence de Docker, il est possible de pointer vers une base locale
     * déjà créée avec {@code -Dfomi.test.localdb=true} ou
     * {@code FOMI_TEST_LOCALDB=true}, en surchargeant au besoin
     * {@code fomi.test.db.url}, {@code fomi.test.db.username} et
     * {@code fomi.test.db.password}.
     */
    static final boolean LOCAL_DB = Boolean.getBoolean("fomi.test.localdb")
            || "true".equalsIgnoreCase(System.getenv("FOMI_TEST_LOCALDB"));

    static final PostgreSQLContainer<?> POSTGRES = LOCAL_DB ? null : new PostgreSQLContainer<>(
            DockerImageName.parse("postgres:16-alpine"))
            .withDatabaseName("fomi_test")
            .withUsername("fomi")
            .withPassword("fomi123");

    static {
        if (POSTGRES != null) {
            POSTGRES.start();
            Runtime.getRuntime().addShutdownHook(new Thread(POSTGRES::stop));
        }
    }

    @DynamicPropertySource
    static void properties(DynamicPropertyRegistry registry) {
        if (POSTGRES == null) {
            registry.add("spring.datasource.url", () -> System.getProperty("fomi.test.db.url",
                    "jdbc:postgresql://localhost:5432/fomi_test"));
            registry.add("spring.datasource.username", () -> System.getProperty("fomi.test.db.username", "fomi"));
            registry.add("spring.datasource.password", () -> System.getProperty("fomi.test.db.password", "fomi123"));
        } else {
            registry.add("spring.datasource.url", POSTGRES::getJdbcUrl);
            registry.add("spring.datasource.username", POSTGRES::getUsername);
            registry.add("spring.datasource.password", POSTGRES::getPassword);
        }
    }

    @Autowired
    protected MockMvc mvc;

    @Autowired
    protected ObjectMapper om;

    protected String token(String username) throws Exception {
        MvcResult result = login(username, "password");
        return om.readTree(new String(result.getResponse().getContentAsByteArray(), StandardCharsets.UTF_8))
                .get("token").asText();
    }

    protected MvcResult login(String username, String password) throws Exception {
        return mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}"))
                .andReturn();
    }

    protected String tokenAdmin() throws Exception {
        return token("admin");
    }

    protected MvcResult apiGet(String url, String token) throws Exception {
        return mvc.perform(get(url).header(HttpHeaders.AUTHORIZATION, "Bearer " + token)).andReturn();
    }

    protected MvcResult apiPost(String url, String token, Object body) throws Exception {
        return apiSend(post(url), token, body);
    }

    protected MvcResult apiPut(String url, String token, Object body) throws Exception {
        return apiSend(put(url), token, body);
    }

    protected MvcResult apiPatch(String url, String token) throws Exception {
        return mvc.perform(patch(url).header(HttpHeaders.AUTHORIZATION, "Bearer " + token)).andReturn();
    }

    protected MvcResult apiPatch(String url, String token, Object body) throws Exception {
        return apiSend(patch(url), token, body);
    }

    protected long creerTicketActif(String token, String numero, int quantite, long depotId) throws Exception {
        MvcResult created = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", numero,
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", quantite,
                "montantPaye", quantite * 31000L,
                "datePaiement", "2026-03-15",
                "depotRetraitId", depotId,
                "saison", "2026A"));
        long id = node(created).get("id").asLong();
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);
        return id;
    }

    private MvcResult apiSend(MockHttpServletRequestBuilder builder, String token, Object body) throws Exception {
        return mvc.perform(builder
                        .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json(body)))
                .andReturn();
    }

    protected String json(Object body) throws Exception {
        return om.writeValueAsString(body);
    }

    protected JsonNode node(MvcResult result) throws Exception {
        return om.readTree(content(result));
    }

    protected String content(MvcResult result) {
        return new String(result.getResponse().getContentAsByteArray(), StandardCharsets.UTF_8);
    }

    protected int code(MvcResult result) {
        return result.getResponse().getStatus();
    }

    protected long stockDepot(String token, long depotId, String engraisCode) throws Exception {
        JsonNode array = node(apiGet("/api/depots/" + depotId + "/stock", token));
        for (JsonNode s : array) {
            if (engraisCode.equals(s.get("engraisCode").asText())) {
                return s.get("quantiteDisponible").asLong();
            }
        }
        return -1;
    }
}
