package bi.fomi.stock.service;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Component;

/**
 * Implémentation SMTP de la passerelle d'envoi d'emails.
 *
 * La configuration du serveur SMTP provient de {@code spring.mail.*}.
 */
@Component
@RequiredArgsConstructor
public class SmtpMailSender implements MailSenderPort {

    private final JavaMailSender javaMailSender;

    @Value("${fomi.mail.from:no-reply@fomi.bi}")
    private String expediteur;

    @Override
    public void envoyer(String destinataire, String sujet, String contenu) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(expediteur);
        message.setTo(destinataire);
        message.setSubject(sujet);
        message.setText(contenu);
        javaMailSender.send(message);
    }
}
