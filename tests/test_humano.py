import subprocess
from datetime import date

import pytest

import conteudo as c
import humano

HOJE = date(2026, 9, 28)


def test_titulo_tem_o_mes_da_geracao():
    assert humano.titulo("pt", HOJE) == "Lucas Bueno Cesario \u2014 Currículo \u2014 Set 2026"
    assert humano.titulo("en", HOJE) == "Lucas Bueno Cesario \u2014 Resume \u2014 Sep 2026"


def test_vaga_alocada_leva_o_cliente_no_titulo():
    assert humano.dados("pt")["vagas"][0]["titulo"] == (
        "Desenvolvedor Java Full Stack Sênior \u2014 Zukk Tecnologia, "
        "alocado na Vivo/Telefónica")


def test_bullet_so_ats_nao_aparece_na_versao_humana():
    luizalabs = humano.dados("pt")["vagas"][2]
    assert not any("Apache Airflow" in b for b in luizalabs["bullets"])
    assert luizalabs["bullets"][0].startswith("Conduzi o upgrade da JVM")


def test_vagas_php_sem_linha_de_stack():
    vagas = humano.dados("pt")["vagas"]
    assert vagas[4]["stack"] is None and vagas[5]["stack"] is None


def test_pdf_tem_um_idioma_e_nenhuma_pretensao():
    html = humano.render_html(("pt",), HOJE, web=False)
    assert "Full Stack com 7 anos de carreira" in html
    assert "cv-en" not in html and "og:title" not in html
    assert "R$" not in html and "US$" not in html


def test_ingles_sem_portugues():
    html = humano.render_html(("en",), HOJE, web=False)
    for pt in ("Experiência", "Destaques", "Resumo", "Ago 2025", "alocado"):
        assert pt not in html, pt
    assert "Aug 2025" in html and "placed at Vivo/Telefónica" in html


def test_web_tem_os_dois_idiomas_seletor_e_og():
    html = humano.render_html(("pt", "en"), HOJE, web=True)
    assert "cv-pt" in html and "cv-en" in html
    assert 'property="og:title"' in html
    assert "try { localStorage" in html
    assert "ARQUIVO GERADO" in html


def test_chrome_ausente_da_erro_claro(tmp_path, monkeypatch):
    monkeypatch.setenv("CHROME", str(tmp_path / "nao-existe.exe"))
    with pytest.raises(RuntimeError, match="CHROME"):
        humano.chrome()


def _paginas(pdf):
    saida = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                           stdin=subprocess.DEVNULL, capture_output=True,
                           check=True).stdout.decode("utf-8")
    return [p for p in saida.split("\f") if p.strip()]


@pytest.mark.parametrize("idioma", ["pt", "en"])
def test_pdf_real_ate_duas_paginas_com_java_na_primeira(tmp_path, idioma):
    html = humano.render_html((idioma,), HOJE, web=False)
    pdf = humano.imprimir_pdf(html, tmp_path / "cv.pdf")
    paginas = _paginas(pdf)
    assert len(paginas) <= 2
    assert paginas[0].lstrip().startswith(c.NOME)
    for empresa in ("Zukk", "Cast Group", "Luizalabs", "PariPassu"):
        assert empresa in paginas[0], empresa


def test_chrome_que_nao_executa_da_erro_claro(tmp_path, monkeypatch):
    falso = tmp_path / "chrome.txt"
    falso.write_text("nao sou um executavel", encoding="utf-8")
    monkeypatch.setenv("CHROME", str(falso))
    with pytest.raises(RuntimeError, match="CHROME"):
        humano.imprimir_pdf("<p>x</p>", tmp_path / "x.pdf")


def test_chrome_com_aspas_em_volta_funciona(monkeypatch):
    monkeypatch.setenv("CHROME", '"' + humano.CHROME_PADRAO[0] + '"')
    assert humano.chrome() == humano.CHROME_PADRAO[0]


@pytest.mark.parametrize("idioma", ["pt", "en"])
def test_competencias_extraem_rotulo_junto_do_valor(tmp_path, idioma):
    # O PDF humano muitas vezes e subido no ATS do recrutador: cada linha de
    # competencia tem que sair com o rotulo colado ao proprio valor.
    pdf = humano.imprimir_pdf(humano.render_html((idioma,), HOJE, web=False),
                              tmp_path / "cv.pdf")
    texto = " ".join(" ".join(_paginas(pdf)).split())
    for rotulo, valor in c.COMPETENCIAS_HUMANO:
        esperado = "{}: {}".format(rotulo.em(idioma), valor.em(idioma).split(",")[0])
        assert esperado in texto, esperado
