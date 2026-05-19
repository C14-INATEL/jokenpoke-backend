from app.domain.rules.rank_up_down import RANK_DOWN, RANK_UP


class Ranking:
    PONTOS_VITORIA = 25
    PONTOS_DERROTA = 15
    PONTOS_EMPATE = 0
    PONTOS_MAXIMOS = 100
    PONTOS_MINIMOS = 0

    @classmethod
    def calcular_novo_rank(
        cls, rank_atual: str, pontos_atuais: int, resultado_partida: str
    ) -> dict:

        novo_rank = rank_atual
        novos_pontos = pontos_atuais
        status = "maintained"
        mensagem = "Partida finalizada. Rank mantido."

        if resultado_partida == "vitoria":
            novos_pontos += cls.PONTOS_VITORIA

            if novos_pontos >= cls.PONTOS_MAXIMOS:
                if rank_atual in RANK_UP:
                    novo_rank = RANK_UP[rank_atual]
                    novos_pontos = novos_pontos - cls.PONTOS_MAXIMOS
                    status = "promoted"
                    mensagem = f"Parabéns! Você subiu para o rank {novo_rank}!"
                else:
                    novos_pontos = cls.PONTOS_MAXIMOS
                    mensagem = "Você atingiu a pontuação máxima do jogo!"

        elif resultado_partida == "empate":
            novos_pontos += cls.PONTOS_EMPATE
            mensagem = "Empate! A partida terminou sem alterações na tua pontuação."

        elif resultado_partida == "derrota":
            novos_pontos -= cls.PONTOS_DERROTA

            if novos_pontos < cls.PONTOS_MINIMOS:
                if rank_atual in RANK_DOWN:
                    novo_rank = RANK_DOWN[rank_atual]
                    novos_pontos = 75
                    status = "demoted"
                    mensagem = f"Poxa! Você foi rebaixado para {novo_rank}."
                else:
                    novos_pontos = cls.PONTOS_MINIMOS
                    mensagem = (
                        "Você perdeu, mas já está no rank inicial. Não pode cair mais!"
                    )

        return {
            "old_rank": rank_atual,
            "new_rank": novo_rank,
            "old_points": pontos_atuais,
            "new_points": novos_pontos,
            "status": status,
            "message": mensagem,
        }
