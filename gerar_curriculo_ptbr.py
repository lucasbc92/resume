#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera o curriculo PT-BR em .docx, um arquivo por destino (Workday, Gupy,
LinkedIn, Greenhouse, sites de analise), a partir de uma fonte unica de dados.

POR QUE UM ARQUIVO POR DESTINO
------------------------------
Nao e porque os parsers sejam muito diferentes - eles nao sao. Layout de coluna
unica, sem tabela, sem caixa de texto, titulos de secao padrao, fonte sem serifa
de 10-11pt, contato fora de cabecalho/rodape e bullets consistentes sao exigidos
por todos. A unica divergencia com evidencia e o FORMATO DE DATA (ver PERFIS).
O valor de ter um arquivo por destino esta no nome do arquivo: voce sabe o que
esta subindo. O risco normal de manter varios curriculos - subir o desatualizado
- nao existe aqui porque todos saem deste mesmo arquivo.

POR QUE O DOCUMENTO E ASSIM
---------------------------
O alvo nao e "o texto sai do arquivo" - e "o parser preenche os campos certos".

  * Linha 1 = SO o nome. Linha 2 = e-mail cru, minusculo, sem rotulo: e a unica
    linha util sem nenhum token capitalizado, entao o parser que cola linha 1 com
    linha 2 nao tem de onde tirar um sobrenome errado.
  * Nenhum nome de tecnologia nas 6 primeiras linhas. Marca perto do nome vira
    sobrenome: o cabecalho antigo do index.html fazia o Workday da Accenture
    devolver "sobrenome: React", porque o NER marcava "Java Backend Engineer" e
    "Spring Boot" como entidade PESSOA.
  * Cargo pretendido isolado e rotulado, sem marca - e o que alimenta o campo
    "cargo".
  * Pretensao salarial longe do bloco de contato: "R$ 9.500-11.000" e alvo facil
    de regex gulosa de telefone/documento.
  * Sem travessao, meia-risca, aspa curva ou sinal de menos tipografico: tudo
    normalizado para ASCII. Acentos sao preservados.
  * Sem tabela, sem caixa de texto, sem coluna, sem cabecalho/rodape do Word.
    Titulos em estilo Heading real, bullets em lista real.

Validado em 15/09/2026 no autofill do Workday da Accenture: nome "Lucas",
sobrenome "Bueno Cesario".

Uso:  python gerar_curriculo_ptbr.py
"""

from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

# --------------------------------------------------------------- perfis ----
#
# "datas":
#   "mm/aaaa"  -> 11/2025 - 06/2026
#   "mmm-en"   -> Nov 2025 - Jun 2026
#
# A diferenca de data e a unica com evidencia. O Greenhouse e documentado como
# exigente com "MMM YYYY" e falha com mes por extenso; Gupy e LinkedIn sao
# nativos em mm/aaaa. Os demais campos sao iguais em todos os perfis - se dois
# arquivos saem identicos, e porque os requisitos sao identicos mesmo.

PERFIS = {
    "Workday": {
        "datas": "mmm-en",
        "salario": True,
        "txt": True,
        "nota": "Nome validado na Accenture em 15/09/2026, mas a experiencia NAO "
                "foi extraida com datas em mm/aaaa. A documentacao do Workday usa "
                "'Jun 2022 - Present', entao aqui e mmm-en. PENDENTE DE RETESTE.",
    },
    # Candidata B do reteste: identica a de Workday, so muda a abreviacao do mes
    # para portugues. O parser do Workday e americano, mas o tenant da Accenture
    # e pt-BR - e "Ago/Abr/Out/Fev" sao as unicas que divergem de "Aug/Apr/Oct/
    # Feb". Testar as duas resolve. Apagar a perdedora depois.
    "Workday-mesPT": {
        "datas": "mmm-pt",
        "salario": True,
        "txt": False,
        "nota": "Candidata B do reteste no Workday. PENDENTE.",
    },
    "Gupy": {
        "datas": "mm/aaaa",
        "salario": True,
        "txt": False,
        "nota": "Identico ao de Workday - a Gupy exige as mesmas coisas. DOCX e "
                "mais confiavel que PDF no parser Gaia.",
    },
    "LinkedIn": {
        "datas": "mm/aaaa",
        "salario": False,
        "txt": False,
        "nota": "Sem pretensao salarial: o LinkedIn importa para o perfil, que e "
                "publico.",
    },
    "Greenhouse": {
        "datas": "mmm-en",
        "salario": False,
        "txt": False,
        "nota": "Datas em MMM YYYY, que e o que o parser do Greenhouse espera. "
                "Atencao: Greenhouse e majoritariamente empresa internacional - "
                "na duvida, mande a versao em ingles, nao esta aqui.",
    },
    "Analise": {
        "datas": "mmm-en",
        "salario": False,
        "txt": True,
        "nota": "Para Jobscan, Resume Worded, SkillSyncer e afins. Sem salario, "
                "para nao poluir a contagem de keyword.",
    },
}

# ------------------------------------------------------ normalizacao -------

# Pontuacao tipografica que atrapalha tokenizador de parser. Acentos ficam.
SUBSTITUICOES = {
    "—": "-",    # travessao
    "–": "-",    # meia-risca
    "−": "-",    # sinal de menos
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "…": "...",
    " ": " ",    # espaco inquebravel
    "‑": "-",    # hifen inquebravel
    "·": "-",    # ponto medio: sozinho ja quebra "Spring Boot" em entidade
}


def limpar(texto: str) -> str:
    for de, para in SUBSTITUICOES.items():
        texto = texto.replace(de, para)
    return texto


MES_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
          "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def formatar_data(ano_mes, formato):
    ano, mes = ano_mes
    if formato == "mmm-en":
        return "{} {}".format(MES_EN[mes - 1], ano)
    if formato == "mmm-pt":
        return "{} {}".format(MES_PT[mes - 1], ano)
    return "{:02d}/{}".format(mes, ano)


def formatar_periodo(vaga, formato, duracao=False):
    """A linha de data fica limpa por padrao. O sufixo "(3 meses)" e ruido para
    o parser - ele so precisa do intervalo, e o proprio ATS calcula a duracao.
    A duracao para leitor humano continua no index.html."""
    s = "{} - {}".format(formatar_data(vaga["inicio"], formato),
                         formatar_data(vaga["fim"], formato))
    if duracao and vaga.get("duracao"):
        s += " ({})".format(vaga["duracao"])
    return s


# ---------------------------------------------------------------- dados ----

NOME = "Lucas Bueno Cesario"

# Sem marca nenhuma: e o campo que vira "cargo" no ATS.
CARGO_PRETENDIDO = "Desenvolvedor Java Full Stack Senior"

# Bloco de identidade. A ordem importa muito - ver o cabecalho deste arquivo.
# Rotulo None = linha crua (o e-mail, de proposito, sem rotulo e minusculo).
CONTATO = [
    (None, "lbc92@hotmail.com"),
    ("Telefone", "(48) 99122-4064"),
    ("WhatsApp", "(48) 99122-4064"),
    ("LinkedIn", "linkedin.com/in/lucasbc92"),
    ("GitHub", "github.com/lucasbc92"),
    ("Cidade", "Araruama"),
    ("Estado", "RJ"),
    ("Pais", "Brasil"),
    ("Cargo pretendido", CARGO_PRETENDIDO),
    ("Modelo de trabalho", "Remoto (fuso UTC-3; sobreposicao total com os EUA, "
                           "parcial com a Europa)"),
]

RESUMO = [
    "Engenheiro de software com quase 7 anos de experiência, com foco em back-end "
    "Java/Spring Boot e atuação full stack em React e Angular (JS/TS). Projetei e "
    "entreguei arquiteturas de microsserviços processando milhões de transações "
    "diárias, com bancos SQL e NoSQL e nuvem (Azure, AWS, GCP). Adoto desenvolvimento "
    "assistido por IA com Spec Driven Development (Cursor, Claude Code).",
    "Domínios: fidelidade (Vivo Valoriza), NF-e e conformidade fiscal "
    "(InvoiceCon/Cast Group e Luizalabs, reforma tributária), agronegócio (inspeção "
    "de qualidade), segurança pública (monitoramento web) e relatórios web "
    "(Canal Telecom).",
]

# Consolidacao das linhas de "Stack" de cada experiencia. Nenhuma tecnologia
# nova: tudo aqui aparece em pelo menos uma das vagas listadas abaixo.
COMPETENCIAS = [
    ("Linguagens",
     "Java (incluindo Java 21), TypeScript, JavaScript, Python, PHP, SQL"),
    ("Back-end",
     "Spring Boot, Spring MVC, Hibernate, jOOQ, APIs RESTful, Microsserviços, "
     "BFF (Backend for Frontend), Nest.js, Virtual Threads, Laravel, Zend"),
    ("Front-end",
     "React, Redux, Micro Front-ends, Angular, AngularJS, Ionic, React Native, "
     "PWA, Leaflet"),
    ("Bancos de dados",
     "PostgreSQL, Oracle Database, Azure SQL, MySQL, MongoDB, Elasticsearch"),
    ("Cloud e DevOps",
     "Azure, Azure DevOps (Boards, Repos, Pipelines), AWS (EC2, S3, RDS), GCP, "
     "Magalu Cloud, Docker, Kubernetes, ArgoCD, Jenkins, GitLab CI/CD, "
     "Azure Blob Storage, Linux, Git, SVN"),
    ("Dados e mensageria",
     "Apache Spark, Apache Airflow, RabbitMQ, Machine Learning, data lake"),
    ("Testes e qualidade",
     "JUnit, Mockito, Jest, SonarQube, Selenium, code review"),
    ("Segurança e integração",
     "JWT, Keycloak, LDAP, Apigee / API Gateway, OpenAPI, Swagger, "
     "integração com SAP"),
    ("Desenvolvimento assistido por IA",
     "Spec Driven Development, Cursor, Claude Code"),
    ("Gestão e observabilidade",
     "Azure Boards, Jira, Grafana"),
]

# Resumo curto para os metadados do arquivo (limite de 255 caracteres em OPC).
PALAVRAS_CHAVE = (
    "Java, Spring Boot, Microsservicos, APIs RESTful, React, TypeScript, Angular, "
    "Node.js, PostgreSQL, Oracle, SQL, NoSQL, Docker, Kubernetes, Azure, AWS, GCP, "
    "CI/CD, JUnit, Mockito, Python, Back-end, Full Stack, Remoto"
)

EXPERIENCIAS = [
    {
        "cargo": "Desenvolvedor Java Full Stack Sênior",
        "empresa": "Zukk Tecnologia",
        "inicio": (2025, 11), "fim": (2026, 6), "duracao": None,
        "meta": "Remoto | Contrato - cliente: Vivo/Telefónica",
        "bullets": [
            "Refatorei o sistema web de administração do Vivo Valoriza (programa de "
            "benefícios do app da Vivo), modernizando uma arquitetura distribuída com "
            "microsserviços em Java, camada de BFF (Backend for Frontend) em Nest.js "
            "e micro front-ends em React.",
            "Adotei Spec Driven Development com agentes de IA (Cursor e Claude Code) e "
            "o plugin Superpowers, aplicando fluxos de brainstorming, escrita e "
            "execução de planos para aumentar a previsibilidade e a qualidade das "
            "entregas.",
            "Conduzi o ciclo de entrega no Azure DevOps - Boards para planejamento, "
            "Repos para versionamento e Pipelines de CI/CD - e alternava entre os "
            "ambientes da Zukk e da Vivo para extrair o legado da Vivo e refatorá-lo "
            "dentro do ambiente da Zukk.",
        ],
        "stack": "Java, Microsserviços, APIs RESTful, React, Micro Front-ends, "
                 "TypeScript, Nest.js (BFF), JUnit, Mockito, Jest, Azure, "
                 "Azure DevOps, Azure SQL, Git, Spec Driven Development, Cursor, "
                 "Claude Code",
    },
    {
        "cargo": "Desenvolvedor Java Full Stack",
        "empresa": "Cast Group",
        "inicio": (2025, 8), "fim": (2025, 11), "duracao": "3 meses",
        "meta": "Remoto",
        "bullets": [
            "Atuei no desenvolvimento do InvoiceCon, solução de notas fiscais "
            "eletrônicas (NF-e), com Java Spring no back-end e Angular no front-end, "
            "contribuindo para a migração do sistema às novas regras da Reforma "
            "Tributária brasileira.",
            "Sustentei a solução no Microsoft Azure, com Azure SQL para os dados "
            "fiscais e Blob Storage para o armazenamento dos documentos, com build e "
            "deploy automatizados via GitLab CI/CD.",
            "Atuei em operações de integração com SAP e em upgrades de versão para "
            "clientes, em um sistema com controle de versionamento rigoroso.",
        ],
        "stack": "Java, Spring, APIs RESTful, SQL, integração com SAP, Angular, "
                 "TypeScript, JUnit, Mockito, SonarQube, Azure, Azure SQL, "
                 "Blob Storage, GitLab CI/CD, Git",
    },
    {
        "cargo": "Desenvolvedor Java Full Stack",
        "empresa": "Luizalabs (Magazine Luiza)",
        "inicio": (2024, 7), "fim": (2025, 4), "duracao": "10 meses",
        "meta": "São Paulo, SP",
        "bullets": [
            "Desenvolvi microsserviços financeiros em Java Spring Boot/MVC com "
            "autenticação JWT e Keycloak, processando milhões de transações diárias, "
            "e interfaces em React/TypeScript para declarações de pagamento "
            "(CPF, CNPJ).",
            "Atuei como \"bombeiro da semana\", resolvendo cards de suporte N3 e bugs "
            "críticos de produção; mantive ~95% de cobertura de código com JUnit, "
            "Mockito e SonarQube.",
            "Construí APIs RESTful com Apigee/API Gateway (OpenAPI) e mantive "
            "pipelines de dados com Python, Apache Spark e Apache Airflow, incluindo "
            "a repopulação do data lake a partir do Oracle EBS.",
            "Otimizei o processamento em lote de faturas com Virtual Threads "
            "(Java 21), reduzindo a importação de ~100 mil registros de vários "
            "minutos para cerca de um minuto.",
            "Tive contato com RabbitMQ, usado no time para reprocessamento manual de "
            "mensagens com falha na fila.",
        ],
        "stack": "Java 21, Virtual Threads, Spring Boot, Spring MVC, Hibernate, JWT, "
                 "Keycloak, Microsserviços, RabbitMQ, Apigee, React, TypeScript, "
                 "JUnit, Mockito, Jest, SonarQube, Oracle Database, Python, "
                 "Apache Spark, Apache Airflow, Docker, Kubernetes, ArgoCD, Grafana, "
                 "GCP, Magalu Cloud",
    },
    {
        "cargo": "Desenvolvedor Java Full Stack",
        "empresa": "PariPassu",
        "inicio": (2022, 8), "fim": (2024, 4), "duracao": "1 ano e 9 meses",
        "meta": "Florianópolis, SC",
        "bullets": [
            "Arquitetei e desenvolvi o CLICQ, sistema de inspeção de qualidade "
            "alimentar para toda a cadeia (do produtor ao varejo), com backend "
            "Spring Boot e frontend React/Redux/TypeScript, além de versões legadas "
            "em AngularJS, Angular 8/Ionic e mobile em React Native.",
            "Construí uma ferramenta de predição de churn com Machine Learning "
            "(Python), acessível via bot do Discord, reduzindo o churn de clientes "
            "em 18%.",
            "Atuei como \"bombeiro da semana\" na prevenção e correção de bugs, com "
            "apoio ao suporte N2, monitoramento via Grafana e testes manuais; não "
            "havia suíte de testes automatizados, mas mantínhamos uma política forte "
            "de code review - nenhum código ia para produção sem aprovação de dois "
            "colegas revisores.",
        ],
        "stack": "Java, Spring Boot, jOOQ, Swagger, React, Redux, TypeScript, "
                 "Angular, Ionic, React Native, PostgreSQL, Python, "
                 "Machine Learning, AWS (EC2, S3, RDS), Jenkins, Grafana, Jira",
    },
    {
        "cargo": "Desenvolvedor PHP Full Stack",
        "empresa": "Secretaria de Segurança Pública",
        "inicio": (2020, 10), "fim": (2022, 7), "duracao": "1 ano e 10 meses",
        "meta": "Florianópolis, SC",
        "bullets": [
            "Desenvolvi o PWA Bem-Te-Vi App em React e Leaflet, com mapa interativo "
            "de quase cinco mil câmeras de segurança de Santa Catarina, visualização "
            "ao vivo e download de gravações para policiais do estado.",
            "Mantive sistemas legados de segurança (Bem-Te-Vi e BRAVO) em PHP com "
            "autenticação LDAP.",
            "Usei RabbitMQ para processamento assíncrono de SMS de ocorrências de "
            "placas monitoradas.",
            "Integrei Elasticsearch para busca de texto completo.",
        ],
        "stack": "PHP, Laravel, LDAP, APIs REST, React, JavaScript, Leaflet, PWA, "
                 "PostgreSQL, Elasticsearch, RabbitMQ, Selenium, Git",
    },
    {
        "cargo": "Desenvolvedor PHP Full Stack Júnior",
        "empresa": "Canal Telecom",
        "inicio": (2018, 2), "fim": (2018, 11), "duracao": "10 meses",
        "meta": "São José, SC",
        "bullets": [
            "Desenvolvi interfaces de relatórios web em PHP/JavaScript.",
            "Participei de uma migração de banco de dados de SQL para NoSQL "
            "(MongoDB).",
            "Dei manutenção no sistema de backups da empresa, trabalhando com "
            "comandos Linux/Debian (rsync) para as rotinas de backup.",
        ],
        "stack": "PHP, Zend, JavaScript, PostgreSQL, MySQL, MongoDB, Linux, rsync, "
                 "SVN",
    },
]

FORMACAO = [
    {
        "curso": "Bacharelado em Ciência da Computação",
        "instituicao": "Universidade Federal de Santa Catarina (UFSC)",
        "conclusao": (2026, 12),
    },
]

CERTIFICACOES = [
    "DEVinHouse - Formação Full Stack React e Java (900h) - SENAI/SC, 2022",
    "Competências Profissionais, Emocionais e Tecnológicas para Tempos de Mudança "
    "- PUC/RS, 2023",
]

IDIOMAS = [
    ("Português", "nativo"),
    ("Inglês", "proficiência profissional - leitura e escrita fluentes, conversação "
               "proficiente; uso diário em documentação e code review"),
    ("Espanhol", "básico"),
]

DISPONIBILIDADE = ("Disponibilidade", "imediata, para trabalho 100% remoto")

# Longe do bloco de contato de proposito: valores em reais perto do telefone
# sao capturados por regex gulosa de telefone/documento.
SALARIO = ("Pretensão salarial",
           "R$ 9.500 a R$ 11.000 por mês (CLT) ou R$ 13.000 a R$ 15.000 por mês (PJ)")

# ---------------------------------------------------------------- docx -----

FONTE = "Arial"
PRETO = RGBColor(0, 0, 0)


def _forcar_fonte(run):
    """Fixa a fonte tambem para complex-script/east-asian, senao o Word troca a
    fonte de trechos acentuados em alguns ambientes."""
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONTE)


def _estilar(run, tamanho, negrito=False, italico=False):
    run.font.name = FONTE
    run.font.size = Pt(tamanho)
    run.font.bold = negrito
    run.font.italic = italico
    run.font.color.rgb = PRETO
    _forcar_fonte(run)
    return run


def _p(doc, texto="", tamanho=10, negrito=False, italico=False,
       espaco_antes=0, espaco_depois=2, estilo=None):
    par = doc.add_paragraph(style=estilo)
    par.paragraph_format.space_before = Pt(espaco_antes)
    par.paragraph_format.space_after = Pt(espaco_depois)
    par.paragraph_format.line_spacing = 1.08
    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if texto:
        _estilar(par.add_run(limpar(texto)), tamanho, negrito, italico)
    return par


def _p_rotulado(doc, rotulo, valor, tamanho=10, espaco_depois=2):
    """Paragrafo unico 'Rotulo: valor'. Um paragrafo so garante que a extracao
    devolva o rotulo e o valor na mesma linha."""
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(0)
    par.paragraph_format.space_after = Pt(espaco_depois)
    par.paragraph_format.line_spacing = 1.08
    _estilar(par.add_run(limpar(rotulo) + ": "), tamanho, negrito=True)
    _estilar(par.add_run(limpar(valor)), tamanho)
    return par


def _secao(doc, titulo):
    """Titulo de secao em estilo 'Heading 1' real: o nome do estilo e o que
    muitos parsers usam para delimitar as secoes."""
    par = doc.add_paragraph(style="Heading 1")
    par.paragraph_format.space_before = Pt(12)
    par.paragraph_format.space_after = Pt(4)
    _estilar(par.add_run(limpar(titulo).upper()), 11.5, negrito=True)

    ppr = par._p.get_or_add_pPr()
    pbdr = ppr.makeelement(qn("w:pBdr"), {})
    bottom = pbdr.makeelement(qn("w:bottom"), {})
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    pbdr.append(bottom)
    ppr.append(pbdr)
    return par


def _bullet(doc, texto):
    par = doc.add_paragraph(style="List Bullet")
    par.paragraph_format.space_before = Pt(0)
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.line_spacing = 1.08
    par.paragraph_format.left_indent = Cm(0.63)
    _estilar(par.add_run(limpar(texto)), 10)
    return par


def _adicionais(perfil):
    itens = [DISPONIBILIDADE]
    if PERFIS[perfil]["salario"]:
        itens.insert(0, SALARIO)
    return itens


def gerar_docx(caminho: Path, perfil: str) -> Path:
    cfg = PERFIS[perfil]
    doc = Document()

    secao = doc.sections[0]
    secao.top_margin = Cm(1.6)
    secao.bottom_margin = Cm(1.6)
    secao.left_margin = Cm(1.9)
    secao.right_margin = Cm(1.9)

    normal = doc.styles["Normal"]
    normal.font.name = FONTE
    normal.font.size = Pt(10)
    normal.font.color.rgb = PRETO
    rfonts = normal.element.rPr.rFonts
    rfonts.set(qn("w:eastAsia"), FONTE)
    rfonts.set(qn("w:cs"), FONTE)

    # Linha 1: SO o nome. Linha 2: e-mail cru. Nenhuma marca ate a linha 7.
    # Cabecalho como paragrafo normal, nunca no header do Word - boa parte dos
    # ATS descarta o conteudo de cabecalho/rodape.
    _p(doc, NOME, tamanho=20, negrito=True, espaco_depois=4)

    for rotulo, valor in CONTATO:
        if rotulo is None:
            _p(doc, valor, espaco_depois=1)
        else:
            _p_rotulado(doc, rotulo, valor, espaco_depois=1)

    _secao(doc, "Resumo profissional")
    for paragrafo in RESUMO:
        _p(doc, paragrafo, espaco_depois=4)

    _secao(doc, "Competências técnicas")
    for rotulo, valor in COMPETENCIAS:
        _p_rotulado(doc, rotulo, valor, espaco_depois=1)

    _secao(doc, "Experiência profissional")
    for i, vaga in enumerate(EXPERIENCIAS):
        # Quatro linhas, uma informacao por linha, nesta ordem.
        #
        # O cargo NAO usa estilo Heading, so negrito. Estilo de titulo e o que o
        # parser usa para delimitar SECAO; com cada vaga marcada como Heading 2 o
        # bloco de experiencia se fragmenta e o Workday nao monta o historico.
        # Foi assim que a extracao de experiencia falhou na Accenture.
        #
        # A data fica sozinha e imediatamente acima dos bullets: e a ancora que o
        # parser usa para fechar o registro da vaga.
        _p(doc, vaga["cargo"], tamanho=11, negrito=True,
           espaco_antes=8 if i else 4, espaco_depois=0)
        _p(doc, vaga["empresa"], espaco_depois=0)
        _p(doc, vaga["meta"], espaco_depois=0)
        _p(doc, formatar_periodo(vaga, cfg["datas"]), espaco_depois=3)
        for bullet in vaga["bullets"]:
            _bullet(doc, bullet)
        _p_rotulado(doc, "Tecnologias", vaga["stack"], tamanho=9.5)

    _secao(doc, "Formação acadêmica")
    for curso in FORMACAO:
        _p(doc, curso["curso"], tamanho=11, negrito=True, espaco_depois=0)
        _p(doc, curso["instituicao"], espaco_depois=0)
        _p(doc, "Conclusão prevista: "
                + formatar_data(curso["conclusao"], cfg["datas"]), espaco_depois=2)

    _secao(doc, "Certificações")
    for cert in CERTIFICACOES:
        _bullet(doc, cert)

    _secao(doc, "Idiomas")
    for idioma, nivel in IDIOMAS:
        _p_rotulado(doc, idioma, nivel, espaco_depois=1)

    _secao(doc, "Informações adicionais")
    for rotulo, valor in _adicionais(perfil):
        _p_rotulado(doc, rotulo, valor, espaco_depois=1)

    # Metadados: varios parsers leem dc:creator / dc:title antes do corpo, e sao
    # o canal que carrega o sobrenome completo quando o parser e baseado em NER.
    doc.core_properties.author = NOME
    doc.core_properties.last_modified_by = NOME
    doc.core_properties.title = NOME + " - Curriculo"
    doc.core_properties.subject = CARGO_PRETENDIDO
    doc.core_properties.category = CARGO_PRETENDIDO
    doc.core_properties.language = "pt-BR"
    doc.core_properties.keywords = PALAVRAS_CHAVE[:255]

    doc.save(str(caminho))
    return caminho


# ----------------------------------------------------------------- txt -----

def gerar_txt(caminho: Path, perfil: str) -> Path:
    cfg = PERFIS[perfil]
    linhas = [NOME]
    for rotulo, valor in CONTATO:
        linhas.append(valor if rotulo is None else rotulo + ": " + valor)

    def secao(titulo):
        linhas.extend(["", titulo.upper(), "=" * len(titulo)])

    secao("Resumo profissional")
    for paragrafo in RESUMO:
        linhas.extend([paragrafo, ""])
    linhas.pop()

    secao("Competências técnicas")
    for rotulo, valor in COMPETENCIAS:
        linhas.append(rotulo + ": " + valor)

    secao("Experiência profissional")
    for vaga in EXPERIENCIAS:
        linhas.extend(["", vaga["cargo"], vaga["empresa"], vaga["meta"],
                       formatar_periodo(vaga, cfg["datas"])])
        for bullet in vaga["bullets"]:
            linhas.append("- " + bullet)
        linhas.append("Tecnologias: " + vaga["stack"])

    secao("Formação acadêmica")
    for curso in FORMACAO:
        linhas.extend([curso["curso"], curso["instituicao"],
                       "Conclusão prevista: "
                       + formatar_data(curso["conclusao"], cfg["datas"])])

    secao("Certificações")
    for cert in CERTIFICACOES:
        linhas.append("- " + cert)

    secao("Idiomas")
    for idioma, nivel in IDIOMAS:
        linhas.append(idioma + ": " + nivel)

    secao("Informações adicionais")
    for rotulo, valor in _adicionais(perfil):
        linhas.append(rotulo + ": " + valor)

    caminho.write_text(limpar("\n".join(linhas)) + "\n", encoding="utf-8")
    return caminho


# ---------------------------------------------------------------- main -----

MESES_ABREV = ["jan", "fev", "mar", "abr", "mai", "jun",
               "jul", "ago", "set", "out", "nov", "dez"]

# O nome do arquivo e sinal de verdade para varios parsers: e a primeira coisa
# que eles usam para conferir o nome extraido do corpo. Por isso o nome completo
# vem primeiro, nao "resume_".
BASE = "Lucas-Bueno-Cesario-Curriculo"

# Perfil arquivado com data, seguindo a convencao dos PDFs do repositorio.
PERFIL_ARQUIVO = "Workday"


def main():
    raiz = Path(__file__).resolve().parent
    hoje = date.today()

    saidas = []
    for perfil in PERFIS:
        saidas.append(gerar_docx(raiz / "{}-{}.docx".format(BASE, perfil), perfil))
        if PERFIS[perfil]["txt"]:
            saidas.append(gerar_txt(raiz / "{}-{}.txt".format(BASE, perfil), perfil))

    datado = "resume_lucas-bueno-cesario_ptbr_{:%Y-%m-%d}_{}.docx".format(
        hoje, MESES_ABREV[hoje.month - 1])
    saidas.append(gerar_docx(raiz / datado, PERFIL_ARQUIVO))

    largura = max(len(c.name) for c in saidas)
    for caminho in saidas:
        print("{:<{w}}  {:>7,} bytes".format(
            caminho.name, caminho.stat().st_size, w=largura))


if __name__ == "__main__":
    main()
