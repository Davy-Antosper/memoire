package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MvcResult;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;

class StatsIntegrationTest extends BaseIntegrationTest {

    @Autowired
    private JdbcTemplate jdbc;

    @Test
    void tauxServiceParZone() throws Exception {
        MvcResult result = apiGet("/api/statistiques/taux-service", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);

        JsonNode mutaho = null;
        for (JsonNode z : array) {
            if ("Mutaho".equals(z.get("zoneNom").asText())) {
                mutaho = z;
            }
        }
        assertThat(mutaho).isNotNull();
        assertThat(mutaho.get("commande").asLong()).isEqualTo(8);
        assertThat(mutaho.get("servi").asLong()).isEqualTo(3);
        assertThat(mutaho.get("tauxService").asDouble()).isEqualTo(0.375);
    }

    @Test
    void stocksParProvince() throws Exception {
        MvcResult result = apiGet("/api/statistiques/stocks-par-province", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);

        JsonNode gitega = null;
        JsonNode butanyerera = null;
        for (JsonNode p : array) {
            if ("Gitega".equals(p.get("nom").asText())) {
                gitega = p;
            }
            if ("Butanyerera".equals(p.get("nom").asText())) {
                butanyerera = p;
            }
        }
        assertThat(gitega).isNotNull();
        assertThat(gitega.get("stock").asLong()).isEqualTo(2900);
        assertThat(gitega.get("distribue").asLong()).isEqualTo(0);
        assertThat(gitega.get("reste").asLong()).isEqualTo(2900);

        assertThat(butanyerera).isNotNull();
        assertThat(butanyerera.get("stock").asLong()).isEqualTo(0);
    }

    @Test
    void ruptures() throws Exception {
        MvcResult result = apiGet("/api/statistiques/ruptures", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);

        JsonNode butanyerera = null;
        for (JsonNode r : array) {
            if ("DEP-BUT-P".equals(r.get("depotCode").asText())) {
                butanyerera = r;
            }
        }
        assertThat(butanyerera).isNotNull();
        assertThat(butanyerera.get("depotNom").asText()).isEqualTo("Dépôt logistique provincial Butanyerera");
        assertThat(butanyerera.get("engraisCode").asText()).isEqualTo("IMBURA");
    }

    @Test
    void tauxServiceExclutLesTicketsAnnules() throws Exception {
        jdbc.update("""
                        INSERT INTO ticket (numero_ticket, agriculteur_id, engrais_type_id,
                                            quantite_commandee, quantite_servie, montant_paye,
                                            date_paiement, depot_retrait_id, statut)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ANNULE'::statut_ticket)
                        """,
                "TKT-ANNULE-001", 1L, 1L, 100, 0, new BigDecimal("100000.00"),
                java.sql.Date.valueOf(LocalDate.of(2026, 3, 1)), 6L);

        MvcResult result = apiGet("/api/statistiques/taux-service", tokenAdmin());
        JsonNode array = node(result);

        JsonNode mutaho = null;
        for (JsonNode z : array) {
            if ("Mutaho".equals(z.get("zoneNom").asText())) {
                mutaho = z;
            }
        }
        assertThat(mutaho).isNotNull();
        assertThat(mutaho.get("commande").asLong()).isEqualTo(8);
        assertThat(mutaho.get("servi").asLong()).isEqualTo(3);
        assertThat(mutaho.get("tauxService").asDouble()).isEqualTo(0.375);
    }
}
