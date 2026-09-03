# Site RAWS Estúdio

Landing page estática (HTML/CSS/JS puro, sem build) pronta pra publicar na Vercel.

## Estrutura
```
index.html          → o site inteiro (conteúdo + estilo + scripts + dados estruturados)
robots.txt          → libera a indexação e aponta o sitemap
sitemap.xml         → mapa do site pro Google/Bing
llms.txt            → resumo do negócio pras IAs (ChatGPT, Claude, Perplexity)
assets/*.webp        → imagens que a página carrega (versões leves)
assets/*.png         → originais, mantidos só como fonte
assets/og-cover.jpg  → imagem da prévia no WhatsApp/Facebook (1200x630)
assets/favicon.png   → ícone da aba
tools/otimizar-imagens.py → regera os .webp a partir dos originais
```

## O que editar (rápido)
Abra o `index.html` e procure por `[ EDITAR ]`:

1. **WhatsApp e Instagram** — no `<script>` no final do arquivo:
   ```js
   const WHATSAPP = "5547999990000";   // seu número: 55 + DDD + número, só dígitos
   const INSTAGRAM = "raws.podcast";   // seu @ sem o "@"
   ```
   Todos os botões de WhatsApp do site usam esse número automaticamente.

2. **Preços e cortes** — procure `[ EDITAR PREÇOS/CORTES AQUI ]` na seção de planos.

3. **Textos** — é HTML normal, edite direto entre as tags.

## Como publicar na Vercel (mesmo fluxo do Chalana's Bet)
1. Crie um repositório novo no GitHub e faça upload destes arquivos (mantendo a pasta `assets`).
2. Na Vercel, clique em **Add New → Project** e importe esse repositório.
3. Framework Preset: **Other** (é site estático, sem build). Deixe os campos de build vazios.
4. **Deploy**. Pronto — a Vercel serve o `index.html` na raiz.

## Domínio (raws.com.br)
O site está no ar em **raws.com.br** e **www.raws.com.br**, com o DNS apontado pra Vercel (registro `A` `@` → `216.198.79.1`, `CNAME` `www` → `cname.vercel-dns.com`). O domínio segue registrado na Hostinger, que também continua hospedando o e-mail — os registros `MX` não foram tocados.

> Pendência de SEO: hoje o apex e o `www` respondem **200 os dois**, o que é conteúdo duplicado pro Google. Na Vercel → **Settings → Domains**, marque `www.raws.com.br` como *Redirect* pra `raws.com.br`. A tag `canonical` já cobre isso, mas o redirect resolve de vez.

## Marca d'água de build
O rodapé mostra `build v1`. Ao subir uma versão nova, troque pra `build v2`, `v3`… pra confirmar visualmente que o deploy pegou.

## SEO — o que já está no ar

O domínio oficial é **https://raws.com.br** (o site também responde em `www.raws.com.br`).

- `robots.txt` e `sitemap.xml` na raiz — envie o sitemap no [Google Search Console](https://search.google.com/search-console) e no [Bing Webmaster Tools](https://www.bing.com/webmasters).
- `llms.txt` na raiz — resumo em texto do negócio, preços e contato, pras IAs citarem o RAWS corretamente.
- No `index.html`: tag `canonical`, Open Graph completo (prévia bonita no WhatsApp) e um bloco **JSON-LD** com `LocalBusiness` + catálogo de ofertas.

> **Ao mudar preço na página, mude também no JSON-LD** (procure `[ EDITAR ]` no `<head>`) e atualize o `llms.txt`. Preço divergente entre página e dados estruturados é penalizado pelo Google.

## Imagens (importante pro Google)

A página carrega **WebP** redimensionado pro tamanho real de exibição. Isso derrubou o peso de **5,6 MB pra 137 KB** — velocidade é fator de ranqueamento (Core Web Vitals), e a foto do topo é o que o Google cronometra como LCP.

**Ao adicionar ou trocar uma foto:**

1. Jogue o original (PNG ou JPG) em `assets/` com um nome que já esteja em `tools/otimizar-imagens.py` — ou adicione o nome novo no dicionário `ALVOS`, com a largura = 2× o tamanho que ele aparece na tela.
2. Rode `python tools/otimizar-imagens.py` (precisa de `pip install pillow`).
3. Aponte o `<img>` do `index.html` pro `.webp` gerado, com `width`, `height` e `loading="lazy"` (menos na foto do topo, que usa `fetchpriority="high"`).

Os `.png` originais ficam no repositório de propósito, como fonte pra reprocessar. Eles não pesam na página — ninguém os baixa.

> A prévia de link (`og-cover.jpg`) é gerada à parte, em **JPEG 1200×630** e sem os cantos arredondados. Não troque por WebP: nem todo scraper de link lê WebP.
