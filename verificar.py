# -*- coding: utf-8 -*-
"""
Checagens das saidas. gerar.py chama verificar_tudo() e sai com erro se houver
qualquer problema. As funcoes checar_* recebem texto (nao arquivo) para poderem
ser testadas sem gerar nada.
"""

import re
import shutil
import subprocess

from docx import Document

import ats
import conteudo as c
import humano
from modelo import formatar_periodo, item_stack, limpar

# Afirmacoes que ja apareceram em material antigo e sao falsas, ou habilidades
# que o Lucas nao tem. Busca literal, sem diferenciar maiusculas. Editavel.
PROIBIDOS = ("Service Bus", "Cosmos", "90%", "60%", "Kafka", "Golang", "Fortify")

# Termos recorrentes nas vagas-alvo. Regex, sem diferenciar maiusculas.
VOCABULARIO = {
    "pt": ("Spring Boot", "Spring Data JPA", "Hibernate", "Maven", "Microsservi[cç]os",
           "APIs? REST", "Angular", "React", "TypeScript", r"Node\.js", "Docker",
           "Kubernetes", "CI/CD", "Scrum", "Kanban", "Oracle", "PostgreSQL", "AWS",
           "Azure", "JUnit", "Mockito", "SonarQube", "RabbitMQ", "mensageria",
           "observabilidade", r"\bGit\b", "Linux"),
    "en": ("Spring Boot", "Spring Data JPA", "Hibernate", "Maven", "Microservices",
           "REST APIs?|APIs? REST", "Angular", "React", "TypeScript", r"Node\.js",
           "Docker", "Kubernetes", "CI/CD", "Scrum", "Kanban", "Oracle", "PostgreSQL",
           "AWS", "Azure", "JUnit", "Mockito", "SonarQube", "RabbitMQ", "messaging",
           "observability", r"\bGit\b", "Linux"),
}

SALARIO = {"pt": "R$ 8.500", "en": "US$ 25-35"}
ANOS = {"pt": ("7 anos", "4 deles"), "en": ("7 years", "4 of them")}


def _plano(texto):
    """Junta quebras de linha: o pdftotext quebra frases no fim de cada linha."""
    return re.sub(r"\s+", " ", texto)


# -------------------------------------------------------- checagens puras ----

def checar_docx(pars, perfil, idioma):
    erros = []
    if not pars or pars[0] != c.NOME:
        erros.append("linha 1 nao e o nome")
    if len(pars) < 2 or pars[1] != c.EMAIL:
        erros.append("linha 2 nao e o e-mail")

    chaves = sorted({k for _, entradas in c.CATEGORIAS for _, ks in entradas for k in ks},
                    key=len, reverse=True)
    for i, linha in enumerate(pars[:6]):
        for chave in chaves:
            if re.search(r"(?<!\w)" + re.escape(chave) + r"(?!\w)", linha):
                erros.append("tecnologia '{}' na linha {}: {}".format(chave, i + 1, linha))
                break

    formato = ats.PERFIS[perfil]["datas"]
    cursor = 0
    for vaga in c.EXPERIENCIAS:
        cargo = limpar(vaga.cargo.em(idioma))
        try:
            i = pars.index(cargo, cursor)
        except ValueError:
            erros.append("cargo ausente: " + cargo)
            continue
        cursor = i + 1
        esperado = [limpar(vaga.empresa.em(idioma)), limpar(vaga.meta_ats.em(idioma)),
                    formatar_periodo(vaga.inicio, vaga.fim, formato)]
        if pars[i + 1:i + 4] != esperado:
            erros.append("bloco da vaga fora do padrao ({}): {}".format(
                cargo, pars[i + 1:i + 4]))
    return erros


def checar_pdf_humano(paginas, idioma):
    erros = []
    if len(paginas) > 2:
        erros.append("PDF com {} paginas (maximo 2)".format(len(paginas)))
    texto = "\n".join(paginas)
    if not texto.lstrip().startswith(c.NOME):
        erros.append("o texto extraido nao comeca pelo nome")
    minusculo = texto.lower()
    posicao = -1
    for secao in humano.SECOES.values():
        achou = minusculo.find(secao.em(idioma).lower(), posicao + 1)
        if achou < 0:
            erros.append("secao ausente ou fora de ordem: " + secao.em(idioma))
        else:
            posicao = achou
    # Pelo titulo da vaga, nao pelo nome da empresa: o resumo tambem cita
    # Cast Group e Luizalabs, e isso nao prova que a vaga esta na pagina 1.
    primeira = _plano(paginas[0]) if paginas else ""
    for vaga, dados_vaga in zip(c.EXPERIENCIAS, humano.dados(idioma)["vagas"]):
        if "Java" in vaga.cargo.pt and _plano(dados_vaga["titulo"]) not in primeira:
            erros.append("vaga Java fora da pagina 1: " + dados_vaga["titulo"])
    return erros


def checar_vocabulario(texto, idioma, nome):
    plano = _plano(texto)
    return ["{}: termo ausente: {}".format(nome, padrao)
            for padrao in VOCABULARIO[idioma] if not re.search(padrao, plano, re.I)]


def checar_proibidos(texto, nome):
    plano = _plano(texto).lower()
    return ["{}: afirmacao proibida: {}".format(nome, termo)
            for termo in PROIBIDOS if termo.lower() in plano]


def checar_anos(texto, idioma, nome):
    plano = _plano(texto)
    return ["{}: falta '{}'".format(nome, trecho)
            for trecho in ANOS[idioma] if trecho not in plano]


def checar_salario(texto, idioma, nome, deve_ter):
    plano = _plano(texto)
    if deve_ter:
        if SALARIO[idioma] not in plano:
            return ["{}: pretensao ausente".format(nome)]
        return []
    if "R$" in plano or "US$" in plano:
        return ["{}: pretensao nao deveria aparecer aqui".format(nome)]
    return []


def checar_titulo(titulo_pdf, idioma, hoje, nome):
    esperado = humano.titulo(idioma, hoje)
    if titulo_pdf != esperado:
        return ["{}: titulo '{}', esperado '{}'".format(nome, titulo_pdf, esperado)]
    return []


# ---------------------------------------------------------- leitura -------

def _ferramenta(nome):
    caminho = shutil.which(nome)
    if not caminho:
        raise RuntimeError("{} nao encontrado no PATH (vem com o MiKTeX).".format(nome))
    return caminho


def paragrafos_docx(caminho):
    return [p.text for p in Document(str(caminho)).paragraphs]


def paginas_pdf(caminho):
    saida = subprocess.run([_ferramenta("pdftotext"), "-enc", "UTF-8", str(caminho), "-"],
                           stdin=subprocess.DEVNULL, capture_output=True,
                           check=True).stdout.decode("utf-8")
    return [pagina for pagina in saida.split("\f") if pagina.strip()]


def titulo_pdf(caminho):
    saida = subprocess.run([_ferramenta("pdfinfo"), "-enc", "UTF-8", str(caminho)],
                           stdin=subprocess.DEVNULL, capture_output=True,
                           check=True).stdout.decode("utf-8")
    for linha in saida.splitlines():
        if linha.startswith("Title:"):
            return linha[len("Title:"):].strip()
    return ""


# ------------------------------------------------------------ tudo --------

def verificar_tudo(raiz, hoje):
    erros = []

    # Integridade do modelo: a linha de stack humana so pode citar tecnologia da
    # propria vaga. (Tecnologia sem categoria ja quebra a geracao em
    # modelo.competencias.)
    for vaga in c.EXPERIENCIAS:
        chaves = {item_stack(i, "pt", c.ROTULOS)[0] for i in (vaga.stack_humano or ())}
        fora = chaves - set(vaga.tecnologias)
        if fora:
            erros.append("stack_humano de {} fora de tecnologias: {}".format(
                vaga.empresa.pt, ", ".join(sorted(fora))))

    for perfil, cfg in ats.PERFIS.items():
        for idioma in cfg["idiomas"]:
            docx = raiz / ats.nome_arquivo(perfil, idioma, "docx")
            if not docx.is_file():
                erros.append("faltando: " + docx.name)
                continue
            pars = paragrafos_docx(docx)
            texto = "\n".join(pars)
            erros += ["{}: {}".format(docx.name, e) for e in checar_docx(pars, perfil, idioma)]
            erros += checar_proibidos(texto, docx.name)
            erros += checar_anos(texto, idioma, docx.name)
            erros += checar_salario(texto, idioma, docx.name, cfg["salario"])
            if cfg["txt"]:
                txt = raiz / ats.nome_arquivo(perfil, idioma, "txt")
                conteudo_txt = txt.read_text(encoding="utf-8")
                erros += checar_vocabulario(conteudo_txt, idioma, txt.name)
                erros += checar_proibidos(conteudo_txt, txt.name)

    for idioma, arquivo in humano.PDFS.items():
        pdf = raiz / arquivo
        if not pdf.is_file():
            erros.append("faltando: " + arquivo)
            continue
        paginas = paginas_pdf(pdf)
        texto = "\n".join(paginas)
        erros += ["{}: {}".format(arquivo, e) for e in checar_pdf_humano(paginas, idioma)]
        erros += checar_proibidos(texto, arquivo)
        erros += checar_anos(texto, idioma, arquivo)
        erros += checar_salario(texto, idioma, arquivo, False)
        erros += checar_titulo(titulo_pdf(pdf), idioma, hoje, arquivo)

    for pdf in sorted(raiz.glob("*_ats_*_lucas-bueno-cesario.pdf")):
        idioma = "pt" if pdf.name.startswith("ptbr_") else "en"
        texto = "\n".join(paginas_pdf(pdf))
        if not texto.lstrip().startswith(c.NOME):
            erros.append("{}: o texto extraido nao comeca pelo nome".format(pdf.name))
        erros += checar_proibidos(texto, pdf.name)
        erros += checar_anos(texto, idioma, pdf.name)
        erros += checar_salario(texto, idioma, pdf.name, False)

    index = raiz / "index.html"
    if not index.is_file():
        erros.append("faltando: index.html")
    else:
        html = index.read_text(encoding="utf-8")
        erros += checar_proibidos(html, "index.html")
        erros += checar_salario(html, "pt", "index.html", False)
    return erros
