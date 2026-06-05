from app.application.use_cases.update_ranking import Ranking


class TestCalcularNovoRank:
    def test_vitoria_abaixo_do_limite_mantem_rank_adiciona_25pts(self):
        result = Ranking.calcular_novo_rank("Great", 50, "vitoria")

        assert result["new_rank"] == "Great"
        assert result["new_points"] == 75
        assert result["status"] == "maintained"

    def test_derrota_acima_de_15pts_subtrai_mantem_rank(self):
        result = Ranking.calcular_novo_rank("Veteran", 60, "derrota")

        assert result["new_rank"] == "Veteran"
        assert result["new_points"] == 45
        assert result["status"] == "maintained"

    def test_empate_pontos_inalterados(self):
        result = Ranking.calcular_novo_rank("Expert", 40, "empate")

        assert result["new_rank"] == "Expert"
        assert result["new_points"] == 40
        assert result["status"] == "maintained"
