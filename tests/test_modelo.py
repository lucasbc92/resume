import pytest

from modelo import (B, IGUAL, T, Vaga, competencias, formatar_data,
                    formatar_periodo, limpar, rotulo)


def test_t_devolve_o_idioma_pedido():
    t = T("olá", "hello")
    assert t.em("pt") == "olá"
    assert t.em("en") == "hello"


def test_t_rejeita_idioma_desconhecido():
    with pytest.raises(ValueError):
        T("a", "b").em("es")


def test_bullet_igual_reaproveita_o_texto_ats():
    ats = T("x", "y")
    assert B(ats=ats, humano=IGUAL).texto_humano() is ats


def test_bullet_so_ats_nao_tem_texto_humano():
    assert B(ats=T("x", "y")).texto_humano() is None


def test_bullet_so_humano_nao_tem_texto_ats():
    b = B(humano=T("x", "y"))
    assert b.ats is None
    assert b.texto_humano() == T("x", "y")


def test_bullet_sem_texto_nenhum_e_rejeitado():
    with pytest.raises(ValueError):
        B(ats=None, humano=IGUAL)


def test_limpar_troca_pontuacao_tipografica_e_mantem_acentos():
    entrada = "Sênior \u2014 \u201cx\u201d \u00b7 a\u2013b\u00a0c"
    assert limpar(entrada) == 'Sênior - "x" - a-b c'


@pytest.mark.parametrize("formato, esperado", [
    ("mm/aaaa", "08/2025"), ("mmm-en", "Aug 2025"), ("mmm-pt", "Ago 2025")])
def test_formatar_data(formato, esperado):
    assert formatar_data((2025, 8), formato) == esperado


def test_formatar_data_rejeita_formato_desconhecido():
    with pytest.raises(ValueError):
        formatar_data((2025, 8), "aaaa-mm")


def test_formatar_periodo_usa_o_separador():
    assert formatar_periodo((2025, 8), (2025, 11), "mmm-pt") == "Ago 2025 - Nov 2025"
    assert (formatar_periodo((2025, 8), (2025, 11), "mmm-en", " \u2013 ")
            == "Aug 2025 \u2013 Nov 2025")


def test_rotulo_traduz_quando_ha_traducao():
    rotulos = {"Microsserviços": T("Microsserviços", "Microservices")}
    assert rotulo("Microsserviços", "en", rotulos) == "Microservices"
    assert rotulo("Docker", "en", rotulos) == "Docker"


def _vaga(*tecnologias):
    return Vaga(cargo=T("c", "c"), empresa=T("e", "e"), inicio=(2020, 1),
                fim=(2020, 2), meta_ats=T("m", "m"), local=T("l", "l"),
                bullets=(), tecnologias=tecnologias)


CATEGORIAS = (
    (T("Back-end", "Back-end"), (
        (T("Java (8 a 21)", "Java (8 to 21)"), ("Java", "Java 8", "Java 21")),
        (T("Spring Boot", "Spring Boot"), ("Spring Boot",)),
    )),
    (T("Front-end", "Front-end"), (
        (T("Angular", "Angular"), ("Angular",)),
    )),
)


def test_competencias_mostra_so_o_que_as_vagas_usam_na_ordem_das_categorias():
    vagas = [_vaga("Spring Boot", "Java 21"), _vaga("Java 8")]
    assert competencias(vagas, CATEGORIAS, "en") == [
        ("Back-end", "Java (8 to 21), Spring Boot")]


def test_competencias_rejeita_tecnologia_sem_categoria():
    with pytest.raises(ValueError, match="Kotlin"):
        competencias([_vaga("Kotlin")], CATEGORIAS, "pt")
