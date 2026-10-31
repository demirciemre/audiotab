# AudioTab

Mac menü çubuğunda küçük bir uygulama: cam görünümlü ⌘Tab · tek tuşla ses çıkışı değiştirme · ekran bölme · ekran görüntüsü ve MP4 kayıt · harici ekran parlaklığı.

[debelemez/AudioTab](https://github.com/debelemez/AudioTab) (MIT) temel alınarak yapıldı. Özellikler aynıdır; değişen **güven zinciridir**:

| | Özgün | Bu sürüm |
|---|---|---|
| İmza | Kendinden imzalı sertifika | Apple **Developer ID**, hardened runtime, güvenli zaman damgası |
| Gatekeeper | "Apple could not verify…" uyarısı; karantina `xattr` ile siliniyor | **Notarize** edilmiş ve bilet zımbalanmış: uyarısız açılır |
| Güncelleme doğrulaması | Sabit SHA-1 parmak izi | Apple köküne bağlı Developer ID + aynı Team ID + `notarized` |
| Ağ | `URLSession.shared` | Çerezsiz/önbelleksiz oturum, yalnızca GitHub, yalnızca HTTPS (TLS 1.2+), GitHub dışına yönlendirme reddedilir |
| CI | Sertifikayı sisteme `trustRoot` olarak ekliyor | Hiçbir kök eklenmez; anahtar yalnızca sürüm etiketinde açılır; action'lar SHA'ya sabit |
| Kurulum | `curl … \| bash`, karantina silinir | İndir → oku → çalıştır; `spctl` + Team ID denetimi, karantinaya dokunulmaz |

TLS doğrulaması hiçbir yerde kapatılmaz ya da özel sertifikaya sabitlenmez; sistemin güven deposu kullanılır.

## Özellikler

- **⌘Tab / ⌥Tab, pencere pencere:** büyük önizlemeler, ızgara/liste/gruplu görünüm, tüm tarayıcı profilleri ve Space'ler, kartta kapat ve böl düğmeleri, tek uygulama filtresi, favori klasörler kenar çubuğu.
- **Ses çıkışı (⌘ basılı + ⇧):** cihazlar arasında döngü, çıkarılan kulaklıkları hatırlar, uygulama başına ses cihazı.
- **Ekran bölme (⌘<):** 9 düzen, çoklu ekran desteği.
- **Ekran görüntüsü ve kayıt:** ⌘⇧3 bulunduğun ekran, ⌘⇧4 alan, ⌘⇧6 kaydırmalı ekran görüntüsü, ⌘⇧5 palet ve MP4/H.264 (H.265, ProRes) kayıt.
- **Harici ekranlar:** DDC ile parlaklık ve ses, ⌘⇧< ile tam karartma.
- **Finder:** fare yan tuşlarıyla geri/ileri, Dock'a sürükleyince uygulamayı öne getirme.
- **Kendini güncelleme**, Türkçe/İngilizce arayüz, girişte açılma.

Ayrıntılı kullanım için özgün projenin [README'sine](https://github.com/debelemez/AudioTab#readme) bakın; kısayollar ve ayarlar aynıdır.

## Kurulum

macOS 13 veya üstü, Apple Silicon ve Intel.

**Hazır sürüm:** [Releases](https://github.com/demirciemre/audiotab/releases/latest) sayfasından `AudioTab.zip`'i indirin, açın, `AudioTab.app`'i **Uygulamalar** klasörüne sürükleyin. Notarize edildiği için uyarı çıkmaz. Ya da:

```bash
curl -fsSL https://raw.githubusercontent.com/demirciemre/audiotab/main/install.sh -o install.sh
```

```bash
bash install.sh
```

**Kaynaktan:** Xcode komut satırı araçları yeterli. Yerelde derlenen uygulama karantinaya alınmadığı için uyarı vermez; ama kendini güncellemez, `git pull` + yeniden derleme ile güncellenir.

```bash
./build.sh --install
```

İlk açılışta **Erişilebilirlik** ve **Ekran Kaydı** izinlerini verin (Sistem Ayarları › Gizlilik ve Güvenlik), Ekran Kaydı'ndan sonra uygulamayı bir kez kapatıp açın. Bu sürümün paket kimliği farklı (`com.uniwebsolution.audiotab`) olduğu için özgün AudioTab'dan geçişte izinler bir kez yeniden istenir; ayarlar ise otomatik taşınır.

## Bakımcı: imza ve sürüm

1. Apple Developer hesabında **Developer ID Application** sertifikası oluşturun, anahtarıyla birlikte `.p12` olarak dışa aktarın.
2. App Store Connect › Users and Access › Integrations › **App Store Connect API**'de bir anahtar (`.p8`) oluşturun.
3. GitHub › Settings › Secrets and variables › Actions altına ekleyin:
   `DEVELOPER_ID_P12` (base64), `DEVELOPER_ID_P12_PASSWORD`, `NOTARY_KEY_P8` (base64), `NOTARY_KEY_ID`, `NOTARY_ISSUER_ID`.
4. `install.sh` içindeki `TEAM_ID`'yi 10 karakterlik Team ID'nizle değiştirin.
5. Güncelleyici ve `install.sh` GitHub'a kimliksiz eriştiği için sürümlerin yayınlandığı repo **herkese açık** olmalı.

Sürüm çıkarmak: `CHANGELOG.md` `[Unreleased]` altında biriken maddelerle `vc.py release` bir `vX.Y.Z` etiketi atar. CI o etiketi derler, imzalar, notarize eder ve `AudioTab.zip`'i Release'e ekler. Etiket `VERSION` dosyasıyla eşleşmelidir. Uygulama içindeki geçmiş için `Sources/Changelog.swift`'e de bir kayıt ekleyin.

Yerelde imzalı ve notarize edilmiş bir derleme için:

```bash
SIGN_IDENTITY="Developer ID Application: Ad Soyad (TEAMID)" NOTARY_PROFILE=audiotab ./build.sh --universal --notarize
```

(`NOTARY_PROFILE`: `xcrun notarytool store-credentials audiotab` ile bir kez kaydedilir.)

## Lisans

MIT. Bkz. [LICENSE](LICENSE). Özgün kod © 2026 Firewall Studio.
