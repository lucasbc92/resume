from datetime import date

import ats
import verificar as v

HOJE = date(2026, 9, 28)


def _pars(tmp_path, perfil="Workday", idioma="pt"):
    caminho = ats.gerar_docx(tmp_path / "cv-{}-{}.docx".format(perfil, idioma), perfil, idioma)
    return v.paragrafos_docx(caminho)


def test_checar_docx_aceita_o_documento_gerado(tmp_path):
    for perfil, idioma in (("Workday", "pt"), ("Gupy", "pt"), ("Workday", "en")):
        assert v.checar_docx(_pars(tmp_path, perfil, idioma), perfil, idioma) == []


def test_checar_docx_acusa_tecnologia_no_topo(tmp_path):
    pars = _pars(tmp_path)
    pars.insert(2, "Java Spring Boot")
    assert any("linha 3" in e for e in v.checar_docx(pars, "Workday", "pt"))


def test_checar_docx_acusa_data_fora_do_formato(tmp_path):
    pars = _pars(tmp_path)
    pars[pars.index("Aug 2025 - Nov 2025")] = "08/2025 - 11/2025"
    assert any("Cast Group" in e for e in v.checar_docx(pars, "Workday", "pt"))


def test_checar_pdf_humano_aceita_o_esperado():
    paginas = ["Lucas Bueno Cesario\nRESUMO\nDESTAQUES\nEXPERIÊNCIA\n"
               "Zukk Cast Group Luizalabs PariPassu",
               "COMPETÊNCIAS\nFORMAÇÃO\nIDIOMAS"]
    assert v.checar_pdf_humano(paginas, "pt") == []


def test_checar_pdf_humano_acusa_tres_paginas_e_vaga_java_na_pagina_2():
    paginas = ["Lucas Bueno Cesario\nRESUMO\nDESTAQUES\nEXPERIÊNCIA\n"
               "Zukk Cast Group Luizalabs",
               "PariPassu\nCOMPETÊNCIAS",
               "FORMAÇÃO\nIDIOMAS"]
    erros = v.checar_pdf_humano(paginas, "pt")
    assert any("3 paginas" in e for e in erros)
    assert any("PariPassu" in e for e in erros)


def test_checar_pdf_humano_acusa_secao_fora_de_ordem():
    paginas = ["Lucas Bueno Cesario\nDESTAQUES\nRESUMO\nEXPERIÊNCIA\n"
               "Zukk Cast Group Luizalabs PariPassu\nCOMPETÊNCIAS\nFORMAÇÃO\nIDIOMAS"]
    assert v.checar_pdf_humano(paginas, "pt") != []


def test_checar_vocabulario_acusa_termo_faltando():
    erros = v.checar_vocabulario("Spring Boot e Angular", "pt", "x.txt")
    assert any("Maven" in e for e in erros)


def test_checar_proibidos_ignora_caixa_e_quebra_de_linha():
    assert v.checar_proibidos("usei Azure service\nbus", "x") != []
    assert v.checar_proibidos("RabbitMQ", "x") == []


def test_checar_salario_na_versao_humana_e_no_perfil_publico():
    assert v.checar_salario("Pretensão: R$ 8.500 a R$ 10.500", "pt", "resume_ptbr.pdf",
                            False) != []
    assert v.checar_salario("sem valores", "pt", "LinkedIn.docx", False) == []
    assert v.checar_salario("sem valores", "pt", "Workday.docx", True) != []
    assert v.checar_salario("Rate: US$ 25-35/h", "en", "Workday.docx", True) == []


def test_checar_anos():
    assert v.checar_anos("7 anos de carreira, 4\ndeles em Java", "pt", "x") == []
    assert v.checar_anos("quase 7 anos", "pt", "x") != []


def test_checar_titulo():
    assert v.checar_titulo("Lucas Bueno Cesario \u2014 Resume \u2014 Sep 2026",
                           "en", HOJE, "x") == []
    assert v.checar_titulo("Lucas Bueno Cesario \u2014 Resume \u2014 Aug 2026",
                           "en", HOJE, "x") != []
