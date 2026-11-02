package bi.fomi.stock.dto;

public record AgriculteurResponse(Long id, String numeroIdentite, String nom, String prenom, String telephone,
                                  String email, Long collineId, String collineNom, Boolean estCooperative) {
}
