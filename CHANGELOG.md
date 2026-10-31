# Değişiklik Günlüğü

Bu projedeki tüm önemli değişiklikler burada tutulur.
Biçim: [Keep a Changelog](https://keepachangelog.com/tr-TR/1.1.0/). Değişiklikler [Unreleased] altında birikir; sürüm yalnızca yayın yapılınca atılır.

## [Unreleased]

### Eklenenler

- Özgün AudioTab'ın (MIT) tüm özellikleri: pencere bazlı ⌘Tab, ⌘⇧ ile ses çıkışı, uygulama başına ses cihazı, ⌘< ekran bölme, ekran görüntüsü ve MP4 kayıt, harici ekran parlaklığı, Finder yardımcıları
- Özgün AudioTab'ın ayarları ilk açılışta taşınır

### Güvenlik

- Developer ID ile hardened runtime imza ve Apple notarize: macOS'un "doğrulanamadı" uyarısı çıkmaz
- Güncellemeler yalnızca aynı ekibin Developer ID'siyle imzalı ve notarize edilmiş paketse kurulur; kendinden imzalı sertifika kaldırıldı
- Güncelleme istekleri ve yönlendirmeleri yalnızca GitHub'a, yalnızca HTTPS (TLS 1.2+) ile; çerezsiz, önbelleksiz oturum
- install.sh karantinayı silmez; paketi Gatekeeper ve sabit Team ID ile denetler
- CI artık hiçbir sertifikayı güvenilir kök olarak eklemiyor; action'lar commit SHA'sına sabitlendi
