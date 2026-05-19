from app.shared.exceptions.domain_exception import DomainException


def test_domain_exception_salva_mensagem():
    erro = DomainException("Erro de teste")
    assert erro.message == "Erro de teste"


def test_domain_exception_heranca():
    erro = DomainException("Erro de teste")
    assert isinstance(erro, Exception)
