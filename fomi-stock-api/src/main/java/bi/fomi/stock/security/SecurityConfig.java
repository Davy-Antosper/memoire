package bi.fomi.stock.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;
import java.util.Map;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthFilter jwtAuthFilter;
    private final ObjectMapper objectMapper;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .cors(cors -> cors.configurationSource(corsConfigurationSource()))
                .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/auth/login").permitAll()
                        .requestMatchers("/actuator/health").permitAll()
                        .requestMatchers("/api-docs/**", "/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html",
                                "/swagger-resources/**").permitAll()
                        .requestMatchers("/api/public/**").permitAll()
                        .requestMatchers(HttpMethod.GET, "/api/statistiques/**").hasAnyRole("ADMIN", "SUPERVISEUR")
                        .requestMatchers(HttpMethod.GET, "/api/alertes/**").hasAnyRole("ADMIN", "SUPERVISEUR",
                                "AGENT_ZONE", "AGENT_COLLINE")
                        .requestMatchers("/api/alertes/**").hasRole("ADMIN")
                        .requestMatchers("/api/utilisateurs/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.GET, "/api/audit-logs/**").hasRole("ADMIN")
                        .requestMatchers("/api/mouvements/reception").hasAnyRole("ADMIN", "AGENT_LOGISTIQUE")
                        .requestMatchers(HttpMethod.POST, "/api/mouvements/transfert").hasRole("ADMIN")
                        .requestMatchers("/api/mouvements/**").authenticated()
                        .requestMatchers(HttpMethod.PUT, "/api/tickets/**").hasAnyRole("ADMIN", "AGENT_ZONE")
                        .requestMatchers(HttpMethod.PATCH, "/api/tickets/*/activer")
                        .hasAnyRole("ADMIN", "SUPERVISEUR")
                        .requestMatchers(HttpMethod.PATCH, "/api/tickets/*/rejeter")
                        .hasAnyRole("ADMIN", "SUPERVISEUR")
                        .requestMatchers(HttpMethod.POST, "/api/lots/**").hasAnyRole("ADMIN", "AGENT_LOGISTIQUE")
                        .requestMatchers(HttpMethod.GET, "/api/export/**").hasAnyRole("ADMIN", "SUPERVISEUR",
                                "AGENT_ZONE", "AGENT_LOGISTIQUE")
                        .requestMatchers(HttpMethod.GET, "/api/lots/**").hasAnyRole("ADMIN", "AGENT_ZONE",
                                "AGENT_COLLINE", "SUPERVISEUR", "AGENT_LOGISTIQUE")
                        .requestMatchers(HttpMethod.POST, "/api/depots/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.PUT, "/api/depots/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.POST, "/api/agriculteurs/**").hasAnyRole("ADMIN", "AGENT_ZONE",
                                "AGENT_COLLINE")
                        .requestMatchers(HttpMethod.PUT, "/api/agriculteurs/**").hasAnyRole("ADMIN", "AGENT_ZONE",
                                "AGENT_COLLINE")
                        .requestMatchers(HttpMethod.POST, "/api/distributions").hasAnyRole("ADMIN", "SUPERVISEUR",
                                "AGENT_ZONE", "AGENT_COLLINE")
                        .requestMatchers(HttpMethod.POST, "/api/tickets/expirer").hasAnyRole("ADMIN", "SUPERVISEUR")
                        .requestMatchers(HttpMethod.POST, "/api/tickets").hasAnyRole("ADMIN", "AGENT_ZONE",
                                "AGENT_COLLINE")
                        .requestMatchers(HttpMethod.GET, "/api/engrais-types/**").authenticated()
                        .requestMatchers(HttpMethod.POST, "/api/engrais-types").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.PUT, "/api/engrais-types/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.DELETE, "/api/engrais-types/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.GET, "/api/seuils-alerte/**").authenticated()
                        .requestMatchers(HttpMethod.POST, "/api/seuils-alerte").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.PUT, "/api/seuils-alerte/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.DELETE, "/api/seuils-alerte/**").hasRole("ADMIN")
                        .requestMatchers(HttpMethod.POST, "/api/mouvements/*/annuler").hasAnyRole("ADMIN",
                                "SUPERVISEUR")
                        .anyRequest().authenticated())
                .exceptionHandling(ex -> ex
                        .authenticationEntryPoint((req, res, e) -> writeError(res, 401, "Non authentifié"))
                        .accessDeniedHandler((req, res, e) -> writeError(res, 403, "Accès refusé")))
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    private void writeError(jakarta.servlet.http.HttpServletResponse res, int status, String message) throws java.io.IOException {
        res.setStatus(status);
        res.setContentType(MediaType.APPLICATION_JSON_VALUE);
        res.setCharacterEncoding("UTF-8");
        objectMapper.writeValue(res.getWriter(), Map.of("status", status, "erreur", message));
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOriginPatterns(List.of("*"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setExposedHeaders(List.of("Authorization"));
        config.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
