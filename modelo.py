# -*- coding: utf-8 -*-
"""
Tipos e funcoes puras do curriculo. Nenhum fato mora aqui: os fatos ficam em
conteudo.py, e a forma de desenhar fica em ats.py e humano.py.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class T:
    """Um texto nos dois idiomas."""
    pt: str
    en: str

    def em(self, idioma):
        if idioma == "pt":
            return self.pt
        if idioma == "en":
            return self.en
        raise ValueError("idioma desconhecido: {!r}".format(idioma))


class _Igual:
    def __repr__(self):
        return "IGUAL"


# Marcador de bullet: a versao humana reaproveita o texto do ATS.
IGUAL = _Igual()


@dataclass(frozen=True)
class B:
    """Bullet de experiencia.

    ats=None     -> so aparece na versao humana
    humano=None  -> so aparece no ATS
    humano=IGUAL -> a versao humana usa o mesmo texto do ATS
    """
    ats: object = None
    humano: object = None

    def __post_init__(self):
        if self.ats is None and (self.humano is None or self.humano is IGUAL):
            raise ValueError("bullet sem texto para nenhuma das versoes")

    def texto_humano(self):
        return self.ats if self.humano is IGUAL else self.humano


@dataclass(frozen=True)
class Vaga:
    cargo: T
    empresa: T
    inicio: tuple                # (ano, mes)
    fim: tuple                   # (ano, mes)
    meta_ats: T                  # 3a linha do bloco da vaga no ATS
    local: T                     # local na versao humana
    bullets: tuple               # de B
    tecnologias: tuple           # chaves; ver CATEGORIAS e ROTULOS em conteudo.py
    cliente: object = None       # T: ", alocado na ..." no titulo humano
    contexto: object = None      # T: linha em italico, so na versao humana
    stack_humano: object = None  # tuple de ate 8 chaves, ou None (sem linha)


@dataclass(frozen=True)
class Formacao:
    curso: T
    instituicao: T
    conclusao: tuple             # (ano, mes)


# Pontuacao tipografica que atrapalha tokenizador de parser. Acentos ficam.
SUBSTITUICOES = {
    "\u2014": "-",   # travessao
    "\u2013": "-",   # meia-risca
    "\u2212": "-",   # sinal de menos
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2026": "...",
    "\u00a0": " ",   # espaco inquebravel
    "\u2011": "-",   # hifen inquebravel
    "\u00b7": "-",   # ponto medio: sozinho ja quebra "Spring Boot" em entidade
}


def limpar(texto):
    for de, para in SUBSTITUICOES.items():
        texto = texto.replace(de, para)
    return texto


MES_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
          "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def formatar_data(ano_mes, formato):
    """"mm/aaaa" -> 08/2025 | "mmm-en" -> Aug 2025 | "mmm-pt" -> Ago 2025"""
    ano, mes = ano_mes
    if formato == "mm/aaaa":
        return "{:02d}/{}".format(mes, ano)
    if formato == "mmm-en":
        return "{} {}".format(MES_EN[mes - 1], ano)
    if formato == "mmm-pt":
        return "{} {}".format(MES_PT[mes - 1], ano)
    raise ValueError("formato de data desconhecido: {!r}".format(formato))


def formatar_periodo(inicio, fim, formato, separador=" - "):
    return formatar_data(inicio, formato) + separador + formatar_data(fim, formato)


def rotulo(chave, idioma, rotulos):
    """Nome de uma tecnologia no idioma pedido. Sem traducao, a chave vale nos dois."""
    traducao = rotulos.get(chave)
    return traducao.em(idioma) if traducao else chave


def competencias(vagas, categorias, idioma):
    """Secao de competencias DERIVADA das vagas: [(categoria, "a, b, c"), ...].

    categorias = ((T nome, ((T rotulo, (chave, ...)), ...)), ...)
    Uma entrada aparece se qualquer chave dela estiver em alguma vaga. Tecnologia
    de vaga sem categoria e erro: e assim que a lista nunca tem habilidade
    inventada nem esquecida.
    """
    usadas = {chave for vaga in vagas for chave in vaga.tecnologias}
    mapeadas = {chave for _, entradas in categorias
                for _, chaves in entradas for chave in chaves}
    sem_categoria = usadas - mapeadas
    if sem_categoria:
        raise ValueError("tecnologia sem categoria: " + ", ".join(sorted(sem_categoria)))
    resultado = []
    for nome, entradas in categorias:
        itens = [rot.em(idioma) for rot, chaves in entradas if usadas & set(chaves)]
        if itens:
            resultado.append((nome.em(idioma), ", ".join(itens)))
    return resultado
