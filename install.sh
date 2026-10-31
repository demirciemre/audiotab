#!/bin/bash
# AudioTab'ı GitHub'daki son sürümden kur (derlemeye gerek yok):
#   curl -fsSL https://raw.githubusercontent.com/demirciemre/audiotab/main/install.sh -o install.sh
#   less install.sh      # ne yaptığına bak
#   bash install.sh
#
# Paket Developer ID ile imzalı ve Apple tarafından notarize edilmiş olmalı; değilse hiçbir şey
# değiştirilmez. Karantina bayrağı silinmez, Gatekeeper atlatılmaz: macOS paketi kendisi denetler.
set -euo pipefail
REPO="demirciemre/audiotab"
BUNDLE_ID="com.uniwebsolution.audiotab"
TEAM_ID="ZUJ2KQLB2U"   # Developer ID ekip kimliği (10 karakter); CI'daki TEAM_ID ile aynı

if ! [[ "$TEAM_ID" =~ ^[A-Z0-9]{10}$ ]]; then
  echo "✖ install.sh içinde TEAM_ID ayarlanmamış." >&2
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "▶ Son sürüm indiriliyor..."
curl --proto '=https' --tlsv1.2 -fsSL "https://github.com/$REPO/releases/latest/download/AudioTab.zip" -o "$TMP/AudioTab.zip"
ditto -x -k "$TMP/AudioTab.zip" "$TMP/x"
APP="$TMP/x/AudioTab.app"
[[ -d "$APP" && ! -L "$APP" ]] || { echo "✖ Paket içinde AudioTab.app yok." >&2; exit 1; }

REQ="anchor apple generic and identifier \"$BUNDLE_ID\" and certificate 1[field.1.2.840.113635.100.6.2.6] and certificate leaf[field.1.2.840.113635.100.6.1.13] and certificate leaf[subject.OU] = \"$TEAM_ID\" and notarized"
if ! codesign --verify --deep --strict -R="$REQ" "$APP" 2>/dev/null; then
  echo "✖ İndirilen paket bu projenin Developer ID'siyle imzalı ve notarize edilmiş değil, kurulmadı." >&2
  exit 1
fi
if ! spctl --assess --type execute "$APP" 2>/dev/null; then
  echo "✖ Gatekeeper paketi onaylamadı, kurulmadı." >&2
  exit 1
fi

pkill -x AudioTab 2>/dev/null || true
sleep 0.5
rm -rf /Applications/AudioTab.app
ditto "$APP" /Applications/AudioTab.app
if ! codesign --verify --deep --strict -R="$REQ" /Applications/AudioTab.app 2>/dev/null; then
  rm -rf /Applications/AudioTab.app
  echo "✖ Kopyalanan uygulama doğrulanamadı, kaldırıldı." >&2
  exit 1
fi
open /Applications/AudioTab.app

echo "✅ AudioTab kuruldu. Bundan sonraki sürümler uygulamanın içinden güncellenir."
