package bi.fomi.stock.config;

import com.zaxxer.hikari.HikariDataSource;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class DatabaseUrlConfigTest {

    private final DatabaseUrlConfig config = new DatabaseUrlConfig();

    @Test
    void convertitUrlPostgresql() {
        HikariDataSource ds = (HikariDataSource) config.dataSourceFromDatabaseUrl(
                "postgresql://fomi:secret@postgres.railway.internal:5432/railway");
        assertThat(ds.getJdbcUrl()).isEqualTo("jdbc:postgresql://postgres.railway.internal:5432/railway");
        assertThat(ds.getUsername()).isEqualTo("fomi");
        assertThat(ds.getPassword()).isEqualTo("secret");
    }

    @Test
    void accepteSchemePostgres() {
        HikariDataSource ds = (HikariDataSource) config.dataSourceFromDatabaseUrl(
                "postgres://user:pass@host.example:5432/mydb");
        assertThat(ds.getJdbcUrl()).isEqualTo("jdbc:postgresql://host.example:5432/mydb");
        assertThat(ds.getUsername()).isEqualTo("user");
        assertThat(ds.getPassword()).isEqualTo("pass");
    }

    @Test
    void decodeMotDePasseUrlEncode() {
        HikariDataSource ds = (HikariDataSource) config.dataSourceFromDatabaseUrl(
                "postgresql://fomi:p%40ss%2Fword@host:5432/db");
        assertThat(ds.getJdbcUrl()).isEqualTo("jdbc:postgresql://host:5432/db");
        assertThat(ds.getUsername()).isEqualTo("fomi");
        assertThat(ds.getPassword()).isEqualTo("p@ss/word");
    }
}
