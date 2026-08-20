# Personal Branding

Posts e materiais de marca pessoal ligados à busca de recolocação.
Complementa `interview_prep/` (preparação reativa) com o lado ativo: conteúdo
que atrai recrutador antes de existir vaga.

---

## Índice

| Arquivo | Tema | Status |
|---|---|---|
| `linkedin_post_wame_link.txt` | Dica técnica: wa.me + CTA de recolocação e freela | Pronto — falta gerar o link curto do Business |
| `whatsapp_business_profile.txt` | **Fonte única** da config do WhatsApp Business: perfil, automáticas, respostas rápidas | Pronto para colar |
| `copiar.ps1` | Utilitário: copia um bloco do post pro clipboard | — |

> Este repositório é público. Material de negociação e preparação de processo
> seletivo não é versionado aqui — ver `.gitignore`.

O `whatsapp_business_profile.txt` é o **destino de todo texto que vai para um
campo de configuração** do WhatsApp — os arquivos de post apenas apontam para
ele. Duplicar esses textos já causou divergência uma vez: a saudação continuou
roteando só recrutador depois que o post passou a anunciar freela.

---

## Como copiar o texto sem quebrar

**Nunca copie prosa da tela do Claude Code.** Ele mede a largura do terminal e
insere quebras de linha *reais* antes de imprimir, então o texto no buffer já
vem picotado no meio das frases — nenhuma configuração do terminal desfaz
isso. Some-se o padding à esquerda, que vem junto na seleção.

Use o script, que vai do arquivo direto pro clipboard:

```powershell
.\copiar.ps1        # bloco [2] — corpo do post
.\copiar.ps1 4      # bloco [4] — primeiro comentário
.\copiar.ps1 3 -Ver # mostra o bloco [3] em vez de copiar
```

Ele ainda avisa se o corpo estourou os 3.000 caracteres do LinkedIn, se
sobrou algum `https://` no texto ou se ficou placeholder `XXXX` pra trocar.

---

## Convenção de nomes

```
linkedin_post_<slug_em_snake_case>.txt
```

- Um arquivo por post. Nunca acumular vários posts no mesmo arquivo.
- `.txt`, não `.md` — o corpo do post é copiado e colado direto no LinkedIn, e
  markdown ali vira lixo visual (`**`, `#`, `-` aparecem literalmente).
- Slug descreve o **assunto**, não a data: `wame_link`, não `post_agosto`.

---

## Estrutura padrão de um post

Todo arquivo segue os mesmos 5 blocos, na mesma ordem:

| Bloco | Nome | Para quê |
|---|---|---|
| `[1]` | ANTES DE PUBLICAR — CHECKLIST | Pré-requisitos acionáveis. Se tem checkbox aberto, não publica. |
| `[2]` | CORPO DO POST | Texto final, pronto pra copiar. Nada de comentário meu aqui dentro. |
| `[3]` | MENSAGENS AUTOMÁTICAS | Textos de WhatsApp Business etc. que o post aciona. Omitir se o post não tiver. |
| `[4]` | PRIMEIRO COMENTÁRIO | Onde vai o link clicável. Postar logo após publicar e fixar. |
| `[5]` | VERSÃO EM INGLÊS | Opcional. |
| `[6]` | NOTAS DE ESTRATÉGIA | Por que cada decisão foi tomada. **Não publicar.** |

O bloco de notas é o que faz o arquivo valer a pena meses depois: sem ele,
daqui a seis meses eu não lembro por que o link foi pro comentário em vez do
corpo.

**Formato dos blocos copiáveis:** nos blocos que vão pro LinkedIn, cada
parágrafo ocupa **uma linha só**, por mais longa que fique. O LinkedIn preserva
as quebras coladas, então texto quebrado em 78 colunas sai picotado no meio das
frases. Só quebre onde a quebra é intencional.

---

## Playbook — regras que valem pra qualquer post

Aprendizados já aplicados no post do wa.me. Reaproveitar, não redescobrir.

**Hook = rótulo + valor imediato + tensão.** Orçamento: ~140 caracteres no
mobile antes do "ver mais". Se o que cabe aí não faz clicar, o post não existe.

```
DICA RÁPIDA: <benefício em uma linha>.

<o valor entregue de cara>

Essa é a dica inteira. Mas tem 3 usos que quase ninguém conhece.
```

Rótulo em CAPS ("DICA RÁPIDA", "PSA", "TIL") sinaliza em meio segundo que o
post é curto e útil. Entregar a dica básica já na linha 1 compra confiança com
público técnico, que rejeita pergunta retórica de abertura — soa a *broetry*.
Isso não queima o post: o valor real fica nos usos avançados, atrás do "ver
mais". A terceira linha fecha o loop pequeno e abre o grande.

Nunca `https://` no hook — o LinkedIn auto-linka e cria uma porta de saída
clicável na primeira linha. Exemplo concreto (`wa.me/5511999999999`) em vez de
placeholder (`wa.me/<ddi><telefone>`): placeholder é sintaxe de documentação e
exige decodificar. A notação com `<...>` fica no corpo, onde se está ensinando.

**Link clicável vai no primeiro comentário.**
Link no corpo derruba a entrega. No corpo, escrever URL como texto puro (sem
`https://`) — funciona como tutorial e não tira ninguém da plataforma.

**Separar o didático do CTA.**
Exemplos com dados fictícios na parte que ensina; o link real só no final e
assumido ("e sim, vou usar o post pra praticar o que ensinei"). Post de dica
com autopromoção no meio da explicação perde credibilidade de tutorial.

**O CTA precisa ser um teste, não um favor.**
Se clicar no link *é* a demonstração da técnica ensinada, o CTA para de soar
mendigado.

**Bilíngue: PT completo → separador → EN completo.**
Nunca alternar idioma frase a frase — atrapalha a leitura dos dois públicos.

**Incluir pelo menos um aviso honesto.**
Limitação real da técnica (atrito, risco, caso em que não funciona). É o que
separa conteúdo de anúncio, e é o que puxa comentário de quem tem experiência.

**Fechar com pergunta específica.**
"Você já usava X ou só Y?" gera resposta. "O que você acha?" não gera nada.

**No máximo 2 CTAs no corpo; a triagem vive fora do post.**
Três chamadas diluem tudo. Duas portas em uma frase cada, e o menu "me diz qual
é o seu caso" na mensagem automática — onde não custa espaço nem atenção.

**Vender serviço: oferta específica, nunca disponibilidade genérica.**
"Aceito freelas" não gera lead — ninguém consegue mapear o próprio problema
nisso. Listar problemas que o cliente já sabe que tem ("aquele bug que ninguém
resolve", "essa planilha me toma 3h por dia") gera.

**Nunca escrever fraqueza de negociação no post.**
"Preciso muito de renda", "aceito qualquer valor", "nunca fiz isso antes"
destroem poder de precificação e plantam dúvida sobre a entrega. O honesto sem
o custo: "comecei a pegar projeto pontual" + diagnóstico grátis na primeira
conversa. Desconto de entrada ancora o preço lá embaixo e é difícil subir
depois; diagnóstico gratuito traz o mesmo contato sem mexer na tabela.

**Verificar formato documentado antes de ensinar.**
Se a doc oficial diz uma coisa e "na prática funciona" diz outra, ensinar a
doc. O contrário aparece nos comentários.

**Nunca usar dado real de terceiro como exemplo.**
Número, e-mail ou endereço de empresa em exemplo didático manda tráfego pra
canal errado e não gera atenção nenhuma da marca. Piggyback em marca só
funciona analisando algo que a empresa fez — e aí marcando a empresa.

**Publicação:** terça a quinta, 8h–10h ou 12h–13h (Brasília). Responder TODOS
os comentários na primeira hora — é o que mais impulsiona a entrega.

---

## Template para um post novo

```
================================================================================
POST LINKEDIN - <TEMA>
Autor: Lucas Bueno Cesario
Objetivo: <engajamento? autoridade técnica? captação de recrutador?>
Status: <rascunho | pronto para publicar | publicado em AAAA-MM-DD>
================================================================================


--------------------------------------------------------------------------------
[1] ANTES DE PUBLICAR - CHECKLIST
--------------------------------------------------------------------------------

[ ] ...


--------------------------------------------------------------------------------
[2] CORPO DO POST (copiar daqui até a linha de fechamento)
--------------------------------------------------------------------------------

<hook em 2 linhas>

<conteúdo>

<aviso honesto>

<CTA>

<pergunta de fechamento>

#Hashtag1 #Hashtag2 #Hashtag3

--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
[3] MENSAGENS AUTOMÁTICAS (omitir se não houver)
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
[4] PRIMEIRO COMENTÁRIO (postar logo após publicar e FIXAR)
--------------------------------------------------------------------------------

<link clicável + 1 linha de contexto>

--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
[5] VERSÃO EM INGLÊS (opcional)
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
[6] NOTAS DE ESTRATÉGIA (não publicar)
--------------------------------------------------------------------------------

<por que cada decisão>

================================================================================
```

O `copiar.ps1` acha os blocos pelo padrão `[N] TÍTULO` entre linhas de traços —
mantenha esse formato e ele funciona em qualquer post novo:
`.\copiar.ps1 2 -Arquivo linkedin_post_outro.txt`

---

## Depois de publicar

1. Atualizar `Status` no cabeçalho do arquivo para `publicado em AAAA-MM-DD`.
2. Atualizar a coluna Status no índice deste README.
3. Anotar no bloco `[5]` o que funcionou e o que não funcionou — alcance,
   comentários, se veio contato de recrutador. É isso que alimenta o playbook
   acima no post seguinte.
