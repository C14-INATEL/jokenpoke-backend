from app.application.use_cases.update_ranking import Ranking


class TestRanking:
    def test_vitoria_sem_subir_de_rank(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Beginner", pontos_atuais=50, resultado_partida="vitoria"
        )
        assert resultado["new_rank"] == "Beginner"
        assert resultado["new_points"] == 75
        assert resultado["status"] == "maintained"

    def test_vitoria_com_subida_de_rank(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Beginner", pontos_atuais=80, resultado_partida="vitoria"
        )
        assert resultado["new_rank"] == "Great"
        assert resultado["new_points"] == 5
        assert resultado["status"] == "promoted"
        assert "Parabéns! Você subiu para o rank Great!" in resultado["message"]

    def test_vitoria_no_rank_maximo_master(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Master", pontos_atuais=90, resultado_partida="vitoria"
        )
        assert resultado["new_points"] == 100
        assert resultado["status"] == "maintained"
        assert "pontuação máxima" in resultado["message"]

    def test_derrota_sem_cair_de_rank(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Great", pontos_atuais=50, resultado_partida="derrota"
        )
        assert resultado["new_rank"] == "Great"
        assert resultado["new_points"] == 35
        assert resultado["status"] == "maintained"

    def test_derrota_com_queda_de_rank(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Great", pontos_atuais=10, resultado_partida="derrota"
        )
        assert resultado["new_rank"] == "Beginner"
        assert resultado["new_points"] == 75
        assert resultado["status"] == "demoted"
        assert "rebaixado para Beginner" in resultado["message"]

    def test_derrota_no_rank_minimo_beginner(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Beginner", pontos_atuais=10, resultado_partida="derrota"
        )
        assert resultado["new_rank"] == "Beginner"
        assert resultado["new_points"] == 0
        assert resultado["status"] == "maintained"
        assert "rank inicial" in resultado["message"]

    def test_empate_sem_alteracao_de_pontos(self):
        resultado = Ranking.calcular_novo_rank(
            rank_atual="Beginner", pontos_atuais=50, resultado_partida="empate"
        )
        assert resultado["new_rank"] == "Beginner"
        assert resultado["new_points"] == 50
        assert resultado["status"] == "maintained"
        assert "Empate" in resultado["message"]
