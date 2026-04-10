from app.shared.exceptions.domain_exception import DomainException

def test_domain_exception_salva_mensagem():
    erro = DomainException("Erro de teste")
    assert erro.message == "Erro de teste"
