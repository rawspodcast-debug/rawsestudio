# Site RAWS Estúdio

Landing page estática (HTML/CSS/JS puro, sem build) pronta pra publicar na Vercel.

## Estrutura
```
index.html          → o site inteiro (conteúdo + estilo + scripts)
assets/raws-logo.png → logo RAWS
assets/favicon.png   → ícone da aba
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

## Domínio (www.rawsestudio.com.br)
No painel do projeto na Vercel → **Settings → Domains** → adicione `rawsestudio.com.br` e `www.rawsestudio.com.br`. A Vercel mostra os registros DNS (um `A` e/ou `CNAME`) pra você apontar no seu provedor de domínio. O domínio continua registrado onde está — só o DNS aponta pra Vercel.

> Atenção: se o e-mail @rawsestudio vem junto da hospedagem antiga, não cancele a hospedagem sem antes garantir o e-mail em outro lugar (os registros `MX` não mudam ao apontar o site pra Vercel, mas confirme).

## Marca d'água de build
O rodapé mostra `build v1`. Ao subir uma versão nova, troque pra `build v2`, `v3`… pra confirmar visualmente que o deploy pegou.
