from datetime import date

import ats
import gerar
import verificar

HOJE = date(2026, 9, 28)


def test_nome_do_snapshot_leva_data_e_tipo():
    assert (gerar.nome_snapshot("pt", HOJE, "human", "pdf")
            == "ptbr_human_2026-09_set_lucas-bueno-cesario.pdf")
    assert (gerar.nome_snapshot("en", HOJE, "human", "pdf")
            == "en_human_2026-09_sep_lucas-bueno-cesario.pdf")
    assert (gerar.nome_snapshot("pt", HOJE, "ats", "docx")
            == "ptbr_ats_2026-09_set_lucas-bueno-cesario.docx")


def test_gerar_tudo_produz_saidas_que_passam_na_verificacao(tmp_path):
    nomes = {s.name for s in gerar.gerar_tudo(tmp_path, HOJE)}
    for esperado in ("resume_ptbr.pdf", "resume_en.pdf", "index.html",
                     "Lucas-Bueno-Cesario-Curriculo-Gupy.docx",
                     "Lucas-Bueno-Cesario-Curriculo-Workday.txt",
                     "Lucas-Bueno-Cesario-Resume-Workday.txt",
                     "ptbr_human_2026-09_set_lucas-bueno-cesario.pdf",
                     "en_ats_2026-09_sep_lucas-bueno-cesario.docx",
                     "en_ats_2026-09_sep_lucas-bueno-cesario.pdf"):
        assert esperado in nomes, esperado
    assert verificar.verificar_tudo(tmp_path, HOJE) == []


def test_main_mostra_erro_sem_traceback(monkeypatch, capsys):
    def falha(raiz, hoje):
        raise RuntimeError("Chrome nao encontrado. Defina a variavel CHROME")
    monkeypatch.setattr(gerar, "gerar_tudo", falha)
    assert gerar.main() == 1
    assert "CHROME" in capsys.readouterr().err


def test_main_mostra_erro_da_verificacao_sem_traceback(tmp_path, monkeypatch, capsys):
    arquivo = tmp_path / "x.txt"
    arquivo.write_text("x", encoding="utf-8")
    monkeypatch.setattr(gerar, "gerar_tudo", lambda raiz, hoje: [arquivo])

    def falha(raiz, hoje):
        raise RuntimeError("pdftotext nao encontrado no PATH")
    monkeypatch.setattr(gerar.verificar, "verificar_tudo", falha)
    assert gerar.main() == 1
    assert "pdftotext" in capsys.readouterr().err


def test_txt_commitados_batem_com_o_conteudo(tmp_path):
    # Pega o "editei conteudo.py e esqueci de rodar gerar.py".
    for perfil, cfg in ats.PERFIS.items():
        if not cfg["txt"]:
            continue
        for idioma in cfg["idiomas"]:
            nome = ats.nome_arquivo(perfil, idioma, "txt")
            novo = ats.gerar_txt(tmp_path / nome, perfil, idioma).read_text(encoding="utf-8")
            commitado = (gerar.RAIZ / nome).read_text(encoding="utf-8").replace("\r\n", "\n")
            assert novo == commitado, nome + " desatualizado: rode python gerar.py"
