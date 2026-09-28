# -*- coding: utf-8 -*-
"""
Renderizador da versao humana: conteudo.py -> Jinja2 -> HTML -> Chrome headless -> PDF.

Layout A (classico sobrio): coluna unica, preto e branco, A4. A coluna unica nao
e estetica: o recrutador muitas vezes sobe este PDF no ATS dele, e duas colunas
saem embaralhadas na extracao.

O mesmo template gera o index.html do GitHub Pages (web=True): os dois idiomas
na pagina, com seletor PT/EN.
"""

import os
import subprocess
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

import conteudo as c
from modelo import MES_EN, MES_PT, T, formatar_periodo, item_stack

RAIZ = Path(__file__).resolve().parent

# Nome estavel de cada PDF humano: e o que vai por link e por e-mail.
PDFS = {"pt": "resume_ptbr.pdf", "en": "resume_en.pdf"}

# Na ordem de exibicao (verificar.py confere essa ordem no PDF).
SECOES = {
    "resumo": T("Resumo", "Summary"),
    "destaques": T("Destaques", "Highlights"),
    "experiencia": T("Experiência", "Experience"),
    "competencias": T("Competências", "Skills"),
    "formacao": T("Formação", "Education"),
    "idiomas": T("Idiomas", "Languages"),
}

NOME_DOCUMENTO = T("Currículo", "Resume")

OG = {
    "titulo": "Lucas Bueno Cesario | Desenvolvedor Java Full Stack",
    "descricao": "Spring Boot, microsserviços, Angular e React. 7 anos de carreira, "
                 "4 em Java. Remoto, UTC-3.",
    "imagem": "https://i.imgur.com/kmzS276.jpeg",
    "url": "https://lucasbc92.github.io/resume/",
}

CHROME_PADRAO = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
)


def titulo(idioma, hoje):
    """Titulo do HTML e do PDF, com o mes da geracao (verificar.py confere)."""
    mes = (MES_PT if idioma == "pt" else MES_EN)[hoje.month - 1]
    return "{} \u2014 {} \u2014 {} {}".format(c.NOME, NOME_DOCUMENTO.em(idioma), mes, hoje.year)


def dados(idioma):
    """Tudo o que o template precisa para um idioma, ja resolvido em texto."""
    formato = "mmm-pt" if idioma == "pt" else "mmm-en"
    vagas = []
    for vaga in c.EXPERIENCIAS:
        cabecalho = vaga.cargo.em(idioma) + " \u2014 " + vaga.empresa.em(idioma)
        if vaga.cliente:
            cabecalho += ", " + vaga.cliente.em(idioma)
        textos = [b.texto_humano() for b in vaga.bullets]
        stack = None
        if vaga.stack_humano:
            stack = " \u00b7 ".join(item_stack(i, idioma, c.ROTULOS)[1]
                                    for i in vaga.stack_humano)
        vagas.append({
            "titulo": cabecalho,
            "meta": (formatar_periodo(vaga.inicio, vaga.fim, formato, " \u2013 ")
                     + " \u00b7 " + vaga.local.em(idioma)),
            "contexto": vaga.contexto.em(idioma) if vaga.contexto else None,
            "bullets": [t.em(idioma) for t in textos if t is not None],
            "stack": stack,
        })
    return {
        "idioma": idioma,
        "lang": "pt-BR" if idioma == "pt" else "en",
        "secoes": {chave: t.em(idioma) for chave, t in SECOES.items()},
        "nome": c.NOME,
        "cargo": c.TITULO_HUMANO.em(idioma),
        "contato": [
            (c.LOCAL_HUMANO.em(idioma), None),
            (c.EMAIL, "mailto:" + c.EMAIL),
            (c.TELEFONE.em(idioma), c.WHATSAPP_LINK),
            (c.LINKEDIN, "https://" + c.LINKEDIN),
            (c.GITHUB, "https://" + c.GITHUB),
        ],
        "resumo": c.RESUMO_HUMANO.em(idioma),
        "destaques": [d.em(idioma) for d in c.DESTAQUES],
        "vagas": vagas,
        "competencias": [(r.em(idioma), v.em(idioma)) for r, v in c.COMPETENCIAS_HUMANO],
        "formacao": [f.em(idioma) for f in c.FORMACAO_HUMANO],
        "idiomas": c.IDIOMAS_HUMANO.em(idioma),
    }


def render_html(idiomas, hoje, web):
    ambiente = Environment(loader=FileSystemLoader(str(RAIZ / "templates")),
                           autoescape=select_autoescape(["html", "j2"]))
    return ambiente.get_template("humano.html.j2").render(
        cvs=[dados(i) for i in idiomas],
        titulo=titulo(idiomas[0], hoje),
        titulos={i: titulo(i, hoje) for i in idiomas},
        web=web,
        og=OG,
    )


def chrome():
    """Caminho do Chrome: variavel CHROME, senao os caminhos padrao do Windows."""
    # strip: "Copiar como caminho" do Windows cola o caminho entre aspas.
    definido = os.environ.get("CHROME", "").strip().strip('"')
    candidatos = [definido] if definido else list(CHROME_PADRAO)
    for candidato in candidatos:
        if Path(candidato).is_file():
            return candidato
    raise RuntimeError(
        "Chrome nao encontrado (tentei: {}). Defina a variavel CHROME com o caminho "
        "do chrome.exe.".format(", ".join(candidatos)))


def imprimir_pdf(html, destino):
    destino = Path(destino).resolve()
    if destino.exists():
        destino.unlink()
    # Perfil proprio: nao briga com um Chrome ja aberto pelo usuario.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        fonte = Path(tmp) / "curriculo.html"
        fonte.write_text(html, encoding="utf-8")
        executavel = chrome()
        try:
            resultado = subprocess.run(
                [executavel, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                 "--user-data-dir=" + str(Path(tmp) / "perfil"),
                 "--print-to-pdf=" + str(destino), fonte.as_uri()],
                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as erro:
            raise RuntimeError(
                "Chrome em {} nao executou ({}). Ajuste a variavel CHROME para o "
                "caminho do chrome.exe.".format(executavel, erro)) from erro
    if resultado.returncode != 0 or not destino.is_file():
        raise RuntimeError("Chrome falhou ao gerar {}: {}".format(
            destino.name, (resultado.stderr or "").strip()[-500:]))
    return destino
