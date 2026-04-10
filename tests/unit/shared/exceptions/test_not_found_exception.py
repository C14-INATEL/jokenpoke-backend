from app.shared.exceptions.not_found_exception import NotFoundException

def test_not_found_exception_salva_mensagem():
    erro = NotFoundException("Usuario sumiu")
    assert erro.message == "Usuario sumiu"
