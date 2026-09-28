# -*- coding: utf-8 -*-
"""
FONTE UNICA do curriculo. Edite so este arquivo e rode, nesta pasta:

    python gerar.py

Daqui saem a versao ATS (DOCX/TXT, ats.py) e a versao humana (PDF e
index.html, humano.py), em portugues e ingles. index.html e os PDFs sao
GERADOS: mudanca feita a mao neles some na proxima geracao.

Regras de conteudo:
  * Nada aqui que nao se sustente em entrevista. Kafka, Service Bus, Cosmos DB,
    Golang e Fortify ficam de fora; verificar.py falha se aparecerem.
  * Carreira: 7 anos (desde fev/2018). Java: 4 anos (desde ago/2022).
  * Toda tecnologia de uma vaga precisa ter entrada em CATEGORIAS.
  * stack_humano: ate 8 itens, todos presentes em tecnologias da mesma vaga.
    Item = chave, ou (chave, nome exibido) para encurtar so na versao humana.
  * A pagina 1 do PDF em PT esta a poucos pixels do limite: uma linha a mais
    nas vagas Java empurra a PariPassu para a pagina 2 e o verificador falha.
    Nesse caso, enxugue texto ou o espacamento em templates/humano.html.j2.
"""

from modelo import B, IGUAL, Formacao, T, Vaga

NOME = "Lucas Bueno Cesario"
EMAIL = "lbc92@hotmail.com"
LINKEDIN = "linkedin.com/in/lucasbc92"
GITHUB = "github.com/lucasbc92"
WHATSAPP_LINK = "https://wa.me/5548991224064"
TELEFONE = T("(48) 99122-4064", "+55 48 99122-4064")

# Sem marca nenhuma: e o campo que vira "cargo" no ATS.
CARGO_ALVO = T("Desenvolvedor Java Full Stack Pleno/Sênior", "Full Stack Java Developer")

# Bloco de identidade do ATS, nesta ordem, logo abaixo do nome e do e-mail.
# Nenhuma tecnologia nas 6 primeiras linhas do documento (ver ats.py).
CONTATO_ATS = (
    (T("Telefone", "Phone"), TELEFONE),
    (T("WhatsApp", "WhatsApp"), TELEFONE),
    (T("LinkedIn", "LinkedIn"), T(LINKEDIN, LINKEDIN)),
    (T("GitHub", "GitHub"), T(GITHUB, GITHUB)),
    (T("Cidade", "City"), T("Araruama", "Araruama")),
    (T("Estado", "State"), T("RJ", "RJ")),
    (T("País", "Country"), T("Brasil", "Brazil")),
    (T("Cargo pretendido", "Target role"), CARGO_ALVO),
    (T("Modelo de trabalho", "Work model"),
     T("Remoto (fuso UTC-3; sobreposição total com os EUA, parcial com a Europa)",
       "Remote (UTC-3; full overlap with US time zones, partial with Europe)")),
)

# ------------------------------------------------------------- resumos ----

RESUMO_ATS = T(
    "Desenvolvedor Java Full Stack Pleno/Sênior com 7 anos de carreira, 4 deles em "
    "Java (8 a 21) com Spring Boot, Spring Data JPA/Hibernate e Maven. Microsserviços "
    "e APIs REST em sistemas críticos: milhões de transações financeiras diárias na "
    "Luizalabs (Magazine Luiza), notas fiscais eletrônicas (NF-e) na Cast Group e o "
    "programa de fidelidade da Vivo. Front-end em Angular e React com TypeScript; SQL "
    "com Oracle, PostgreSQL e Azure SQL; Docker, Kubernetes e CI/CD (Azure DevOps, "
    "GitLab CI/CD, Jenkins); nuvem Azure, AWS e GCP; testes com JUnit e Mockito; Scrum "
    "e Kanban. Desenvolvimento assistido por IA com Spec Driven Development (Cursor, "
    "Claude Code).",
    "Full Stack Java Developer with 7 years of experience, 4 of them in Java (8 to 21) "
    "with Spring Boot, Spring Data JPA/Hibernate and Maven. Microservices and REST APIs "
    "for critical systems: millions of daily financial transactions at Luizalabs "
    "(Magazine Luiza), electronic invoicing (NF-e) at Cast Group and Vivo's loyalty "
    "program. Front-end in Angular and React with TypeScript; SQL with Oracle, "
    "PostgreSQL and Azure SQL; Docker, Kubernetes and CI/CD (Azure DevOps, GitLab "
    "CI/CD, Jenkins); Azure, AWS and GCP cloud; testing with JUnit and Mockito; Scrum "
    "and Kanban. AI-assisted development with Spec Driven Development (Cursor, Claude "
    "Code).",
)

DOMINIOS = T(
    "Domínios: fidelidade (Vivo Valoriza), NF-e e conformidade fiscal (InvoiceCon/Cast "
    "Group e Luizalabs, reforma tributária), agronegócio (inspeção de qualidade), "
    "segurança pública (monitoramento web) e relatórios web (Canal Telecom).",
    "Domains: loyalty programs (Vivo Valoriza), e-invoicing and tax compliance "
    "(InvoiceCon/Cast Group and Luizalabs, Brazilian tax reform), agribusiness quality "
    "inspection, public safety monitoring, and web reporting (Canal Telecom).",
)

# Caixa de sentenca de proposito: em Title Case o parser marcava o titulo como
# nome de PESSOA (Workday da Accenture devolvia "sobrenome: React").
TITULO_HUMANO = T(
    "Desenvolvedor Java full stack pleno/sênior \u2014 back-end em Spring Boot, "
    "front-end em Angular e React",
    "Full Stack Java developer \u2014 Spring Boot back-end, Angular and React front-end",
)

LOCAL_HUMANO = T("Araruama, RJ \u00b7 remoto (UTC-3)",
                 "Araruama, RJ, Brazil \u00b7 remote (UTC-3)")

RESUMO_HUMANO = T(
    "Full Stack com 7 anos de carreira, 4 deles em Java com Spring Boot. Construo e "
    "sustento sistemas críticos \u2014 milhões de transações financeiras na Luizalabs, "
    "notas fiscais na Cast Group, o programa de fidelidade da Vivo \u2014 do banco de "
    "dados à tela em React ou Angular.",
    "Full Stack developer with 7 years in the industry, 4 of them in Java with Spring "
    "Boot. I build and maintain critical systems \u2014 millions of financial "
    "transactions at Luizalabs, e-invoicing at Cast Group, Vivo's loyalty program "
    "\u2014 from the database to the UI in React or Angular.",
)

DESTAQUES = (
    T("Importação de ~100 mil faturas de <b>mais de 10 min para ~1 min</b>, com "
      "upgrade para Java 21 e Virtual Threads",
      "Import of ~100k invoices cut from <b>over 10 min to ~1 min</b> by upgrading to "
      "Java 21 and Virtual Threads"),
    T("Microsserviços financeiros com <b>milhões de transações por dia</b> e "
      "<b>~95% de cobertura</b> de testes",
      "Financial microservices handling <b>millions of transactions a day</b> with "
      "<b>~95% test coverage</b>"),
    T("Churn de clientes reduzido em <b>18%</b> com modelo preditivo em Python",
      "Customer churn cut by <b>18%</b> with a predictive model in Python"),
)

# ---------------------------------------------------------- experiencia ----

EXPERIENCIAS = (
    Vaga(
        cargo=T("Desenvolvedor Java Full Stack Sênior", "Senior Full Stack Java Developer"),
        empresa=T("Zukk Tecnologia", "Zukk Tecnologia"),
        cliente=T("alocado na Vivo/Telefónica", "placed at Vivo/Telefónica"),
        inicio=(2025, 11), fim=(2026, 6),
        meta_ats=T("Remoto | Contrato - cliente: Vivo/Telefónica",
                   "Remote | Contract - client: Vivo/Telefónica"),
        local=T("Remoto", "Remote"),
        contexto=T("Vivo Valoriza, o programa de benefícios do app da Vivo.",
                   "Vivo Valoriza, the benefits program inside Vivo's mobile app."),
        bullets=(
            B(ats=T("Refatorei o sistema web de administração do Vivo Valoriza (programa de "
                    "benefícios do app da Vivo), modernizando uma arquitetura distribuída "
                    "com microsserviços em Java e Spring Boot, camada de BFF (Backend for "
                    "Frontend) em NestJS (Node.js), micro front-ends em React e mensageria "
                    "em RabbitMQ.",
                    "Refactored the Vivo Valoriza web administration system (the benefits "
                    "program inside Vivo's app), modernizing a distributed architecture with "
                    "Java and Spring Boot microservices, a BFF (Backend for Frontend) layer "
                    "in NestJS (Node.js), React micro front-ends, and RabbitMQ messaging."),
              humano=T("Refatorei o sistema de administração do programa: microsserviços "
                       "Java/Spring, BFF em NestJS e micro front-ends em React, com "
                       "mensageria em RabbitMQ.",
                       "Refactored the program's administration system: Java/Spring "
                       "microservices, a NestJS BFF and React micro front-ends, with "
                       "RabbitMQ messaging.")),
            B(ats=T("Adotei Spec Driven Development com agentes de IA (Cursor e Claude Code), "
                    "com especificação, plano e execução revisados em cada etapa para "
                    "aumentar a previsibilidade e a qualidade das entregas.",
                    "Adopted Spec Driven Development with AI agents (Cursor and Claude "
                    "Code), with specification, plan and execution reviewed at each step to "
                    "increase delivery predictability and quality."),
              humano=T("Entreguei por Spec Driven Development com agentes de IA (Cursor, "
                       "Claude Code): especificação e plano revisados antes de cada linha "
                       "de código.",
                       "Delivered through Spec Driven Development with AI agents (Cursor, "
                       "Claude Code): specification and plan reviewed before any code was "
                       "written.")),
            B(ats=T("Conduzi o ciclo de entrega no Azure DevOps: Boards para planejamento, "
                    "Repos para versionamento com Git flow e code review, e Pipelines de "
                    "CI/CD.",
                    "Drove the delivery cycle on Azure DevOps: Boards for planning, Repos for "
                    "version control with Git flow and code review, and CI/CD Pipelines."),
              humano=T("Ciclo de entrega completo no Azure DevOps \u2014 Boards, Repos e "
                       "Pipelines de CI/CD.",
                       "Full delivery cycle on Azure DevOps \u2014 Boards, Repos and CI/CD "
                       "Pipelines.")),
        ),
        tecnologias=("Java", "Spring Boot", "Spring Data JPA", "Maven", "Microsserviços",
                     "APIs RESTful", "RabbitMQ", "NestJS", "Node.js", "BFF", "React",
                     "Micro Front-ends", "TypeScript", "JUnit", "Mockito", "Jest", "Docker",
                     "Azure", "Azure DevOps", "Azure SQL", "Git", "Git flow", "Scrum",
                     "Kanban", "Spec Driven Development", "Cursor", "Claude Code"),
        stack_humano=("Java", "Spring Boot", "NestJS", "React", "TypeScript", "RabbitMQ",
                      "Azure SQL", "Azure DevOps"),
    ),
    Vaga(
        cargo=T("Desenvolvedor Java Full Stack", "Full Stack Java Developer"),
        empresa=T("Cast Group", "Cast Group"),
        inicio=(2025, 8), fim=(2025, 11),
        meta_ats=T("Remoto", "Remote"),
        local=T("Remoto", "Remote"),
        contexto=T("InvoiceCon, solução de notas fiscais eletrônicas (NF-e).",
                   "InvoiceCon, an electronic invoicing (NF-e) product."),
        bullets=(
            B(ats=T("Atuei no desenvolvimento do InvoiceCon, solução de notas fiscais "
                    "eletrônicas (NF-e), com Java e Spring Boot no back-end e Angular 8 no "
                    "front-end, contribuindo para a migração do sistema às novas regras da "
                    "Reforma Tributária brasileira.",
                    "Worked on InvoiceCon, an electronic invoicing (NF-e) solution, with Java "
                    "and Spring Boot on the back-end and Angular 8 on the front-end, "
                    "contributing to the system's migration to the new rules of the "
                    "Brazilian Tax Reform."),
              humano=T("Trabalhei na migração do InvoiceCon para as regras da Reforma "
                       "Tributária, com Java Spring no back-end e Angular 8 no front-end.",
                       "Worked on migrating InvoiceCon to the Brazilian Tax Reform rules, "
                       "with Java Spring on the back-end and Angular 8 on the front-end.")),
            B(ats=T("Sustentei a solução no Microsoft Azure, com Azure SQL para os dados "
                    "fiscais e Blob Storage para o armazenamento dos documentos, com build e "
                    "deploy automatizados via GitLab CI/CD.",
                    "Ran the solution on Microsoft Azure, using Azure SQL for fiscal data and "
                    "Blob Storage for invoice documents, with build and deployment automated "
                    "through GitLab CI/CD.")),
            B(ats=T("Atuei em operações de integração com SAP e em upgrades de versão para "
                    "clientes, em um sistema com controle de versionamento rigoroso.",
                    "Worked on SAP integration operations and client version upgrades, in a "
                    "system with rigorous version control."),
              humano=T("Integrações com SAP e upgrades de versão em clientes, sob controle "
                       "de versionamento rigoroso.",
                       "SAP integrations and client version upgrades under rigorous version "
                       "control.")),
        ),
        tecnologias=("Java", "Spring Boot", "Spring Data JPA", "Maven", "APIs RESTful", "SQL",
                     "SAP", "Angular 8", "TypeScript", "JUnit", "Mockito", "SonarQube",
                     "Docker", "Azure", "Azure SQL", "Blob Storage", "GitLab CI/CD", "Git",
                     "Git flow", "Scrum", "Kanban"),
        stack_humano=("Java", "Spring Boot", "Angular 8", "TypeScript", "SQL", "SAP", "Azure",
                      "GitLab CI/CD"),
    ),
    Vaga(
        cargo=T("Desenvolvedor Java Full Stack", "Full Stack Java Developer"),
        empresa=T("Luizalabs (Magazine Luiza)", "Luizalabs (Magazine Luiza)"),
        inicio=(2024, 7), fim=(2025, 4),
        meta_ats=T("São Paulo, SP", "São Paulo, Brazil"),
        local=T("São Paulo, SP", "São Paulo, Brazil"),
        contexto=T("Time de sistemas financeiros do Magazine Luiza.",
                   "Magazine Luiza's financial systems team."),
        bullets=(
            B(ats=T("Conduzi o upgrade da JVM de 17 para 21 e reescrevi com Virtual Threads "
                    "a importação em lote de ~100 mil faturas: de mais de 10 minutos para "
                    "cerca de 1 minuto.",
                    "Upgraded the JVM from 17 to 21 and rewrote the batch import of ~100k "
                    "invoices with Virtual Threads: from over 10 minutes to about 1 minute."),
              humano=IGUAL),
            B(ats=T("Desenvolvi microsserviços financeiros em Java, Spring Boot e Spring MVC "
                    "com Spring Data JPA/Hibernate sobre Oracle, autenticação JWT e Keycloak, "
                    "processando milhões de transações financeiras diárias, e interfaces em "
                    "React/TypeScript para declarações de pagamento (CPF, CNPJ).",
                    "Developed financial microservices in Java, Spring Boot and Spring MVC "
                    "with Spring Data JPA/Hibernate over Oracle and JWT and Keycloak "
                    "authentication, processing millions of daily financial transactions, "
                    "plus React/TypeScript interfaces for payment declarations (CPF, CNPJ)."),
              humano=T("Microsserviços financeiros em Spring Boot com milhões de transações "
                       "por dia, autenticação JWT/Keycloak e APIs publicadas no Apigee; "
                       "telas de declaração de pagamento em React.",
                       "Financial microservices in Spring Boot handling millions of "
                       "transactions a day, with JWT/Keycloak authentication and APIs "
                       "published on Apigee; payment declaration screens in React.")),
            B(ats=T("Atuei como \"bombeiro da semana\", resolvendo incidentes críticos de "
                    "produção e cards de suporte N3 com observabilidade no Grafana; mantive "
                    "~95% de cobertura de código com JUnit, Mockito e SonarQube.",
                    "Owned the weekly on-call rotation, resolving critical production "
                    "incidents and L3 (N3) support tickets with observability in Grafana; "
                    "sustained ~95% code coverage with JUnit, Mockito and SonarQube."),
              humano=T("\u201cBombeiro da semana\u201d: incidentes críticos de produção e "
                       "suporte N3, com ~95% de cobertura de testes (JUnit, Mockito, "
                       "SonarQube).",
                       "Weekly on-call rotation: critical production incidents and L3 (N3) "
                       "support, with ~95% test coverage (JUnit, Mockito, SonarQube).")),
            B(ats=T("Construí APIs RESTful publicadas no Apigee (API Gateway) com contrato "
                    "OpenAPI e mantive pipelines de dados com Python, Apache Spark e Apache "
                    "Airflow, incluindo a repopulação do data lake a partir do Oracle EBS.",
                    "Built RESTful APIs published on Apigee (API Gateway) with OpenAPI "
                    "contracts and maintained data pipelines with Python, Apache Spark and "
                    "Apache Airflow, including repopulating the data lake from Oracle EBS.")),
        ),
        tecnologias=("Java 21", "Virtual Threads", "Spring Boot", "Spring MVC",
                     "Spring Data JPA", "Hibernate", "Maven", "Microsserviços",
                     "APIs RESTful", "JWT", "Keycloak", "RabbitMQ", "Apigee", "OpenAPI",
                     "React", "TypeScript", "JUnit", "Mockito", "Jest", "SonarQube",
                     "Oracle Database", "Python", "Apache Spark", "Apache Airflow", "Docker",
                     "Kubernetes", "ArgoCD", "Grafana", "GCP", "Magalu Cloud", "Git",
                     "Git flow", "Scrum", "Kanban"),
        stack_humano=("Java 21", "Spring Boot", "Spring Data JPA", ("Oracle Database", "Oracle"),
                      "React", "TypeScript", "Kubernetes", "GCP"),
    ),
    Vaga(
        cargo=T("Desenvolvedor Java Full Stack", "Full Stack Java Developer"),
        empresa=T("PariPassu", "PariPassu"),
        inicio=(2022, 8), fim=(2024, 4),
        meta_ats=T("Florianópolis, SC", "Florianópolis, Brazil"),
        local=T("Florianópolis, SC", "Florianópolis, Brazil"),
        contexto=T("CLICQ, sistema de inspeção de qualidade de alimentos, do produtor ao "
                   "varejo.",
                   "CLICQ, a food quality inspection system covering the chain from "
                   "producers to retail."),
        bullets=(
            B(ats=T("Arquitetei e desenvolvi o CLICQ, sistema de inspeção de qualidade "
                    "alimentar para toda a cadeia (do produtor ao varejo), com back-end em "
                    "Java 8 e Spring Boot e front-end em React/Redux/TypeScript, além de "
                    "versões legadas em AngularJS e Angular 8/Ionic e app mobile em React "
                    "Native com autenticação OAuth2.",
                    "Architected and developed CLICQ, a food quality inspection system "
                    "covering the entire supply chain (from producers to retail), with a "
                    "Java 8 and Spring Boot back-end and a React/Redux/TypeScript front-end, "
                    "plus legacy versions in AngularJS and Angular 8/Ionic and a React "
                    "Native mobile app with OAuth2 authentication."),
              humano=T("Arquitetei e desenvolvi o CLICQ: Spring Boot no back-end, "
                       "React/TypeScript no front-end e app em React Native com login OAuth2.",
                       "Architected and built CLICQ: Spring Boot back-end, React/TypeScript "
                       "front-end and a React Native app with OAuth2 login.")),
            B(ats=T("Construí uma ferramenta de predição de churn com Machine Learning "
                    "(Python), acessível via bot do Discord, reduzindo o churn de clientes "
                    "em 18%.",
                    "Built a churn prediction tool with Machine Learning (Python), accessible "
                    "through a Discord bot, reducing customer churn by 18%."),
              humano=T("Criei uma ferramenta de predição de churn em Python, consultada por "
                       "bot no Discord, que reduziu o churn de clientes em 18%.",
                       "Built a churn prediction tool in Python, queried through a Discord "
                       "bot, that cut customer churn by 18%.")),
            B(ats=T("Atuei como \"bombeiro da semana\" na prevenção e correção de bugs, com "
                    "apoio ao suporte N2, monitoramento via Grafana e testes manuais; não "
                    "havia suíte de testes automatizados, mas o time seguia Git flow com "
                    "code review obrigatório: nenhum código ia para produção sem aprovação "
                    "de dois colegas revisores.",
                    "Owned the weekly on-call rotation, preventing and fixing defects with "
                    "L2 (N2) support, Grafana monitoring and manual testing; there was no "
                    "automated test suite, but the team followed Git flow with mandatory "
                    "code review: no code shipped to production without approval from two "
                    "reviewers."),
              humano=T("Plantão de bugs e suporte N2 com monitoramento no Grafana; code "
                       "review obrigatório com dois aprovadores antes de produção.",
                       "Bug on-call and L2 (N2) support with Grafana monitoring; mandatory code "
                       "review with two approvers before production.")),
        ),
        tecnologias=("Java 8", "Spring Boot", "Spring Data JPA", "jOOQ", "Maven", "Swagger",
                     "OAuth2", "React", "Redux", "TypeScript", "Angular 8", "AngularJS",
                     "Ionic", "React Native", "PostgreSQL", "Python", "Machine Learning",
                     "Docker", "AWS (EC2, S3, RDS)", "Jenkins", "Grafana", "Jira", "Git",
                     "Git flow", "Scrum", "Kanban"),
        stack_humano=("Java 8", "Spring Boot", "jOOQ", "PostgreSQL", "React",
                      ("Angular 8", "Angular"), "React Native", ("AWS (EC2, S3, RDS)", "AWS")),
    ),
    Vaga(
        cargo=T("Desenvolvedor PHP Full Stack", "Full Stack PHP Developer"),
        empresa=T("Secretaria de Segurança Pública de SC",
                  "Santa Catarina Department of Public Safety"),
        inicio=(2020, 10), fim=(2022, 7),
        meta_ats=T("Florianópolis, SC", "Florianópolis, Brazil"),
        local=T("Florianópolis, SC", "Florianópolis, Brazil"),
        bullets=(
            B(ats=T("Desenvolvi o PWA Bem-Te-Vi App em React e Leaflet, com mapa interativo "
                    "de quase cinco mil câmeras de segurança de Santa Catarina, visualização "
                    "ao vivo e download de gravações para policiais do estado.",
                    "Developed the Bem-Te-Vi App PWA in React and Leaflet, featuring an "
                    "interactive map of nearly five thousand security cameras across Santa "
                    "Catarina, with live viewing and recording downloads for state police "
                    "officers."),
              humano=T("Criei o Bem-Te-Vi App, PWA em React com mapa de quase 5 mil câmeras "
                       "de segurança do estado, vídeo ao vivo e download de gravações para a "
                       "polícia.",
                       "Built the Bem-Te-Vi App, a React PWA mapping nearly 5,000 state "
                       "security cameras, with live video and recording downloads for the "
                       "police.")),
            B(ats=T("Mantive sistemas legados de segurança (Bem-Te-Vi e BRAVO) em PHP com "
                    "autenticação LDAP.",
                    "Maintained legacy public safety systems (Bem-Te-Vi and BRAVO) in PHP "
                    "with LDAP authentication."),
              humano=T("Mantive sistemas legados em PHP/Laravel com LDAP, mensageria em "
                       "RabbitMQ e busca em Elasticsearch.",
                       "Maintained legacy PHP/Laravel systems with LDAP, RabbitMQ messaging "
                       "and Elasticsearch search.")),
            B(ats=T("Usei RabbitMQ para processamento assíncrono de SMS de ocorrências de "
                    "placas monitoradas.",
                    "Used RabbitMQ for asynchronous SMS processing of monitored license-plate "
                    "events.")),
            B(ats=T("Integrei Elasticsearch para busca de texto completo.",
                    "Integrated Elasticsearch for full-text search.")),
        ),
        tecnologias=("PHP", "Laravel", "LDAP", "APIs REST", "React", "JavaScript", "Leaflet",
                     "PWA", "PostgreSQL", "Elasticsearch", "RabbitMQ", "Selenium", "Git"),
    ),
    Vaga(
        cargo=T("Desenvolvedor PHP Full Stack Júnior", "Junior Full Stack PHP Developer"),
        empresa=T("Canal Telecom", "Canal Telecom"),
        inicio=(2018, 2), fim=(2018, 11),
        meta_ats=T("São José, SC", "São José, Brazil"),
        local=T("São José, SC", "São José, Brazil"),
        bullets=(
            B(ats=T("Desenvolvi interfaces de relatórios web em PHP/JavaScript.",
                    "Developed web reporting interfaces in PHP/JavaScript.")),
            B(ats=T("Participei de uma migração de banco de dados de SQL para NoSQL (MongoDB).",
                    "Took part in a database migration from SQL to NoSQL (MongoDB).")),
            B(ats=T("Dei manutenção no sistema de backups da empresa, trabalhando com "
                    "comandos Linux/Debian (rsync) para as rotinas de backup.",
                    "Maintained the company's backup system, working with Linux/Debian "
                    "commands (rsync) for backup routines.")),
            B(humano=T("Relatórios web em PHP/JavaScript, migração de SQL para MongoDB e "
                       "rotinas de backup em Linux.",
                       "Web reports in PHP/JavaScript, a SQL-to-MongoDB migration and Linux "
                       "backup routines.")),
        ),
        tecnologias=("PHP", "Zend", "JavaScript", "PostgreSQL", "MySQL", "MongoDB", "Linux",
                     "rsync", "SVN"),
    ),
)

# Nome de tecnologia que muda com o idioma. O que nao esta aqui vale nos dois.
ROTULOS = {
    "Microsserviços": T("Microsserviços", "Microservices"),
    "APIs RESTful": T("APIs RESTful", "RESTful APIs"),
    "APIs REST": T("APIs REST", "REST APIs"),
    "BFF": T("BFF (Backend for Frontend)", "BFF (Backend for Frontend)"),
}


def _e(chave, exibido=None, *outras):
    """Entrada de competencia: (rotulo exibido, chaves de tecnologia que a acionam)."""
    return (exibido or T(chave, chave), (chave,) + outras)


# Secao "Competencias tecnicas" do ATS, derivada das vagas (modelo.competencias).
# Dentro de cada grupo, a especifica vem antes da generica.
CATEGORIAS = (
    (T("Linguagens", "Languages"), (
        _e("Java", T("Java (8 a 21)", "Java (8 to 21)"), "Java 8", "Java 21"),
        _e("TypeScript"), _e("JavaScript"), _e("Python"), _e("PHP"), _e("SQL"),
    )),
    (T("Back-end", "Back-end"), (
        _e("Spring Boot"), _e("Spring MVC"), _e("Spring Data JPA"), _e("Hibernate"),
        _e("jOOQ"), _e("Maven"),
        _e("Microsserviços", T("Microsserviços (Microservices)", "Microservices")),
        _e("APIs RESTful", T("APIs REST (RESTful)", "REST APIs (RESTful)"), "APIs REST"),
        _e("OpenAPI"), _e("Swagger"),
        _e("BFF", T("BFF (Backend for Frontend)", "BFF (Backend for Frontend)")),
        _e("NestJS"), _e("Node.js"), _e("Virtual Threads"), _e("Laravel"), _e("Zend"),
    )),
    (T("Front-end", "Front-end"), (
        _e("Angular 8"), _e("AngularJS"), _e("React"), _e("Redux"), _e("Micro Front-ends"),
        _e("React Native"), _e("Ionic"), _e("PWA"), _e("Leaflet"),
    )),
    (T("Bancos de dados", "Databases"), (
        _e("Oracle Database"), _e("PostgreSQL"), _e("Azure SQL"), _e("MySQL"),
        _e("MongoDB"), _e("Elasticsearch"),
    )),
    (T("Mensageria e dados", "Messaging and data"), (
        _e("RabbitMQ"), _e("Apache Spark"), _e("Apache Airflow"), _e("Machine Learning"),
    )),
    (T("Cloud e DevOps", "Cloud and DevOps"), (
        _e("Docker"), _e("Kubernetes"), _e("ArgoCD"), _e("Azure DevOps"),
        _e("Blob Storage", T("Azure Blob Storage", "Azure Blob Storage")), _e("Azure"),
        _e("AWS (EC2, S3, RDS)"), _e("GCP"), _e("Magalu Cloud"), _e("GitLab CI/CD"),
        _e("Jenkins"), _e("Git flow"), _e("Git"), _e("Linux"), _e("rsync"), _e("SVN"),
    )),
    (T("Testes e qualidade", "Testing and quality"), (
        _e("JUnit"), _e("Mockito"), _e("Jest"), _e("SonarQube"), _e("Selenium"),
    )),
    (T("Segurança e integração", "Security and integration"), (
        _e("JWT"), _e("Keycloak"), _e("OAuth2"), _e("LDAP"),
        _e("Apigee", T("Apigee (API Gateway)", "Apigee (API Gateway)")),
        _e("SAP", T("integração com SAP", "SAP integration")),
    )),
    (T("Metodologias", "Methodologies"), (
        _e("Scrum", T("Metodologias ágeis (Scrum, Kanban)", "Agile (Scrum, Kanban)"),
           "Kanban"),
    )),
    (T("Desenvolvimento assistido por IA", "AI-assisted development"), (
        _e("Spec Driven Development"), _e("Cursor"), _e("Claude Code"),
    )),
    (T("Gestão e observabilidade", "Management and observability"), (
        _e("Jira"), _e("Grafana"),
    )),
)

# Versao humana: 5 linhas curadas a mao (a do ATS e derivada e longa demais).
COMPETENCIAS_HUMANO = (
    (T("Back-end", "Back-end"),
     T("Java 8\u201321, Spring Boot, Spring Data JPA, Hibernate, Maven, APIs REST, "
       "microsserviços, NestJS",
       "Java 8\u201321, Spring Boot, Spring Data JPA, Hibernate, Maven, REST APIs, "
       "microservices, NestJS")),
    (T("Front-end", "Front-end"),
     T("Angular, React, TypeScript, React Native", "Angular, React, TypeScript, React Native")),
    (T("Dados", "Data"),
     T("Oracle, PostgreSQL, Azure SQL, MySQL, MongoDB, RabbitMQ, Elasticsearch",
       "Oracle, PostgreSQL, Azure SQL, MySQL, MongoDB, RabbitMQ, Elasticsearch")),
    (T("Entrega", "Delivery"),
     T("Docker, Kubernetes, CI/CD (Azure DevOps, GitLab, Jenkins), Azure, AWS, GCP",
       "Docker, Kubernetes, CI/CD (Azure DevOps, GitLab, Jenkins), Azure, AWS, GCP")),
    (T("Qualidade", "Quality"),
     T("JUnit, Mockito, Jest, SonarQube, code review, Scrum e Kanban",
       "JUnit, Mockito, Jest, SonarQube, code review, Scrum and Kanban")),
)

# ------------------------------------------------ formacao e o resto ----

FORMACAO = (
    Formacao(
        curso=T("Bacharelado em Ciência da Computação", "Bachelor's Degree in Computer Science"),
        instituicao=T("Universidade Federal de Santa Catarina (UFSC)",
                      "Federal University of Santa Catarina (UFSC)"),
        conclusao=(2026, 12),
    ),
)

FORMACAO_HUMANO = (
    T("<b>Bacharelado em Ciência da Computação</b> \u2014 UFSC \u00b7 conclusão prevista "
      "em dez/2026",
      "<b>Bachelor's Degree in Computer Science</b> \u2014 UFSC (Federal University of "
      "Santa Catarina) \u00b7 expected Dec 2026"),
    T("DEVinHouse, formação full stack React e Java (900h) \u2014 SENAI/SC, 2022",
      "DEVinHouse, full stack React and Java program (900h) \u2014 SENAI/SC, 2022"),
)

# So no ATS. O curso da PUC/RS nao entra na versao humana (ocupa espaco sem
# dizer nada tecnico); o DEVinHouse la vai em FORMACAO_HUMANO.
CERTIFICACOES = (
    T("DEVinHouse - Formação Full Stack React e Java (900h) - SENAI/SC, 2022",
      "DEVinHouse - Full Stack React & Java program (900h) - SENAI/SC, 2022"),
    T("Competências Profissionais, Emocionais e Tecnológicas para Tempos de Mudança - "
      "PUC/RS, 2023",
      "Professional, Emotional, and Technological Skills for Times of Change - PUC/RS, 2023"),
)

IDIOMAS_ATS = (
    (T("Português", "Portuguese"), T("nativo", "native")),
    (T("Inglês", "English"),
     T("proficiência profissional - leitura e escrita fluentes, conversação proficiente; "
       "uso diário em documentação e code review",
       "professional working proficiency - fluent reading and writing, proficient spoken "
       "conversation; used daily for documentation and code review")),
    (T("Espanhol", "Spanish"), T("básico", "basic")),
)

IDIOMAS_HUMANO = T(
    "Português nativo \u00b7 Inglês profissional (leitura e escrita fluentes, conversação "
    "proficiente) \u00b7 Espanhol básico",
    "Portuguese (native) \u00b7 English (professional: fluent reading and writing, "
    "proficient conversation) \u00b7 Spanish (basic)",
)

# Longe do bloco de contato de proposito: valores em reais perto do telefone
# sao capturados por regex gulosa de telefone/documento.
PRETENSAO = (
    T("Pretensão salarial", "Rate expectation"),
    T("R$ 8.500 a R$ 10.500 por mês (CLT) ou R$ 13.000 a R$ 15.000 por mês (PJ)",
      "US$ 25-35/h (contractor, PJ/CNPJ)"),
)

DISPONIBILIDADE = (
    T("Disponibilidade", "Availability"),
    T("imediata, para trabalho 100% remoto", "immediate, for 100% remote work"),
)

# Metadados do DOCX (limite de 255 caracteres em OPC).
PALAVRAS_CHAVE = T(
    "Java, Spring Boot, Spring Data JPA, Maven, Microsservicos, APIs REST, Angular, React, "
    "TypeScript, Node.js, Oracle, PostgreSQL, SQL, Docker, Kubernetes, CI/CD, Azure, AWS, "
    "GCP, JUnit, Mockito, RabbitMQ, Scrum, Full Stack, Remoto",
    "Java, Spring Boot, Spring Data JPA, Maven, Microservices, REST APIs, Angular, React, "
    "TypeScript, Node.js, Oracle, PostgreSQL, SQL, Docker, Kubernetes, CI/CD, Azure, AWS, "
    "GCP, JUnit, Mockito, RabbitMQ, Scrum, Full Stack, Remote",
)
