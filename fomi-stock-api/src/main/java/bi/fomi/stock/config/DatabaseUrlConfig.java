package bi.fomi.stock.config;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

@Configuration
public class DatabaseUrlConfig {

    @Bean
    @Primary
    @ConditionalOnProperty(name = "DATABASE_URL")
    public DataSource dataSourceFromDatabaseUrl(@Value("${DATABASE_URL}") String databaseUrl) {
        String rest = databaseUrl;
        if (rest.startsWith("postgresql://")) {
            rest = rest.substring("postgresql://".length());
        } else if (rest.startsWith("postgres://")) {
            rest = rest.substring("postgres://".length());
        }
        int slash = rest.indexOf('/');
        String authority = slash >= 0 ? rest.substring(0, slash) : rest;
        String dbPath = slash >= 0 ? rest.substring(slash) : "";
        int at = authority.lastIndexOf('@');
        String userInfo = at >= 0 ? authority.substring(0, at) : "";
        String hostPort = at >= 0 ? authority.substring(at + 1) : authority;
        int colonUser = userInfo.indexOf(':');
        String username = URLDecoder.decode(
                colonUser >= 0 ? userInfo.substring(0, colonUser) : userInfo, StandardCharsets.UTF_8);
        String password = colonUser >= 0
                ? URLDecoder.decode(userInfo.substring(colonUser + 1), StandardCharsets.UTF_8)
                : "";
        String jdbcUrl = "jdbc:postgresql://" + hostPort + dbPath;
        return DataSourceBuilder.create()
                .url(jdbcUrl)
                .username(username)
                .password(password)
                .build();
    }
}
