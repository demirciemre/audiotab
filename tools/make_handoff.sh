#!/bin/zsh
# Devir paketini üretir: docs/handoff/<ad>/HANDOFF.md + README'ler + görseller + simge kaynakları.
# Kullanım: tools/make_handoff.sh [ad]      (varsayılan: upstream-2.4.2)
# Çıktı: dist/AudioTab-handoff-<ad>-v<VERSION>.zip  (dist/ git'e girmez)
# Paket sırrı içermez; içinde Team ID ya da anahtar adı bulunursa betik durur.
set -euo pipefail
here=${0:A:h}
repo=${here:h}
name=${1:-upstream-2.4.2}
version=$(<"$repo/VERSION")
src="$repo/docs/handoff/$name"
[[ -f "$src/HANDOFF.md" ]] || { echo "docs/handoff/$name/HANDOFF.md yok"; exit 1; }

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
pkg="$work/AudioTab-handoff-$name"
mkdir -p "$pkg"

cp "$src/HANDOFF.md" "$pkg/"
cd "$repo"
for p in README.md README.tr.md docs/images docs/brand Icon/AppIcon.icon Resources/Assets.car Resources/AppIcon.icns \
         tools/make_icon.sh tools/icon_review.sh tools/icon_sheet.swift tools/readme-art; do
  mkdir -p "$pkg/${p:h}"
  cp -R "$p" "$pkg/$p"
done

# Sır denetimi: Team ID, anahtar ve sertifika izleri pakete girmesin
team=$(sed -n 's/^TEAM_ID="\([A-Z0-9]\{10\}\)".*/\1/p' install.sh)
if grep -rIl -e "BEGIN .*PRIVATE KEY" -e "AuthKey_[A-Z0-9]\{10\}" ${team:+-e "$team"} "$pkg" >/dev/null 2>&1; then
  echo "✖ Pakette gizli kalması gereken bir değer bulundu:"; grep -rIl -e "BEGIN .*PRIVATE KEY" -e "AuthKey_[A-Z0-9]\{10\}" ${team:+-e "$team"} "$pkg"
  exit 1
fi
find "$pkg" \( -name '*.p12' -o -name '*.p8' -o -name '*.pem' -o -name '.env*' \) | grep -q . && { echo "✖ Pakette anahtar dosyası var"; exit 1; }

mkdir -p "$repo/dist"
out="$repo/dist/AudioTab-handoff-$name-v$version.zip"
rm -f "$out"
(cd "$work" && ditto -c -k --keepParent --norsrc "AudioTab-handoff-$name" "$out")
echo "$out ($(du -h "$out" | cut -f1))"
