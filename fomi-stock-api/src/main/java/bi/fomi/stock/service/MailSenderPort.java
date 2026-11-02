package bi.fomi.stock.service;

/**
 * Passerelle d'envoi d'emails.
 *
 * L'abstraction permet de remplacer le transport SMTP par un double de test
 * sans modifier le service métier de notification.
 */
public interface MailSenderPort {

    void envoyer(String destinataire, String sujet, String contenu);
}
