# AudioTab: 2.4.2'den sonra yapılanlar ve kendi reponuza alma rehberi

Bu doküman, [debelemez/AudioTab](https://github.com/debelemez/AudioTab) 2.4.2 (commit `6130cf0`) üzerine [demirciemre/audiotab](https://github.com/demirciemre/audiotab) reposunda yapılan değişiklikleri anlatır. Amaç, bu değişiklikleri kendi reponuza **kendi kimliğinizle** almanız. Bunun için kişisel bir anahtar, sertifika ya da hesap bilgisine gerek yok; her şey herkese açık repodan alınır.

Nasıl kullanılır: dokümanı kendi reponuzda çalışan bir Claude oturumuna verin ve [6. bölümdeki](#6-claudea-verilecek-istem) istemle başlayın. Claude önce iki repoyu karşılaştırıp bir plan çıkarır. Hangi değişiklikleri alacağınıza siz karar verirsiniz.

İçindekiler:
1. [Ne yapıldı (özet)](#1-ne-yapıldı-özet)
2. [Değişikliklerin ayrıntılı listesi](#2-değişikliklerin-ayrıntılı-listesi)
3. [Kaynağa nasıl bakılır](#3-kaynağa-nasıl-bakılır)
4. [Yol A: Apple Developer hesabınız varsa](#4-yol-a-apple-developer-hesabınız-varsa)
5. [Yol B: Apple Developer hesabınız yoksa](#5-yol-b-apple-developer-hesabınız-yoksa)
6. [Claude'a verilecek istem](#6-claudea-verilecek-istem)
7. [Doğrulama kontrol listesi](#7-doğrulama-kontrol-listesi)
8. [Paketin içeriği](#8-paketin-içeriği)

---

## 1. Ne yapıldı (özet)

Özellikler aynı kaldı. Değişenler altı başlıkta toplanıyor:

| Başlık | Kısaca | Yol A | Yol B |
|---|---|---|---|
| **Güven zinciri** | Kendinden imzalı sertifika yerine Apple Developer ID, hardened runtime ve notarize. "Apple could not verify…" uyarısı kalkar. | ✅ | — |
| **Güvenli güncelleyici** | Güncelleme yalnızca aynı Team ID'yle imzalı ve notarize edilmiş paketse kurulur. Ağ yalnızca GitHub'a, yalnızca HTTPS. | ✅ | kısmen |
| **Güvenlik sıkılaştırmaları** | Güvensiz arşiv açma kaldırıldı, tanı bilgisinde e-posta gizleme, sinyal işleme, install.sh ve CI sıkılaştırması. | ✅ | ✅ |
| **Hız** | ⌘Tab paneli ~130 ms yerine 60–95 ms'de açılıyor; açılırken diğer tuşlar gecikmiyor. | ✅ | ✅ |
| **Hata düzeltmeleri** | Ekrana sığmayan kartlar artık görünmez kalmıyor (⌥Tab kaydırma), macOS ⌘Tab'ı ile çift panel açılmıyor, monitör numarası seçiciyi kapatmıyor. | ✅ | ✅ |
| **Görsel kimlik ve README** | Uygulama simgesi, tek renkli menü çubuğu simgesi, iki dilli tanıtım README'si ve görselleri. | isteğe bağlı | isteğe bağlı |

Önemli: Yol A'ya geçerseniz **mevcut kullanıcılarınızın otomatik güncellemesi** bir kez kırılır. Nedeni ve çözümü [4.7'de](#47-mevcut-kullanıcılarınızı-taşıma).

---

## 2. Değişikliklerin ayrıntılı listesi

Commit'ler `demirciemre/audiotab` reposuna aittir. Geçmişler bağlı değil (kod kopyalanarak başlandı); karşılaştırma için [3. bölüme](#3-kaynağa-nasıl-bakılır) bakın.

### 2.1 Güven zinciri ve dağıtım (Yol A)

Commit: `af06b1a`, `b4bfe26`, `36be0f3`

- **`build.sh`**
  - `SIGN_IDENTITY` verilirse `--options runtime --timestamp` ile Developer ID imzası atar; verilmezse ad-hoc imzalar.
  - `--notarize`: `xcrun notarytool submit --wait --timeout 2h`, sonra `stapler staple`, `stapler validate`, `spctl --assess`. Zaman aşımı ile red ayrı mesajlarla raporlanır; Apple yeni hesapların ilk gönderimlerini saatlerce bekletebilir.
  - Kimlik bilgisi iki yoldan biriyle gelir: `NOTARY_PROFILE` (keychain profili) ya da `NOTARY_KEY` / `NOTARY_KEY_ID` / `NOTARY_ISSUER` (App Store Connect API anahtarı).
  - `VERSION` semver olarak doğrulanır; `xattr -cr` yalnızca derlenen pakete uygulanır, tüm repoya değil.
- **`.github/workflows/release.yml`**
  - İki iş: `build` (salt okunur, `contents: read`) ve `release` (`contents: write`). `release` yalnızca imzalı bir `v*` etiketi derlendiğinde çalışır.
  - İmza sırları yalnızca etiket push'unda ve `workflow_dispatch`'te runner'a verilir; main ve PR derlemelerinde hiç açılmaz.
  - Etiket `v$VERSION`'la eşleşmeli. Sırlardan biri eksikse etiket derlemesi kırmızı biter; imzasız sürüm sessizce yayınlanmaz.
  - Hiçbir sertifika `trustRoot` olarak eklenmez. Action'lar commit SHA'sına sabit, `persist-credentials: false`. Derleme zaman sınırı 180 dakika.
- **`install.sh`**
  - `curl | bash` yerine önce indirilip okunur. `curl --proto '=https' --tlsv1.2`.
  - Paket, Developer ID + Team ID + `notarized` kod gereksinimiyle `codesign -R` ile denetlenir, ardından `spctl --assess`.
  - Karantina bayrağı silinmez. Sembolik bağlantılı paket reddedilir. Kopyalanan uygulama yeniden doğrulanır.

### 2.2 Güvenli güncelleyici (`Sources/Updater.swift`)

Commit: `af06b1a`, `36be0f3`

- Kod gereksinimi, sabit SHA-1 parmak izi yerine şu: `anchor apple generic and identifier "<BUNDLE_ID>" and certificate 1[field.1.2.840.113635.100.6.2.6] and certificate leaf[field.1.2.840.113635.100.6.1.13] and certificate leaf[subject.OU] = "<TEAM_ID>" and notarized`.
- Team ID, çalışan kopyanın kendi imzasından okunur (`SecCodeCopySelf` → `SecCodeCopySigningInformation`). Ad-hoc derlenmiş kopyada Team ID yoktur; o kopya kendini güncellemez ve Ayarlar'da "GitHub'da aç" düğmesi gösterir.
- `SecStaticCodeCheckValidity` bayrakları: tüm mimariler, iç içe kod, katı doğrulama ve sertifika iptal denetimi.
- Ağ: çerezsiz ve önbelleksiz (`ephemeral`) oturum, en az TLS 1.2. Yalnızca `github.com`, `api.github.com`, `objects.githubusercontent.com`, `release-assets.githubusercontent.com`. Yönlendirmeler de bu listeye karşı denetlenir.
- Sürüm etiketi her yolda `^v?\d{1,6}\.\d{1,6}\.\d{1,6}$` ile doğrulanır; URL'lerde zorla açma (`!`) yok; sürüm sayfası yalnızca izinli bir GitHub adresiyse açılır.
- Kurulum: yeni paket hedefin yanına geçici bir adla kopyalanır, **orada yeniden doğrulanır**, sonra tek adımda yerine taşınır; hata olursa eskisi geri konur. Paket içinde sembolik bağlantılı `AudioTab.app` reddedilir.

### 2.3 Güvenlik sıkılaştırmaları (iki yolda da)

Commit: `36be0f3`. Denetim raporu: `docs/security-audit.md`.

- **`Sources/Favorites.swift`**: Finder favorileri arşivi `NSKeyedUnarchiver.unarchivedObject(ofClasses:)` ile, yalnızca plist türleri izinli olarak açılır (`requiresSecureCoding = false` kaldırıldı).
- **`Sources/Switcher.swift`**: favori bir paketse (ör. `.app`) çalıştırılmaz, Finder'da gösterilir.
- **`Sources/BrowserProfiles.swift`**: tanı bilgisinde e-postalar kısaltmadan önce gizlenir, hesap adları maskelenir.
- **`Sources/App.swift`**: SIGTERM/SIGINT `DispatchSource.makeSignalSource` ile ana kuyrukta işlenir (sinyal işleyicide güvensiz kod yok). Güvenli giriş açıkken ⌘Tab ayarı değişirse macOS ⌘Tab'ı kapanmaz.
- **Karartma klavye kilidi** yalnızca ⌘⇧< kaçış kısayolu açıkken devreye girer; kısayol kapalıysa klavye kilitlenmez.
- **`Sources/Monitors.swift`**: DDC'den okunan değer en büyük değerle sınırlanır.
- **`.gitignore`**: `*.p8`, `*.pem`, `.env*`, `notary.json` eklendi.

### 2.4 Hız (`Sources/Switcher.swift`)

Commit: `3f4445c`. Ölçüm, sizin bilgisayarınızda değil bu repodaki geliştirme Mac'inde yapıldı: önce ~130 ms (ilk açılışta 270–420 ms), sonra 60–95 ms.

- Eskiden `WindowList.build` (pencere listesi ve AX taraması) **tuş yakalayıcının (CGEventTap) içinde**, ana iş parçacığında çalışıyordu. O süre boyunca bilgisayardaki tüm tuş basışları bekliyordu. Uzun sürerse macOS tuş yakalayıcıyı kapatıyor ve tuşlar arkadaki uygulamaya gidiyordu.
- Şimdi `begin()` Tab'ı hemen yutar, `active = true` yapar ve işi `DispatchQueue.main.async` ile `prepareSession()`'a bırakır.
- Liste ve panel yerleşimi, var olan 60 ms'lik bekleme süresinin **içinde** hazırlanır: `ui.show(..., reveal: false)`. Süre dolunca `ui.reveal()` paneli yalnızca öne getirir.
- Hazırlık bitmeden gelen Tab'lar `pendingSteps`'te birikir. Hazırlık bitmeden ⌘ bırakılırsa `pendingCommit` ile yerleşim yapılmadan doğrudan pencereye geçilir.
- Ölçüm kayıtları `os.Logger` ile (`subsystem` = paket kimliği, `category` = `perf`), `notice` seviyesinde. Okumak için: `log show --last 10m --predicate 'subsystem == "<BUNDLE_ID>" AND category == "perf"'`. `info` seviyesi diske yazılmadığı için `notice` kullanıldı.
- Tanı kayıtları: tuş yakalayıcı kapatılırsa, güvenli giriş açıksa ve ⌥/⌘ basılıyken yakalanmadan geçen bir Tab olursa kayıt düşülür.

### 2.5 Hata düzeltmeleri

Commit: `3f4445c`, `ec55d5d`

- **Görünmeyen kartlar** (`layoutGrid`): ekrana sığmayan satırlar hiç çizilmiyor ama Tab seçimi onların üzerinden geçiyordu.
  - Önizlemeler tüm pencereler sığana kadar küçülür, en fazla `minGridThumbH = 130`'a kadar.
  - Yine sığmazsa panel seçili satıra kayar (`firstRow`, `followSelection`).
  - Trackpad ve fare tekerleğiyle satır satır kaydırılabilir; bunun için panel görünürken yerel bir `scrollWheel` izleyicisi çalışır.
  - Üst ve alt kenarda "↑/↓ N pencere daha" yazar.
- **Çift ⌘Tab paneli**: güvenli giriş sonrasında macOS'un ⌘Tab'ı geri açıkken AudioTab de paneli açıyordu. `Switcher.nativeCmdTabOn` doğruyken ⌘ profili panel açmaz. `App.guardTick` güvenli giriş açılınca bu bayrağı ayarlar.
- **Monitör numarası kartı** (`Sources/Tiling.swift`, `MonitorBadges.show(_:target:avoid:)`): ekran bölme seçicisinin çerçevesine değmeyen ilk konuma yerleşir. Sıra: üst orta, üst köşeler, alt kenar.
- **Gizlilik metni** (İzinler sekmesi): "internete gönderilmez" yanlıştı. Uygulama güncelleme kontrolü için GitHub'a bağlanıyor; metin buna göre düzeltildi.
- **`build.sh --install`** derlenen kopyayı proje klasöründe bırakmaz. Önceden Spotlight'ta iki AudioTab görünüyordu.

### 2.6 Görsel kimlik ve README (isteğe bağlı)

Commit: `ec55d5d` ve sonrası

- **Uygulama simgesi**: `Icon/AppIcon.icon` (Icon Composer). Önde içine ses dalgası oyulmuş bir pencere kartı, arkasında soluk bir kart, çivit mavisi zemin.
  - `tools/make_icon.sh` simgeyi `Resources/Assets.car` ve `AppIcon.icns` olarak derler; bunun için Xcode 26 gerekir. Derlenmiş dosyalar repoda tutulur, böylece CI'da Xcode 26 olmasa da simge pakete girer.
  - `Info.plist`'e `CFBundleIconName` ve `CFBundleIconFile` eklendi.
- **Menü çubuğu simgesi**: `Sources/StatusIcon.swift`. Logonun tek renkli şablon (template) görüntüsü, kodla çiziliyor. Seçili ses cihazı artık simgede değil, ipucunda.
- **SVG halleri**: `docs/brand/` (renkli, siyah, beyaz, `currentColor`).
- **README**: İngilizce `README.md` ve Türkçe `README.tr.md`. Her özellik için temsili ekran görseli var; görseller `tools/readme-art/` içindeki sahnelerden Chrome ve `cwebp` ile iki dilde üretilir.
- Simgeyi ve görselleri kullanıp kullanmamak size kalmış. Kendi markanızı korumak isterseniz yalnızca 2.1–2.5'i alın.

### 2.7 Almamanız gerekenler (bu repoya özgü)

- Paket kimliği `com.uniwebsolution.audiotab`, repo adı `demirciemre/audiotab`, `install.sh` içindeki `TEAM_ID`. Kendi değerlerinizi kullanın.
- `Sources/Settings.swift` içindeki `com.firewallstudio.audiotab` ayar taşıma kodu. Bu kod, sizin uygulamanızdan bu repoya geçen kullanıcılar için yazıldı.
- `Sources/Changelog.swift` ve `CHANGELOG.md` içindeki 2.5.x kayıtları. Kendi sürüm notlarınızı yazın.
- `LICENSE` dosyasına eklenen atıf satırı.

---

## 3. Kaynağa nasıl bakılır

Kendi reponuzun kökünde, uzak bir remote eklemeden:

```bash
git fetch https://github.com/demirciemre/audiotab.git main
git diff 6130cf0 FETCH_HEAD -- Sources build.sh install.sh .github
```

Belirli bir değişikliğe bakmak için:

```bash
git show FETCH_HEAD:Sources/Updater.swift
git diff 6130cf0 FETCH_HEAD -- Sources/Switcher.swift
```

Geçmişler ortak değil; bu yüzden `git merge` ya da `cherry-pick` yerine farkları okuyup elle uygulamak daha güvenli. Bu repo MIT lisanslı ve herkese açık.

---

## 4. Yol A: Apple Developer hesabınız varsa

Sonuç: indirilen uygulama uyarısız açılır, otomatik güncelleme Apple'ın güven zinciriyle doğrulanır. Gereken: ücretli Apple Developer Program üyeliği.

### 4.1 Değerleri belirleyin

| Değer | Örnek | Nerede kullanılır |
|---|---|---|
| `<BUNDLE_ID>` | `com.firewallstudio.audiotab` (mevcut kullanıcılarınızın ayarları korunsun diye aynısı) | `build.sh`, `install.sh`, perf log subsystem |
| `<OWNER/REPO>` | `debelemez/AudioTab` | `UpdateConfig.repo`, `install.sh` |
| `<TEAM_ID>` | 10 karakter, developer.apple.com › Membership | `install.sh` (uygulama kendi imzasından okur) |

### 4.2 Developer ID Application sertifikası

1. Xcode › Settings › Accounts › hesabınız › **Manage Certificates** › **+** › **Developer ID Application**.
2. Anahtarlık Erişimi › Oturum Aç › Sertifikalarım: "Developer ID Application: <Ad> (<TEAM_ID>)" satırını anahtarıyla birlikte seçin › **Dışa Aktar** › `.p12`, güçlü bir parolayla.
3. `.p12` dosyasını repo **dışında** saklayın.

Not: Sertifika 5 yıl geçerlidir ve otomatik uzatılamaz. Süre dolmadan yenisi oluşturulup CI sırları güncellenir. O ana kadar imzalanmış sürümler çalışmaya devam eder.

### 4.3 Notarize için App Store Connect API anahtarı

1. appstoreconnect.apple.com › Users and Access › **Integrations** › App Store Connect API › **+**, rol: Developer.
2. `AuthKey_<KEYID>.p8` dosyasını indirin; yalnızca bir kez indirilebilir. **Key ID** ve sayfanın üstündeki **Issuer ID**'yi not edin.

### 4.4 GitHub Actions sırları

Repo › Settings › Secrets and variables › Actions altına beş sır ekleyin. Komut satırından:

```bash
base64 -i Certificates.p12 | gh secret set DEVELOPER_ID_P12
gh secret set DEVELOPER_ID_P12_PASSWORD     # parolayı sorar
base64 -i AuthKey_<KEYID>.p8 | gh secret set NOTARY_KEY_P8
gh secret set NOTARY_KEY_ID                 # 10 karakterlik Key ID
gh secret set NOTARY_ISSUER_ID              # UUID biçiminde
```

Dosya yolunu yanlış verirseniz sır boş kaydedilir. `release.yml` her sırrın dolu olup olmadığını ✔/✖ ile yazar; etiket derlemesinde biri eksikse durur. Bunu bir kez **Actions › Run workflow** ile deneyin.

### 4.5 Kodu uygulayın

[2.1](#21-güven-zinciri-ve-dağıtım-yol-a)–[2.5](#25-hata-düzeltmeleri) arasını kendi değerlerinizle uygulayın. `signing/AudioTab.pem`, kendinden imzalı sertifikayla ilgili adımlar ve `trustRoot` kaldırılır.

### 4.6 İlk sürüm

1. `VERSION` dosyasını artırın, etiketi atın: `git tag v<sürüm> && git push origin v<sürüm>`.
2. CI derler, imzalar, notarize eder ve `AudioTab.zip`'i Release'e ekler. İlk gönderimler bir saatten uzun sürebilir; zaman sınırı bu yüzden 2 saat.
3. Doğrulayın:

```bash
codesign -dv --verbose=2 AudioTab.app 2>&1 | grep -E "Authority|TeamIdentifier|Runtime"
spctl --assess --type execute -vv AudioTab.app
xcrun stapler validate AudioTab.app
```

### 4.7 Mevcut kullanıcılarınızı taşıma

Bugünkü 2.4.2 güncelleyicisi yalnızca `signing/AudioTab.pem` parmak iziyle imzalı paketi kabul eder. Developer ID ile imzalı yeni sürümü **reddeder**. İki seçenek var:

- **Basit:** Release notunda ve README'de "bu sürüme bir kez elle geçin" deyin. Kullanıcılar zip'i indirip uygulamayı değiştirir; sonraki güncellemeler otomatik gelir.
- **Köprü sürüm:** Son bir sürümü **eski sertifikayla** imzalayın. Bu sürümün güncelleyicisi hem eski parmak izini hem de yeni Developer ID gereksinimini kabul etsin (`or` ile). Bir sonraki sürüm Developer ID ile çıkar ve kullanıcılar otomatik geçer.

Paket kimliğini değiştirmezseniz ayarlar korunur. macOS izinleri (Erişilebilirlik, Ekran Kaydı) imzaya bağlı olduğu için kullanıcılar bunları **bir kez** yeniden verir.

---

## 5. Yol B: Apple Developer hesabınız yoksa

Sonuç: uygulama sizin bilgisayarınızda derlenir ve uyarısız çalışır. Yerelde derlenen uygulama karantinaya alınmadığı için Gatekeeper uyarısı çıkmaz. Başkalarına dağıtırsanız onların bilgisayarında uyarı çıkar; bu, hesap olmadan aşılamaz.

### 5.1 Uygulanacaklar

- [2.3 Güvenlik](#23-güvenlik-sıkılaştırmaları-iki-yolda-da), [2.4 Hız](#24-hız-sourcesswitcherswift), [2.5 Hata düzeltmeleri](#25-hata-düzeltmeleri); isterseniz [2.6](#26-görsel-kimlik-ve-readme-isteğe-bağlı).
- 2.1 ve 2.2'den yalnızca platforma bağlı olmayanlar: HTTPS ve GitHub dışına yönlendirmeyi reddetme, sürüm etiketi doğrulama, kopyala-doğrula-taşı kurulumu. Developer ID gereksinimi ve notarize uygulanmaz.

### 5.2 Kalıcı yerel imza (izinler her derlemede kaybolmasın)

Ad-hoc imza (`codesign --sign -`) her derlemede değişir; macOS da Erişilebilirlik ve Ekran Kaydı izinlerini her seferinde yeniden ister. Kalıcı bir yerel imza bunu önler:

1. Anahtarlık Erişimi › menüden **Sertifika Asistanı › Sertifika Oluştur…**
2. Ad: `AudioTab Local`, Kimlik türü: **Kendinden imzalı kök**, Sertifika türü: **Kod İmzalama**.
3. Derleyin:

```bash
SIGN_IDENTITY="AudioTab Local" ./build.sh --install
```

4. `build.sh` Developer ID için `--timestamp` kullanır. Apple'ın zaman damgası sunucusu kendinden imzalı sertifikaya damga vermez; bu yüzden `SIGN_IDENTITY` kendinden imzalıysa `--timestamp=none` kullanılmalı. Claude'dan `build.sh`'e bunu ayıran küçük bir koşul eklemesini isteyin. `--options runtime` kalabilir.

Bu sertifika yalnızca sizin anahtarlığınızda durur, hiçbir yere yüklenmez ve **hiçbir zaman sisteme güvenilir kök olarak eklenmemelidir**.

### 5.3 Güncellemeler

- Bu repodaki güncelleyici yalnızca Developer ID ile imzalı ve notarize edilmiş paketleri kurar. Yerel imzalı bir kopyada otomatik güncelleme kapalı kalır, Ayarlar › Sürümler'de "GitHub'da aç" düğmesi görünür. Kendi bilgisayarınızda kullanım için en güvenli yol budur: güncellemek için `git pull` ve yeniden derleme yeterli.
- Mevcut kendinden imzalı güncelleyicinizi (sabit SHA-1 parmak izi) korumak isterseniz, en azından 2.2'deki ağ kısıtlarını ve kopyala-doğrula-taşı kurulumunu ekleyin. `install.sh` içindeki karantina silme (`xattr -dr com.apple.quarantine`) Gatekeeper'ı atlatır; bunu kullanıcıya açıkça söyleyin ya da kaldırın.

---

## 6. Claude'a verilecek istem

Kendi reponuzun kökünde açılmış bir Claude Code oturumuna bu dokümanla birlikte şunu yazın. Yolu A ya da B olarak seçin:

```text
Bu klasör AudioTab'ın kendi repom (2.4.2, commit 6130cf0). Ekteki HANDOFF.md,
demirciemre/audiotab reposunda bu sürümün üstüne yapılan değişiklikleri anlatıyor.

1. HANDOFF.md'yi baştan sona oku.
2. Kaynağı şu komutlarla incele, remote ekleme:
   git fetch https://github.com/demirciemre/audiotab.git main
   git diff 6130cf0 FETCH_HEAD -- Sources build.sh install.sh .github
3. Yol <A|B> için bir plan çıkar: her madde için hangi dosyalar değişecek, neyi
   ALMAYACAĞIZ (2.7), hangi değerler benim (paket kimliği, repo, Team ID).
4. Planı bana göster, onayımı bekle. Sonra her başlığı ayrı commit'te uygula,
   her adımda ./build.sh ile derle.
5. Bitince 7. bölümdeki kontrol listesini benimle birlikte yürüt.

Benim sertifikalarım ve anahtarlarım repoya hiçbir zaman girmesin.
```

---

## 7. Doğrulama kontrol listesi

- [ ] `./build.sh` hatasız derleniyor; `./build.sh --universal` hem arm64 hem x86_64 üretiyor.
- [ ] İzinler verildikten sonra ⌘Tab ve ⌥Tab açılıyor. `perf` kayıtlarında `panel shown` 100 ms'nin altında.
- [ ] 25'ten fazla pencere açıkken ⌥Tab: seçim her basışta görünür bir kartta, panel kayıyor, kenarda "N pencere daha" yazıyor.
- [ ] Bir parola alanına tıklayıp ⌘Tab'a basınca yalnızca macOS'un paneli açılıyor. Alandan çıkınca 2 saniye içinde AudioTab devralıyor.
- [ ] İki monitörde ⌘<: monitör numarası kartı seçicinin üstüne binmiyor.
- [ ] Finder favorileri açık; `.app` bir favori çalıştırılmıyor, Finder'da gösteriliyor.
- [ ] Yol A: `spctl --assess` "accepted, source=Notarized Developer ID" diyor; `install.sh` kuruyor; eski sürümden otomatik güncelleme geliyor (köprü sürüm kullandıysanız).
- [ ] Yol B: yeniden derlemeden sonra izinler korunuyor (kalıcı yerel imza).

---

## 8. Paketin içeriği

| Yol | Ne |
|---|---|
| `HANDOFF.md` | Bu doküman |
| `README.md`, `README.tr.md` | Yeni tanıtım README'leri (İngilizce, Türkçe) |
| `docs/images/` | README görselleri: `en/`, `tr/` ve `icon.png` |
| `docs/brand/` | Simgenin SVG halleri |
| `Icon/AppIcon.icon/` | Icon Composer kaynağı |
| `Resources/` | Derlenmiş simge (`Assets.car`, `AppIcon.icns`) |
| `tools/` | Simge derleme ve README görseli üretme betikleri |

Bu pakette sertifika, anahtar, parola, Team ID ya da kişisel bilgi **yoktur**. Kodun kendisi pakette değil; doğrudan herkese açık repodan alınır (3. bölüm).
