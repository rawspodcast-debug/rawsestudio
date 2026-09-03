#!/usr/bin/env python3
"""
Otimiza as imagens do site: PNG/JPG -> WebP, no tamanho em que a página
realmente exibe. Rode sempre que adicionar ou trocar uma foto em assets/.

    pip install pillow
    python tools/otimizar-imagens.py

Depois é só apontar o <img> do index.html pro arquivo .webp gerado.
Os originais NÃO são apagados — eles ficam como fonte pra reprocessar.
"""
import os
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# nome do arquivo (sem extensão) -> largura máxima em px.
# Regra: 2x o tamanho em que a imagem aparece na tela (pra telas retina).
ALVOS = {
    'estudio2':   1200,   # foto do topo: exibe ~490px
    'canecas':     500,   # painel das canecas
    'pod1':        448,   # slots de canal: 224x108 na tela
    'pod2':        448,
    'pod3':        448,
    'pod5':        448,
    'pod6':        448,
    'pod7':        448,
    'raws-logo':   682,   # logo (tem transparência)
}
QUALIDADE = 82
QUALIDADE_LOGO = 90


def main():
    assets = os.path.join(RAIZ, 'assets')
    antes = depois = 0
    for nome, largura in ALVOS.items():
        src = next((os.path.join(assets, nome + e)
                    for e in ('.png', '.jpg', '.jpeg')
                    if os.path.exists(os.path.join(assets, nome + e))), None)
        if not src:
            print(f'  {nome:14} — sem original, pulando')
            continue

        im = Image.open(src)
        if im.width > largura:
            im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)

        dst = os.path.join(assets, nome + '.webp')
        q = QUALIDADE_LOGO if 'logo' in nome else QUALIDADE
        im.save(dst, 'WEBP', quality=q, method=6)

        a, d = os.path.getsize(src), os.path.getsize(dst)
        antes += a
        depois += d
        print(f'  {nome:14} {a/1024:7.0f}K -> {d/1024:6.0f}K  ({100-100*d/a:3.0f}% menor)  {im.size}')

    if antes:
        print(f'\n  TOTAL {antes/1024/1024:.2f} MB -> {depois/1024/1024:.2f} MB '
              f'({100-100*depois/antes:.0f}% menor)')
    print('\n  Lembre: a imagem de compartilhamento (assets/og-cover.jpg) é gerada à parte,')
    print('  em 1200x630 e em JPEG — é o formato que WhatsApp e Facebook leem sem falhar.')


if __name__ == '__main__':
    main()
