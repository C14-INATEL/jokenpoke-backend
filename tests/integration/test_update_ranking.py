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

    def test_vitoria_ultrapassa_100pts_promove_rank_overflow(self):
        result = Ranking.calcular_novo_rank("Beginner", 80, "vitoria")

        assert result["new_rank"] == "Great"
        assert result["new_points"] == 5
        assert result["status"] == "promoted"

    def test_vitoria_rank_maximo_cap_em_100(self):
        result = Ranking.calcular_novo_rank("Master", 90, "vitoria")

        assert result["new_rank"] == "Master"
        assert result["new_points"] == 100
        assert result["status"] == "maintained"

    def test_derrota_abaixo_de_0_rebaixa_rank_pontos_75(self):
        result = Ranking.calcular_novo_rank("Great", 10, "derrota")

        assert result["new_rank"] == "Beginner"
        assert result["new_points"] == 75
        assert result["status"] == "demoted"

    def test_derrota_rank_minimo_cap_em_0(self):
        result = Ranking.calcular_novo_rank("Beginner", 0, "derrota")

        assert result["new_rank"] == "Beginner"
        assert result["new_points"] == 0
        assert result["status"] == "maintained"

