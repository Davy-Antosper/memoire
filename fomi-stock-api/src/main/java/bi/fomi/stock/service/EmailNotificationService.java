package bi.fomi.stock.service;

import bi.fomi.stock.model.entity.Agriculteur;
import bi.fomi.stock.model.entity.Ticket;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * Notifications email destinées aux agriculteurs.
 *
 * Le service est volontairement tolérant aux pannes : une erreur SMTP est
 * journalisée et tracée dans l'audit sans faire échouer l'opération métier
 * (création de ticket, validation, distribution, etc.).
 */
@Service
@RequiredArgsConstructor
public class EmailNotificationService {

    private static final Logger log = LoggerFactory.getLogger(EmailNotificationService.class);

    private final MailSenderPort mailSenderPort;
    private final AuditLogService auditLogService;

    @Value("${fomi.mail.enabled:false}")
    private boolean enabled;

    @Value("${fomi.mail.sujet-prefix:[FOMI-Stock] }")
    private String sujetPrefix;

    /**
     * Envoie un email à un agriculteur.
     *
     * @return {@code true} si l'email a été remis au transport SMTP, {@code false}
     *         si les notifications sont désactivées, si l'agriculteur n'a pas
     *         d'adresse ou si l'envoi a échoué.
     */
    public boolean notifierAgriculteur(Agriculteur agriculteur, String sujet, String contenu) {
        if (agriculteur == null) {
            return false;
        }
        String destinataire = agriculteur.getEmail();
        if (destinataire == null || destinataire.isBlank()) {
            log.warn("Aucune adresse email pour l'agriculteur {} ({})",
                    agriculteur.getNumeroIdentite(), agriculteur.getId());
            return false;
        }
        if (!enabled) {
            log.info("Notifications email désactivées : message non envoyé à {} ({})",
                    destinataire, sujet);
            return false;
        }

        String sujetComplet = sujetPrefix + sujet;
        try {
            mailSenderPort.envoyer(destinataire.trim(), sujetComplet, contenu);
            auditLogService.log("EMAIL_SEND", "Agriculteur", agriculteur.getId(),
                    details(destinataire, sujetComplet, "OK"));
            log.info("Email envoyé à {} : {}", destinataire, sujetComplet);
            return true;
        } catch (Exception e) {
            auditLogService.log("EMAIL_FAILED", "Agriculteur", agriculteur.getId(),
                    details(destinataire, sujetComplet, e.getMessage()));
            log.error("Échec de l'envoi de l'email à {} : {}", destinataire, e.getMessage());
            return false;
        }
    }

    /**
     * Notifie l'agriculteur d'un changement d'état de son ticket.
     *
     * @param evenement libellé fonctionnel (TICKET_CREE, TICKET_VALIDE,
     *                  TICKET_REJETE, TICKET_EXPIRE, DISTRIBUTION)
     * @param precision information complémentaire (motif de rejet, quantité
     *                  distribuée, etc.), peut être {@code null}
     */
    public boolean notifierTicket(Ticket ticket, String evenement, String precision) {
        if (ticket == null || ticket.getAgriculteur() == null) {
            return false;
        }
        Agriculteur agriculteur = ticket.getAgriculteur();
        String statut = ticket.getStatut() == null ? "—" : ticket.getStatut().name();

        String nomEngrais = ticket.getEngraisType() == null
                ? "non précisé"
                : ticket.getEngraisType().getNom();

        StringBuilder contenu = new StringBuilder();
        contenu.append("Bonjour ").append(agriculteur.getPrenom()).append(' ')
                .append(agriculteur.getNom()).append(",\n\n");
        contenu.append("Votre ticket ").append(ticket.getNumeroTicket())
                .append(" pour l'engrais ").append(nomEngrais)
                .append(" est maintenant : ").append(statut).append(".\n\n");
        contenu.append("Détails du ticket\n");
        contenu.append("- Quantité commandée : ").append(ticket.getQuantiteCommandee()).append(" sacs de 25 kg\n");
        contenu.append("- Quantité servie    : ").append(ticket.getQuantiteServie()).append(" sacs de 25 kg\n");
        contenu.append("- Quantité restante  : ").append(ticket.getQuantiteRestante()).append(" sacs de 25 kg\n");
        if (ticket.getDepotRetrait() != null) {
            contenu.append("- Dépôt de retrait   : ").append(ticket.getDepotRetrait().getNom())
                    .append(" (").append(ticket.getDepotRetrait().getCode()).append(")\n");
        }
        if (ticket.getSaison() != null) {
            contenu.append("- Saison             : ").append(ticket.getSaison()).append('\n');
        }
        if (precision != null && !precision.isBlank()) {
            contenu.append('\n').append(precision).append('\n');
        }
        contenu.append("\nCet email est généré automatiquement par FOMI-Stock. ")
                .append("Merci de ne pas y répondre.\n");

        return notifierAgriculteur(agriculteur, "Ticket " + ticket.getNumeroTicket() + " — " + libelle(evenement),
                contenu.toString());
    }

    private static String libelle(String evenement) {
        if (evenement == null) {
            return "mise à jour";
        }
        return switch (evenement) {
            case "TICKET_CREE" -> "ticket enregistré";
            case "TICKET_VALIDE" -> "ticket validé";
            case "TICKET_REJETE" -> "ticket rejeté";
            case "TICKET_EXPIRE" -> "ticket expiré";
            case "TICKET_ARRIERE" -> "ticket en arriéré";
            case "DISTRIBUTION" -> "distribution enregistrée";
            default -> evenement;
        };
    }

    private static String details(String destinataire, String sujet, String resultat) {
        return "{\"destinataire\":\"" + jsonEscape(destinataire)
                + "\",\"sujet\":\"" + jsonEscape(sujet)
                + "\",\"resultat\":\"" + jsonEscape(resultat) + "\"}";
    }

    /**
     * Échappe une valeur destinée à être insérée dans une chaîne JSON.
     * Les retours à la ligne et caractères de contrôle sont fréquents dans les
     * messages SMTP et rendraient le JSON d'audit invalide s'ils n'étaient pas
     * échappés.
     */
    private static String jsonEscape(String valeur) {
        if (valeur == null) {
            return "";
        }
        StringBuilder sb = new StringBuilder(valeur.length() + 16);
        for (int i = 0; i < valeur.length(); i++) {
            char c = valeur.charAt(i);
            switch (c) {
                case '"' -> sb.append("\\\"");
                case '\\' -> sb.append("\\\\");
                case '\n' -> sb.append("\\n");
                case '\r' -> sb.append("\\r");
                case '\t' -> sb.append("\\t");
                case '\b' -> sb.append("\\b");
                case '\f' -> sb.append("\\f");
                default -> {
                    if (c < 0x20) {
                        sb.append(String.format("\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
                }
            }
        }
        return sb.toString();
    }
}
