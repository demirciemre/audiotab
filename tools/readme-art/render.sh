#!/bin/zsh
# README görsellerini üretir: scenes.py sahneleri HTML'e yazar, Chrome (headless) 2x çizer, cwebp ile WebP yapar.
# Kullanım: tools/readme-art/render.sh [sahne-adı ...]   (boşsa hepsi)
# Gerekenler: python3, Google Chrome, cwebp (brew install webp). Çıktı: docs/images/<sahne>.webp
set -euo pipefail
here=${0:A:h}
repo=${here:h:h}
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[[ -x "$chrome" ]] || { echo "Google Chrome bulunamadı"; exit 1; }
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
mkdir -p "$repo/docs/images"

python3 "$here/scenes.py" "$work/html" > "$work/list"
while read -r name w h; do
  (( $# == 0 )) || [[ " $* " == *" $name "* ]] || continue
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --default-background-color=00000000 --user-data-dir="$work/profile" \
    --window-size="$w,$h" --screenshot="$work/$name.png" "file://$work/html/$name.html" >/dev/null 2>&1
  cwebp -quiet -q 88 -alpha_q 100 "$work/$name.png" -o "$repo/docs/images/$name.webp"
  echo "docs/images/$name.webp"
done < "$work/list"
