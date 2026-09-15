package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class AgriculteurIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerAgriculteursDefautLimiteA50() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("content").size()).isEqualTo(50);
        assertThat(node(result).get("totalElements").asLong()).isGreaterThanOrEqualTo(505);
    }

    @Test
    void listerGrandePageLimiteeA200() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs?size=1000", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("content").size()).isEqualTo(200);
    }

    @Test
    void listerAvecPage() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs?page=0&size=10", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("content").size()).isEqualTo(10);
    }

    @Test
    void listerPageSuivante() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs?page=1&size=10", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("content").size()).isEqualTo(10);
        assertThat(node(result).get("number").asInt()).isEqualTo(1);
    }

    @Test
    void getById() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs/1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode a = node(result);
        assertThat(a.get("numeroIdentite").asText()).isEqualTo("AGR-001");
        assertThat(a.get("nom").asText()).isEqualTo("Ndayisaba");
        assertThat(a.get("prenom").asText()).isEqualTo("Jean");
        assertThat(a.get("telephone").asText()).isEqualTo("79000001");
        assertThat(a.get("collineNom").asText()).isEqualTo("Mutaho");
        assertThat(a.get("estCooperative").asBoolean()).isFalse();
    }

    @Test
    void getByIdInexistant() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs/999999", tokenAdmin());
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void rechercheParTelephone() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs/recherche?telephone=79000001", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("numeroIdentite").asText()).isEqualTo("AGR-001");
    }

    @Test
    void rechercheTelephoneInconnu() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs/recherche?telephone=00000000", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(0);
    }

    @Test
    void creerTelephoneDoublonRefuse() throws Exception {
        MvcResult premier = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-PHONE-01",
                "nom", "Premier",
                "prenom", "A",
                "telephone", "79611111",
                "collineId", 1));
        assertThat(code(premier)).isEqualTo(200);

        MvcResult second = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-PHONE-02",
                "nom", "Second",
                "prenom", "B",
                "telephone", "79611111",
                "collineId", 1));
        assertThat(code(second)).isEqualTo(400);
    }

    @Test
    void rechercheParTelephoneRetourneLesCrees() throws Exception {
        assertThat(code(apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-PHONE-03",
                "nom", "Premier",
                "prenom", "A",
                "telephone", "79622222",
                "collineId", 1)))).isEqualTo(200);

        JsonNode recherche = node(apiGet("/api/agriculteurs/recherche?telephone=79622222", tokenAdmin()));
        assertThat(recherche.size()).isEqualTo(1);
        assertThat(recherche.get(0).get("numeroIdentite").asText()).isEqualTo("AGR-PHONE-03");
    }

    @Test
    void creerAgriculteur() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiPost("/api/agriculteurs", token, Map.of(
                "numeroIdentite", "AGR-NEW-01",
                "nom", "Manirakiza",
                "prenom", "Claude",
                "telephone", "79555555",
                "collineId", 1,
                "estCooperative", false));
        assertThat(code(result)).isEqualTo(200);
        JsonNode created = node(result);
        long id = created.get("id").asLong();
        assertThat(created.get("numeroIdentite").asText()).isEqualTo("AGR-NEW-01");
        assertThat(created.get("nom").asText()).isEqualTo("Manirakiza");

        JsonNode fetched = node(apiGet("/api/agriculteurs/" + id, token));
        assertThat(fetched.get("telephone").asText()).isEqualTo("79555555");
    }

    @Test
    void creerNumeroIdentiteDoublonRefuse() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-001",
                "nom", "Doublon",
                "prenom", "X",
                "collineId", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerCollineInexistante() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-NEW-02",
                "nom", "Test",
                "prenom", "Y",
                "collineId", 999999));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void creerSansNomRefuse() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-NEW-03",
                "prenom", "Y",
                "collineId", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerSansCollineRefuse() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-NEW-04",
                "nom", "Test",
                "prenom", "Y"));
        assertThat(code(result)).isEqualTo(400);
    }
}
