# Değişiklik Günlüğü

Bu projedeki tüm önemli değişiklikler burada tutulur.
Biçim: [Keep a Changelog](https://keepachangelog.com/tr-TR/1.1.0/). Değişiklikler [Unreleased] altında birikir; sürüm yalnızca yayın yapılınca atılır.

## [Unreleased]

### Eklenenler

- Güvenlik denetimi raporu: docs/security-audit.md (Cloudflare security-audit, standard profil)

### Düzeltilenler

- Notarize zaman aşımı 2 saate çıktı ve reddedilmeden ayrı raporlanıyor
- Tanı bilgisi kopyalanırken e-postalar kısaltmadan önce gizleniyor; hesap adları maskeleniyor
- Güvenli giriş sırasında ⌘Tab ayarı değiştirilince macOS ⌘Tab'ı kapanmıyor; karartma klavye kilidi yalnızca ⌘⇧< kaçışı açıkken devrede; sinyaller güvenli işleniyor

### Güvenlik

- Finder favorileri arşivi artık yalnızca izinli plist türleriyle açılıyor (güvensiz NSKeyedUnarchiver kaldırıldı); .app favorileri çalıştırılmak yerine Finder'da gösteriliyor
- Güncelleyici: sürüm etiketi her yolda doğrulanıyor, sürüm sayfası yalnızca GitHub, paket hedefin yanında yeniden doğrulanıp tek adımda yerine taşınıyor, iptal edilmiş imzalar reddediliyor
- CI: derleme işi salt okunur, yazma yetkisi yalnızca imzalı etiket sonrası yayın işinde; imza sırları main ve PR'larda runner'a hiç verilmiyor
- install.sh sembolik bağlantılı paketi reddediyor ve kurulan uygulamayı yeniden doğruluyor; .gitignore .p8/.pem/.env dosyalarını kapsıyor

## [v2.5.1] - 2026-10-31

_Doğrulama: yerel derleme geçti; CI'da 5/5 imza sırrı dolu; v2.5.0 Developer ID imzalı yerel derleme açılışta çökmüyor_

### Düzeltilenler

- Sürüm etiketinde imza sırları eksikse CI artık kırmızı biter; imzasız sürüm sessizce yayınlanmaz
- İndirilebilir AudioTab.zip artık Release'e ekleniyor: ilk imzalı ve notarize edilmiş sürüm (v2.5.0'da imza sırları eksikti)

## [v2.5.0] - 2026-10-31

_Doğrulama: universal derleme (arm64+x86_64) yerelde ve CI'da geçti; Developer ID + hardened runtime imza zinciri doğrulandı; uygulama açılışta çökmüyor_

### Eklenenler

- Özgün AudioTab'ın (MIT) tüm özellikleri: pencere bazlı ⌘Tab, ⌘⇧ ile ses çıkışı, uygulama başına ses cihazı, ⌘< ekran bölme, ekran görüntüsü ve MP4 kayıt, harici ekran parlaklığı, Finder yardımcıları
- Özgün AudioTab'ın ayarları ilk açılışta taşınır

### Güvenlik

- Developer ID ile hardened runtime imza ve Apple notarize: macOS'un "doğrulanamadı" uyarısı çıkmaz
- Güncellemeler yalnızca aynı ekibin Developer ID'siyle imzalı ve notarize edilmiş paketse kurulur; kendinden imzalı sertifika kaldırıldı
- Güncelleme istekleri ve yönlendirmeleri yalnızca GitHub'a, yalnızca HTTPS (TLS 1.2+) ile; çerezsiz, önbelleksiz oturum
- install.sh karantinayı silmez; paketi Gatekeeper ve sabit Team ID ile denetler
- CI artık hiçbir sertifikayı güvenilir kök olarak eklemiyor; action'lar commit SHA'sına sabitlendi

[Unreleased]: https://github.com/demirciemre/audiotab/compare/v2.5.1...HEAD
[v2.5.1]: https://github.com/demirciemre/audiotab/compare/v2.5.0...v2.5.1
[v2.5.0]: https://github.com/demirciemre/audiotab/releases/tag/v2.5.0
