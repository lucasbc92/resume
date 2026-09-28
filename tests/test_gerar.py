from datetime import date

import gerar
import verificar

HOJE = date(2026, 9, 28)


def test_nome_do_snapshot():
    assert (gerar.nome_snapshot("pt", HOJE, "pdf")
            == "resume_lucas-bueno-cesario_ptbr_2026-09-28_set.pdf")
    assert (gerar.nome_snapshot("en", HOJE, "docx")
            == "resume_lucas-bueno-cesario_en_2026-09-28_sep.docx")


def test_gerar_tudo_produz_saidas_que_passam_na_verificacao(tmp_path):
    nomes = {s.name for s in gerar.gerar_tudo(tmp_path, HOJE)}
    for esperado in ("resume_ptbr.pdf", "resume_en.pdf", "index.html",
                     "Lucas-Bueno-Cesario-Curriculo-Gupy.docx",
                     "Lucas-Bueno-Cesario-Curriculo-Workday.txt",
                     "Lucas-Bueno-Cesario-Resume-Workday.txt",
                     "resume_lucas-bueno-cesario_ptbr_2026-09-28_set.pdf",
                     "resume_lucas-bueno-cesario_en_2026-09-28_sep.docx"):
        assert esperado in nomes, esperado
    assert verificar.verificar_tudo(tmp_path, HOJE) == []
