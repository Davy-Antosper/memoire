package bi.fomi.stock.service;

import bi.fomi.stock.dto.RuptureResponse;
import bi.fomi.stock.dto.StockParZoneResponse;
import bi.fomi.stock.dto.TauxServiceZoneResponse;
import bi.fomi.stock.model.entity.Province;
import bi.fomi.stock.model.enums.StatutTicket;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

@Service
public class StatsService {

    @PersistenceContext
    private EntityManager em;

    @Transactional(readOnly = true)
    public List<TauxServiceZoneResponse> tauxServiceParZone() {
        List<Object[]> rows = em.createQuery("""
                        SELECT z.id, z.nom,
                               COALESCE(SUM(t.quantiteServie), 0),
                               COALESCE(SUM(t.quantiteCommandee), 0)
                        FROM Ticket t
                        JOIN t.agriculteur a
                        JOIN a.colline c
                        JOIN c.zone z
                        WHERE t.statut <> :annule
                        GROUP BY z.id, z.nom
                        """, Object[].class)
                .setParameter("annule", StatutTicket.ANNULE)
                .getResultList();

        return rows.stream().map(r -> {
            Long zoneId = ((Number) r[0]).longValue();
            String nom = (String) r[1];
            long servi = ((Number) r[2]).longValue();
            long commande = ((Number) r[3]).longValue();
            double taux = commande == 0 ? 0 : (double) servi / commande;
            return new TauxServiceZoneResponse(zoneId, nom, taux, commande, servi);
        }).toList();
    }

    @Transactional(readOnly = true)
    public List<StockParZoneResponse> stockParProvince() {
        List<Province> provinces = em.createQuery("SELECT p FROM Province p ORDER BY p.nom", Province.class)
                .getResultList();
        List<StockParZoneResponse> resultat = new ArrayList<>();
        for (Province province : provinces) {
            Long pid = province.getId();
            long stock = ((Number) em.createQuery("""
                            SELECT COALESCE(SUM(s.quantiteDisponible), 0)
                            FROM Stock s
                            LEFT JOIN s.depot.province p
                            LEFT JOIN s.depot.zone z
                            LEFT JOIN z.province zp
                            LEFT JOIN s.depot.colline c
                            LEFT JOIN c.zone cz
                            LEFT JOIN cz.province czp
                            WHERE p.id = :pid OR zp.id = :pid OR czp.id = :pid
                            """, Long.class).setParameter("pid", pid).getSingleResult()).longValue();
            long distribue = ((Number) em.createQuery("""
                            SELECT COALESCE(SUM(d.quantite), 0)
                            FROM Distribution d
                            LEFT JOIN d.depot.province p
                            LEFT JOIN d.depot.zone z
                            LEFT JOIN z.province zp
                            LEFT JOIN d.depot.colline c
                            LEFT JOIN c.zone cz
                            LEFT JOIN cz.province czp
                            WHERE p.id = :pid OR zp.id = :pid OR czp.id = :pid
                            """, Long.class).setParameter("pid", pid).getSingleResult()).longValue();
            resultat.add(new StockParZoneResponse(province.getNom(), stock, distribue, stock - distribue));
        }
        return resultat;
    }

    @Transactional(readOnly = true)
    public List<RuptureResponse> ruptures() {
        List<Object[]> rows = em.createQuery("""
                        SELECT s.depot.code, s.depot.nom, s.engraisType.code, s.engraisType.nom
                        FROM Stock s
                        WHERE s.quantiteDisponible = 0
                        ORDER BY s.depot.code
                        """, Object[].class)
                .getResultList();
        return rows.stream()
                .map(r -> new RuptureResponse((String) r[0], (String) r[1], (String) r[2], (String) r[3]))
                .toList();
    }

    @Transactional(readOnly = true)
    public List<Object[]> ticketsNonServisParColline() {
        return em.createQuery("""
                        SELECT c.id, c.nom, z.nom,
                               COUNT(t),
                               COALESCE(SUM(t.quantiteCommandee), 0),
                               COALESCE(SUM(t.quantiteServie), 0),
                               COALESCE(SUM(t.quantiteCommandee), 0) - COALESCE(SUM(t.quantiteServie), 0)
                        FROM Ticket t
                        JOIN t.agriculteur a
                        JOIN a.colline c
                        JOIN c.zone z
                        WHERE t.statut <> :annule
                          AND t.quantiteServie < t.quantiteCommandee
                        GROUP BY c.id, c.nom, z.nom
                        ORDER BY z.nom, c.nom
                        """, Object[].class)
                .setParameter("annule", StatutTicket.ANNULE)
                .getResultList();
    }

    @Transactional(readOnly = true)
    public List<Object[]> tauxServiceParProvince() {
        return em.createQuery("""
                        SELECT p.id, p.nom,
                               COALESCE(SUM(t.quantiteServie), 0),
                               COALESCE(SUM(t.quantiteCommandee), 0)
                        FROM Ticket t
                        JOIN t.agriculteur a
                        JOIN a.colline c
                        JOIN c.zone z
                        JOIN z.province p
                        WHERE t.statut <> :annule
                        GROUP BY p.id, p.nom
                        ORDER BY p.nom
                        """, Object[].class)
                .setParameter("annule", StatutTicket.ANNULE)
                .getResultList();
    }

    @Transactional(readOnly = true)
    public List<Object[]> mouvementsParAgent(Long agentId) {
        return em.createQuery("""
                        SELECT m.type, COUNT(m), COALESCE(SUM(m.quantite), 0)
                        FROM Mouvement m
                        WHERE m.agent.id = :agentId
                          AND m.annule = false
                        GROUP BY m.type
                        ORDER BY m.type
                        """, Object[].class)
                .setParameter("agentId", agentId)
                .getResultList();
    }
}
