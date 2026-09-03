# Site RAWS Estúdio

Landing page estática (HTML/CSS/JS puro, sem build) no ar em **https://raws.com.br**, hospedada na Vercel com deploy automático a cada push na `main`.

## Estrutura

```
index.html                → o site inteiro (conteúdo + estilo + scripts + dados estruturados)
vercel.json               → redirect www → apex
robots.txt                → libera indexação e aponta o sitemap
sitemap.xml               → mapa do site pro Google/Bing
llms.txt                  → resumo do negócio pras IAs (ChatGPT, Claude, Perplexity)
tools/otimizar-imagens.py → regera os .webp a partir dos originais
assets/*.webp             → imagens que a página carrega (versões leves)
assets/*.png              → originais, mantidos só como fonte
assets/og-cover.jpg       → prévia de link no WhatsApp/Facebook (1200×630)
assets/favicon.png        → ícone da aba
```

---

## Antes de commitar: `git fetch`

O `index.html` também é editado **direto pela interface web do GitHub**. O clone local fica atrasado sem avisar — o `git status` mostra `main...origin/main` sem divergência se você não fez fetch, e aí o push é rejeitado.

```bash
git fetch origin
git log --oneline HEAD..origin/main   # vazio = em dia
```

Ao resolver conflito, **preserve a edição feita no GitHub** — ela é intencional, não resíduo.

## Marca d'água de build

O rodapé mostra `build v8`. Ao subir uma versão nova, incremente (`v9`, `v10`…) — é assim que se confirma que o deploy pegou, e não uma versão em cache.

---

## O que editar (rápido)

Abra o `index.html` e procure por `[ EDITAR ]`:

1. **WhatsApp e Instagram** — no `<script>` no final do arquivo:
   ```js
   const WHATSAPP = "5547997198877";   // 55 + DDD + número, só dígitos
   const INSTAGRAM = "estudioraws";    // @ sem o "@"
   ```
   Todos os botões de WhatsApp do site usam esse número automaticamente.

2. **Preços e cortes** — procure `[ EDITAR PREÇOS/CORTES AQUI ]` na seção de planos.

3. **Textos** — é HTML normal, edite direto entre as tags.

> **Ao mudar preço, mude em três lugares:** o texto da página, o bloco JSON-LD no `<head>` e o `llms.txt`. Preço divergente entre a página e os dados estruturados é violação das diretrizes do Google.

---

## SEO

### Arquivos na raiz

| arquivo | o que faz |
|---|---|
| `robots.txt` | libera tudo, inclusive os robôs de IA (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot). Aponta o sitemap. |
| `sitemap.xml` | uma URL só — o site é página única. Âncoras (`#planos`, `#como`) **não** entram: o Google as ignora em sitemaps. Inclui as imagens principais com título e legenda. |
| `llms.txt` | resumo em Markdown do negócio, planos, preços, endereço e contato. É o que decide o que o ChatGPT/Claude respondem sobre o RAWS. |

### No `<head>` do `index.html`

- `canonical` apontando pro apex
- `robots` com `max-image-preview:large`
- Open Graph e Twitter Card completos, com `og-cover.jpg` própria
- **JSON-LD** com `LocalBusiness` + `WebSite` + `WebPage`, incluindo endereço, telefone, `geo`, `priceRange` e um `hasOfferCatalog` com os 3 planos e os 3 serviços avulsos

### Alinhamento com o Google Meu Negócio

A ficha **já existe e ranqueia bem**. Site e ficha precisam concordar — o JSON-LD foi alinhado a ela:

- `name` é **"Raws Estúdio de Podcast"** (o nome da ficha), não "RAWS Estúdio". A forma curta está em `alternateName`.
- `geo` usa as coordenadas do pino da ficha (`-26.2908485, -48.8678485`), que são a fonte autoritativa.
- `sameAs` e `hasMap` apontam pra ficha; a página tem um link visível "Como chegar".

> **Nunca adicione `aggregateRating` ou `review` no JSON-LD.** Avaliação auto-declarada em `LocalBusiness` é contra as diretrizes do Google, não gera resultado rico e pode render ação manual. A nota real o Google já mostra a partir dos dados dele.

Ausente de propósito: `openingHoursSpecification` — o atendimento é sob agendamento, e o schema.org não expressa isso sem declarar horário fixo falso.

### Como validar

- [Rich Results Test](https://search.google.com/test/rich-results?url=https%3A%2F%2Fraws.com.br%2F)
- [Validador do schema.org](https://validator.schema.org/#url=https%3A%2F%2Fraws.com.br%2F) (mais rigoroso)

### Pendente

- [ ] Enviar o sitemap no [Search Console](https://search.google.com/search-console) — cadastre como propriedade de **Domínio** (verificação por DNS na Hostinger), não "Prefixo de URL": a de domínio cobre apex e www de uma vez.

---

## Imagens

A página carrega **WebP** redimensionado pro tamanho real de exibição. Isso derrubou as imagens de **5,5 MB para 136 KB** (home inteira: ~176 KB). Velocidade é fator de ranqueamento, e a foto do topo é o que o Google cronometra como LCP.

**Ao adicionar ou trocar uma foto:**

1. Jogue o original (PNG ou JPG) em `assets/` com um nome que já esteja em `tools/otimizar-imagens.py` — ou adicione o nome no dicionário `ALVOS`, com largura = 2× o tamanho que ele aparece na tela.
2. Rode `python tools/otimizar-imagens.py` (precisa de `pip install pillow`).
3. Aponte o `<img>` pro `.webp` gerado, com `width`, `height` e `loading="lazy"` — menos na foto do topo, que usa `fetchpriority="high"` por ser o LCP.

Os `.png` originais ficam no repositório de propósito, como fonte pra reprocessar. Não pesam na página — ninguém os baixa.

### Armadilha: `width`/`height` esticam a imagem

Os atributos `width`/`height` no `<img>` (que existem pra evitar layout shift) viram *presentational hints* e são usados como **altura real**. Se o CSS define só `width`, a imagem estica.

Por isso a regra global é:

```css
img{max-width:100%;display:block;height:auto;}
```

O `height:auto` neutraliza o atributo em qualquer `<img>` sem altura própria no CSS. As regras com classe (`.nav .logo img`, `.mug-art img`, `.logos .slot`, `.foot-grid img`) têm especificidade maior e seguem valendo.

Esse bug já apareceu duas vezes: no logo do rodapé e na foto do topo. **Ao mexer em imagem, meça a proporção renderizada contra a do arquivo** em vez de só olhar a tela.

> A prévia de link (`og-cover.jpg`) é gerada à parte, em **JPEG 1200×630** e sem os cantos arredondados. Não troque por WebP: nem todo scraper de link lê WebP.

---

## Domínio e hospedagem

O site está no ar em **raws.com.br**, com o DNS apontado pra Vercel (`A` `@` → `216.198.79.1`, `CNAME` `www` → `cname.vercel-dns.com`). O domínio segue registrado na Hostinger, que também hospeda o e-mail — os registros `MX` não foram tocados.

### Redirect do www (`vercel.json`)

`www.raws.com.br` responde **308** para `raws.com.br`, preservando o caminho. Antes os dois hostnames devolviam 200, o que é conteúdo duplicado.

Fica no `vercel.json` (versionado, revisável no diff) em vez do painel da Vercel. Duas armadilhas encontradas na prática:

- O `source` é `/(.*)` e **não** `/:path*`. Com `/:path*` os subcaminhos redirecionam mas a raiz `www.raws.com.br/` continua respondendo 200 — o padrão não casa com o caminho vazio.
- `vercel.json` é JSON puro: não aceita comentários nem chaves fora do schema. Um `"comment"` dentro do redirect faz o deploy falhar na validação.

Ao trocar de domínio, atualize o `value` do `has.host` e o `destination`.

### Como testar depois de um deploy

```bash
# o deploy pegou?
curl -s https://raws.com.br/ | grep -o 'build v[0-9]*'

# o redirect cobre raiz E subcaminhos?
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" https://www.raws.com.br/
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" https://www.raws.com.br/llms.txt
```

Um 200 na raiz do `www` significa que o redirect quebrou.

> **Nota sobre o `sitemap.xml`:** abrir no navegador mostra *"This XML file does not appear to have any style information"*. Isso é normal em qualquer XML sem folha de estilo — não é erro. O rastreador baixa e faz parse direto.
