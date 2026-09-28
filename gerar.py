#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera TODAS as versoes do curriculo a partir de conteudo.py e verifica o
resultado. E o unico comando que se roda:

    python gerar.py

Saidas (nesta pasta):
  * ATS, PT e EN: Lucas-Bueno-Cesario-{Curriculo,Resume}-<Perfil>.docx (+ .txt)
  * Humana: resume_ptbr.pdf e resume_en.pdf (nomes estaveis) e index.html
  * Snapshots do dia, com data e tipo:
      resume_lucas-bueno-cesario_{ptbr,en}_<data>_<mes>_{humano,human}.pdf
      resume_lucas-bueno-cesario_{ptbr,en}_<data>_<mes>_ats.docx

Sai com codigo 1 se a verificacao falhar - nesse caso NAO publique.
"""

import shutil
import sys
from datetime import date
from pathlib import Path

import ats
import humano
import verificar

RAIZ = Path(__file__).resolve().parent

MES_ARQUIVO = {
    "pt": ["jan", "fev", "mar", "abr", "mai", "jun",
           "jul", "ago", "set", "out", "nov", "dez"],
    "en": ["jan", "feb", "mar", "apr", "may", "jun",
           "jul", "aug", "sep", "oct", "nov", "dec"],
}


# Tipo no fim do nome: da para saber o que e cada snapshot sem abrir o arquivo.
SUFIXO_TIPO = {
    ("humano", "pt"): "humano", ("humano", "en"): "human",
    ("ats", "pt"): "ats", ("ats", "en"): "ats",
}


def nome_snapshot(idioma, hoje, tipo, ext):
    return "resume_lucas-bueno-cesario_{}_{:%Y-%m-%d}_{}_{}.{}".format(
        "ptbr" if idioma == "pt" else "en", hoje, MES_ARQUIVO[idioma][hoje.month - 1],
        SUFIXO_TIPO[(tipo, idioma)], ext)


def gerar_tudo(raiz, hoje):
    raiz = Path(raiz)
    saidas = []
    for perfil, cfg in ats.PERFIS.items():
        for idioma in cfg["idiomas"]:
            saidas.append(ats.gerar_docx(raiz / ats.nome_arquivo(perfil, idioma, "docx"),
                                         perfil, idioma))
            if cfg["txt"]:
                saidas.append(ats.gerar_txt(raiz / ats.nome_arquivo(perfil, idioma, "txt"),
                                            perfil, idioma))

    for idioma, arquivo in humano.PDFS.items():
        pdf = humano.imprimir_pdf(humano.render_html((idioma,), hoje, web=False),
                                  raiz / arquivo)
        snapshot = raiz / nome_snapshot(idioma, hoje, "humano", "pdf")
        shutil.copyfile(pdf, snapshot)
        saidas += [pdf, snapshot]
        # Snapshot ATS: o perfil Workday e o de referencia, como no gerador antigo.
        saidas.append(ats.gerar_docx(raiz / nome_snapshot(idioma, hoje, "ats", "docx"),
                                     "Workday", idioma))

    index = raiz / "index.html"
    index.write_text(humano.render_html(("pt", "en"), hoje, web=True), encoding="utf-8")
    saidas.append(index)
    return saidas


def main():
    hoje = date.today()
    try:
        saidas = gerar_tudo(RAIZ, hoje)
        largura = max(len(s.name) for s in saidas)
        for caminho in saidas:
            print("{:<{w}}  {:>9,} bytes".format(caminho.name, caminho.stat().st_size,
                                                  w=largura))
        erros = verificar.verificar_tudo(RAIZ, hoje)
    except RuntimeError as erro:
        # Erro de ambiente (Chrome, pdftotext): a mensagem ja diz o que fazer.
        print("ERRO: {}".format(erro), file=sys.stderr)
        return 1
    if erros:
        print("\nVERIFICACAO FALHOU - nao publique:", file=sys.stderr)
        for erro in erros:
            print("  - " + erro, file=sys.stderr)
        return 1
    print("\nVerificacao OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
