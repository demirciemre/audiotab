#!/bin/zsh
# README görsellerini üretir: scenes.py sahneleri HTML'e yazar, Chrome (headless) 2x çizer, cwebp ile WebP yapar.
# Kullanım: tools/readme-art/render.sh [sahne-adı ...]   (boşsa hepsi; her sahne tr ve en olarak)
# Gerekenler: python3, Google Chrome, cwebp (brew install webp). Çıktı: docs/images/{tr,en}/<sahne>.webp
set -euo pipefail
here=${0:A:h}
repo=${here:h:h}
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[[ -x "$chrome" ]] || { echo "Google Chrome bulunamadı"; exit 1; }
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
mkdir -p "$repo/docs/images"

for lang in tr en; do
  mkdir -p "$repo/docs/images/$lang" "$work/$lang"
  python3 "$here/scenes.py" "$work/$lang/html" "$lang" > "$work/$lang/list"
  while read -r name w h; do
    (( $# == 0 )) || [[ " $* " == *" $name "* ]] || continue
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
      --default-background-color=00000000 --user-data-dir="$work/profile" \
      --window-size="$w,$h" --screenshot="$work/$lang/$name.png" "file://$work/$lang/html/$name.html" >/dev/null 2>&1
    cwebp -quiet -q 88 -alpha_q 100 "$work/$lang/$name.png" -o "$repo/docs/images/$lang/$name.webp"
    echo "docs/images/$lang/$name.webp"
  done < "$work/$lang/list"
done
