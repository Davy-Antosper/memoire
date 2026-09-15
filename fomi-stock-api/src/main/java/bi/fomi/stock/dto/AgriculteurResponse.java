package bi.fomi.stock.dto;

public record AgriculteurResponse(Long id, String numeroIdentite, String nom, String prenom, String telephone,
                                  Long collineId, String collineNom, Boolean estCooperative) {
}
