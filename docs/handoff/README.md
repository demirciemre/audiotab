# Devir paketleri

Başka birinin (ya da onun Claude oturumunun) bu repodaki değişiklikleri kendi projesine alabilmesi için hazırlanan dokümanlar.

- Her paket kendi klasöründe durur: `docs/handoff/<ad>/HANDOFF.md`. `<ad>` paketin kime ve hangi noktadan itibaren yazıldığını söyler, örneğin `upstream-2.4.2`.
- Bu klasörde yalnızca kaynak (Markdown) tutulur. Zip dosyası `tools/make_handoff.sh <ad>` ile `dist/` klasörüne üretilir. `dist/` git'e girmez; paylaşmak için oradan alınır ya da bir GitHub Release'e eklenir.
- Paketler herkese açıktır. Sertifika, anahtar, parola, Team ID ya da kişisel bilgi içermez. `make_handoff.sh` bunları arar ve bulursa durur.

| Paket | Kimin için |
|---|---|
| [upstream-2.4.2](upstream-2.4.2/HANDOFF.md) | debelemez/AudioTab 2.4.2 üzerine yapılan her şey: Apple Developer hesabıyla ve hesapsız iki yol |
