import dataclasses

import conteudo as c
from modelo import T, competencias


def _textos():
    achados = []

    def andar(x):
        if isinstance(x, T):
            achados.append(x)
        elif isinstance(x, (tuple, list)):
            for item in x:
                andar(item)
        elif isinstance(x, dict):
            for item in x.values():
                andar(item)
        elif dataclasses.is_dataclass(x) and not isinstance(x, type):
            for campo in dataclasses.fields(x):
                andar(getattr(x, campo.name))

    for nome in dir(c):
        if nome.isupper():
            andar(getattr(c, nome))
    return achados


def test_todo_texto_tem_pt_e_en_preenchidos():
    textos = _textos()
    assert len(textos) > 100
    assert [t for t in textos if not t.pt.strip() or not t.en.strip()] == []


def test_stack_humano_so_usa_tecnologias_da_propria_vaga():
    for vaga in c.EXPERIENCIAS:
        if vaga.stack_humano:
            assert len(vaga.stack_humano) <= 8, vaga.empresa.pt
            assert set(vaga.stack_humano) <= set(vaga.tecnologias), vaga.empresa.pt


def test_competencias_derivam_nos_dois_idiomas():
    for idioma in ("pt", "en"):
        assert len(competencias(c.EXPERIENCIAS, c.CATEGORIAS, idioma)) >= 8


def test_competencias_em_ingles_usam_rotulo_ingles():
    texto = str(competencias(c.EXPERIENCIAS, c.CATEGORIAS, "en"))
    assert "Microservices" in texto
    assert "Microsserviços" not in texto


def test_tres_destaques():
    assert len(c.DESTAQUES) == 3


def test_resumos_dizem_7_anos_e_4_de_java():
    for resumo in (c.RESUMO_ATS, c.RESUMO_HUMANO):
        assert "7 anos" in resumo.pt and "4 deles" in resumo.pt
        assert "7 years" in resumo.en and "4 of them" in resumo.en
        assert "quase" not in resumo.pt


def test_transacoes_financeiras_nunca_pagamentos_no_resumo():
    assert "transações financeiras" in c.RESUMO_HUMANO.pt
    assert "pagamentos" not in c.RESUMO_HUMANO.pt


def test_cargo_alvo():
    assert c.CARGO_ALVO == T("Desenvolvedor Java Full Stack Pleno/Sênior",
                             "Full Stack Java Developer")


def test_vagas_em_ordem_cronologica_reversa():
    inicios = [v.inicio for v in c.EXPERIENCIAS]
    assert inicios == sorted(inicios, reverse=True)


def test_quatro_vagas_java_primeiro():
    assert [v.empresa.pt for v in c.EXPERIENCIAS[:4]] == [
        "Zukk Tecnologia", "Cast Group", "Luizalabs (Magazine Luiza)", "PariPassu"]
