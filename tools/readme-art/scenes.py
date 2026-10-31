#!/usr/bin/env python3
"""README görselleri: AudioTab'ın özelliklerini anlatan 2B ekran görüntüsü benzeri sahneler.

Gerçek ekran görüntüsü değildir; uygulama adları ve simgeler geneldir (marka yok).
Her sahne bir HTML dosyasına yazılır, render.sh onları Chrome ile docs/images/*.png yapar.
Kullanım: tools/readme-art/render.sh
"""
import html, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/audiotab-art"
LANG = sys.argv[2] if len(sys.argv) > 2 else "tr"   # tr | en
os.makedirs(OUT, exist_ok=True)

# Görsellerdeki Türkçe metinlerin İngilizcesi (arayüz terimleri Sources/Localization.swift ile aynı).
# Uzun ifadeler önce değiştirilir; kısa sözcükler uzunların içinde kalmaz.
EN = {
 "Cmt 31 Eki 16:40": "Sat Oct 31 4:40 PM", "Ekim 2026": "October 2026",
 "Proje panosu — Tarayıcı": "Project board — Browser", "main.swift — Kod": "main.swift — Code", "~/projeler — zsh": "~/projects — zsh",
 "Proje panosu": "Project board", "Toplantı notları": "Meeting notes", "Çalma listesi": "Playlist", "Tatil albümü": "Holiday album",
 "Ekip sohbeti": "Team chat", "Gelen kutusu": "Inbox", "Logo taslağı": "Logo draft", "Dokümantasyon": "Documentation",
 "Alışveriş": "Shopping", "Hafta": "Week", "Albüm": "Album", "Aile": "Family", "Radyo": "Radio", "Bülten": "Newsletter",
 "Afiş": "Poster", "afiş.png": "poster.png", "Haberler": "News", "Ekip": "Team",
 "⌘ basılı · Tab sonraki · ⇧Tab önceki · bırakınca o pencereye geçer": "Hold ⌘ · Tab next · ⇧Tab previous · release to switch to that window",
 "↑ 4 pencere daha": "↑ 4 more windows", "↓ 6 pencere daha": "↓ 6 more windows",
 "F: yalnızca seçili uygulamanın pencereleri · A: filtreyi değiştir · kenar çubuğundan klasöre tek tık": "F: only the selected app's windows · A: change filter · one click to a folder in the sidebar",
 "Panel açıkken": "While the panel is open", "pencereyi kapat": "close window", "uygulamadan çık": "quit app",
 "ses cihazını değiştir": "change sound device", "sadece bu uygulama": "only this app", "filtreyi değiştir": "change filter",
 "sonraki": "next", "önceki": "previous", "gezin": "navigate", "küçült": "minimize", "gizle": "hide", "vazgeç": "cancel", ">geç<": ">switch<",
 "Kablosuz Kulaklık": "Wireless Headphones", "MacBook Hoparlörleri": "MacBook Speakers", "Masaüstü Hoparlör": "Desktop Speaker",
 "Harici monitör · DDC/CI": "External display · DDC/CI", "Harici Monitör": "External Display", "Harici monitör": "External display",
 "Ses çıkışı değişti": "Sound output changed", "basılıyken": "held", "Ses cihazları · sırayla": "Sound devices · in order",
 "Çıkarılan kulaklığı hatırlar, takınca geri döner": "Remembers unplugged headphones and switches back when you plug them in",
 "Uygulamaya göre ses cihazı": "Sound device per app", "Uygulama öne gelince ses kendiliğinden o cihaza geçer": "When an app comes to the front, sound moves to its device",
 "⌘Tab panelinde ses cihazını değiştir": "change the sound device in the ⌘Tab panel", "Kulaklık": "Headphones",
 "Ekranın hangi bölmesine?": "Which part of the screen?", "1 · Dahili ekran · buradasın": "1 · Built-in display · you're here",
 "2 · Harici monitör": "2 · External display", "Hedef monitör": "Target display",
 "1–9 düzen seç · ↩ seç · Tab monitör değiştir · Esc kapat": "1–9 pick a layout · ↩ choose · Tab change display · Esc close",
 "Sonuç: 2 dikey bölme": "Result: 2 columns", "Tam ekran": "Full screen", "2 dikey": "2 columns", "2 yatay": "2 rows", "3 dikey": "3 columns",
 "Bulunduğun ekran": "Current screen", "Kaydırmalı": "Scrolling", "Kayıt": "Record", "Alan": "Area",
 "Sen kaydırırsın, AudioTab yakalar": "You scroll, AudioTab captures", "Tek parça uzun ekran görüntüsü · ⌘⇧6": "One long screenshot · ⌘⇧6",
 "Monitör 1 · DDC/CI ile parlaklık ve ses, menü çubuğundan": "Display 1 · brightness and volume over DDC/CI, from the menu bar",
 "Monitör 2 · ⌘⇧< ile tam karartma": "Display 2 · full blackout with ⌘⇧<", "Monitör 2 · ⌘⇧&lt; ile tam karartma": "Display 2 · full blackout with ⌘⇧&lt;",
 "tamamen karartıldı": "fully blacked out",
 "Farenin yan tuşları Finder klasörlerinde geri ve ileri gider": "The mouse side buttons go back and forward in Finder folders",
 "Projeler › audiotab": "Projects › audiotab", "‹ Geri": "‹ Back", "İleri ›": "Forward ›",
 "DOCK'A SÜRÜKLE-BIRAK": "DRAG TO DOCK", "Dock\'a sürükle-bırak": "Drag to Dock", "Dock'a sürükle-bırak": "Drag to Dock",
 "Dosyayı Dock'taki uygulamanın üstüne getir: beklemeden öne gelir, dosyayı doğrudan penceresine bırakırsın": "Hold a file over an app in the Dock: it comes forward right away, and you drop the file straight into its window",
 "Tarayıcı klavyeyi kilitledi": "Browser locked the keyboard", "⌘Tab şimdilik macOS'unki · kilit kalkınca AudioTab devralır": "⌘Tab is macOS's for now · AudioTab takes over when the lock lifts",
 "Parola alanları ve \"güvenli klavye girişi\" tuşları her uygulamadan gizler; AudioTab bunu fark eder": "Password fields and \"secure keyboard entry\" hide keys from every app; AudioTab notices",
 'Parola alanları ve "güvenli klavye girişi" tuşları her uygulamadan gizler; AudioTab bunu fark eder': 'Password fields and "secure keyboard entry" hide keys from every app; AudioTab notices',
 "Her şey hazır": "All set", "Kısayollar çalışıyor": "Shortcuts are working", "Gerekli izinler": "Required permissions",
 "⌘Tab, ⌥Tab ve ses kısayolu için; pencereleri kapatmak ve küçültmek için": "For ⌘Tab, ⌥Tab and the sound shortcut; to close and minimize windows",
 "Pencere önizlemeleri, ekran görüntüsü ve kayıt için": "For window previews, screenshots and recording",
 "Basılan tuşlar kaydedilmez, saklanmaz. Yalnızca güncelleme kontrolü için GitHub'a bağlanır.": "Keystrokes are never logged or stored. AudioTab only connects to GitHub to check for updates.",
 "● Verildi": "● Granted", "Erişilebilirlik": "Accessibility", "Ekran Kaydı": "Screen Recording",
 "Pencereler": "Windows", "İzinler": "Permissions", "Genel": "General", "Sürümler": "Versions",
 "Yeni sürüm: 2.6.0": "New version: 2.6.0", "Apple Developer ID ile imzalı": "Signed with Apple Developer ID", "Aynı Team ID": "Same Team ID",
 "Apple tarafından notarize edilmiş": "Notarized by Apple", "Sertifika iptal edilmemiş": "Certificate not revoked",
 "Yalnızca GitHub · HTTPS (TLS 1.2+)": "GitHub only · HTTPS (TLS 1.2+)", "Güncelle ve yeniden başlat": "Update and restart", ">Sonra<": ">Later<",
 "İndir · aç · çalıştır": "Download · open · run", "\"Apple could not verify…\" yok": "No \"Apple could not verify…\"", '"Apple could not verify…" yok': 'No "Apple could not verify…"',
 "Notarize edilmiş ve bileti zımbalanmış uygulama Gatekeeper'dan uyarısız geçer. Karantina bayrağına dokunulmaz.": "A notarized app with a stapled ticket passes Gatekeeper without a warning. The quarantine flag is left alone.",
 "Tarayıcılar": "Browsers", "Geliştirme": "Development", "Uygulamalar": "Apps", "Klasörler": "Folders", "Projeler": "Projects", "Favoriler": "Favorites",
 "Masaüstü": "Desktop", "İndirilenler": "Downloads", "Belgeler": "Documents", "Fotoğraflar": "Photos", "Tümü": "All",
 "Tarayıcı": "Browser", "Notlar": "Notes", "Müzik": "Music", "Mesajlar": "Messages", "Takvim": "Calendar", "Posta": "Mail",
 "Tasarım": "Design", "Ayarlar": "Settings", "Klasör": "Folder", ">Kod<": ">Code<", ">Ekran<": ">Screen<", ">Ses<": ">Sound<", ">İş<": ">Work<",
}

def translate(doc):
    if LANG != "en":
        return doc
    doc = doc.replace('lang="tr"', 'lang="en"')
    for k in sorted(EN, key=len, reverse=True):
        doc = doc.replace(k, EN[k])
    return doc

ACCENT = "#6366f1"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.frame{position:relative;overflow:hidden;border-radius:22px;
  background:radial-gradient(120% 90% at 15% 10%,#4338ca 0%,transparent 55%),
             radial-gradient(90% 80% at 90% 90%,#9333ea 0%,transparent 55%),
             radial-gradient(70% 60% at 70% 20%,#0ea5e9 0%,transparent 50%),#0f0b2e}
.menubar{position:absolute;top:0;left:0;right:0;height:30px;background:rgba(20,18,40,.55);backdrop-filter:blur(20px);
  display:flex;align-items:center;justify-content:flex-end;gap:16px;padding:0 16px;font-size:13px;color:rgba(255,255,255,.85)}
.glass{background:rgba(36,34,52,.72);backdrop-filter:blur(30px) saturate(1.4);border:1px solid rgba(255,255,255,.14);
  box-shadow:0 30px 80px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.12);border-radius:22px}
.center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.card{position:relative;border-radius:14px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);padding:10px;display:flex;flex-direction:column;align-items:center}
.card.sel{background:rgba(99,102,241,.32);border:2px solid #818cf8;box-shadow:0 0 0 4px rgba(99,102,241,.25)}
.title{font-size:12px;font-weight:600;margin-top:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.sub{font-size:11px;color:rgba(255,255,255,.55);white-space:nowrap}
.icon{border-radius:22%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.3)}
.btns{position:absolute;top:7px;right:7px;display:flex;gap:5px}
.btns i{width:16px;height:16px;border-radius:50%;display:block}
.badge{position:absolute;padding:2px 7px;border-radius:9px;font-size:10px;font-weight:700}
.kbd{display:inline-flex;align-items:center;justify-content:center;min-width:34px;height:34px;padding:0 9px;border-radius:8px;
  background:linear-gradient(#3a3852,#2a283d);border:1px solid rgba(255,255,255,.18);border-bottom-width:3px;font-size:15px;font-weight:600}
.hint{font-size:12px;color:rgba(255,255,255,.6);text-align:center}
.pill{display:inline-block;white-space:nowrap;padding:5px 12px;border-radius:999px;font-size:12px;font-weight:600;background:rgba(255,255,255,.1)}
.pill.on{background:#6366f1}
.row{display:flex;align-items:center;gap:12px}
.sec{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.5)}
"""

# --- Genel uygulama simgeleri (marka yok) --------------------------------------------------
G = {
 "globe": '<circle cx="12" cy="12" r="8.5" fill="none" stroke="#fff" stroke-width="2"/><path d="M3.5 12h17M12 3.5c3 3.2 3 13.8 0 17M12 3.5c-3 3.2-3 13.8 0 17" fill="none" stroke="#fff" stroke-width="1.8"/>',
 "note": '<rect x="5" y="4" width="14" height="16" rx="2.5" fill="#fff"/><path d="M8 9h8M8 12.5h8M8 16h5" stroke="#d97706" stroke-width="1.8" stroke-linecap="round"/>',
 "term": '<path d="M6 8l4 4-4 4" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16h6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>',
 "music": '<path d="M9 17V6.5l9-2V15" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/><circle cx="7" cy="17" r="2.6" fill="#fff"/><circle cx="16" cy="15" r="2.6" fill="#fff"/>',
 "chat": '<path d="M4 6.5A2.5 2.5 0 016.5 4h11A2.5 2.5 0 0120 6.5v7a2.5 2.5 0 01-2.5 2.5H10l-4.5 4v-4A2.5 2.5 0 014 13.5z" fill="#fff"/>',
 "cal": '<rect x="4" y="5" width="16" height="15" rx="3" fill="#fff"/><rect x="4" y="5" width="16" height="5" rx="2" fill="#ef4444"/><circle cx="9" cy="14" r="1.3" fill="#999"/><circle cx="13" cy="14" r="1.3" fill="#999"/><circle cx="17" cy="14" r="1.3" fill="#ef4444"/>',
 "code": '<path d="M9 7l-5 5 5 5M15 7l5 5-5 5" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
 "photo": '<circle cx="12" cy="12" r="3" fill="#fff"/><g fill="#fff" opacity=".85"><ellipse cx="12" cy="6" rx="2.2" ry="3"/><ellipse cx="12" cy="18" rx="2.2" ry="3"/><ellipse cx="6" cy="12" rx="3" ry="2.2"/><ellipse cx="18" cy="12" rx="3" ry="2.2"/></g>',
 "folder": '<path d="M3.5 7.5A2 2 0 015.5 5.5h4l2 2h7a2 2 0 012 2v8a2 2 0 01-2 2h-13a2 2 0 01-2-2z" fill="#fff"/>',
 "mail": '<rect x="3.5" y="6" width="17" height="12" rx="2.5" fill="#fff"/><path d="M4.5 7.5l7.5 5.5 7.5-5.5" fill="none" stroke="#0284c7" stroke-width="1.8"/>',
 "pen": '<path d="M5 19l2-6 8.5-8.5a2.1 2.1 0 013 3L10 16z" fill="#fff"/><path d="M5 19l4-1" stroke="#fff" stroke-width="2"/>',
 "gear": '<circle cx="12" cy="12" r="6.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-dasharray="3 2.1"/><circle cx="12" cy="12" r="2.6" fill="#fff"/>',
}
APPS = {
 "Tarayıcı": ("globe", "linear-gradient(135deg,#38bdf8,#2563eb)", "#1e3a8a"),
 "Notlar": ("note", "linear-gradient(135deg,#fde047,#f59e0b)", "#fef3c7"),
 "Terminal": ("term", "linear-gradient(135deg,#374151,#111827)", "#0b0f19"),
 "Müzik": ("music", "linear-gradient(135deg,#fb7185,#e11d48)", "#3f0a1a"),
 "Mesajlar": ("chat", "linear-gradient(135deg,#4ade80,#16a34a)", "#e8f5ec"),
 "Takvim": ("cal", "linear-gradient(135deg,#f8fafc,#e2e8f0)", "#f8fafc"),
 "Kod": ("code", "linear-gradient(135deg,#60a5fa,#4f46e5)", "#1b1e2e"),
 "Fotoğraflar": ("photo", "linear-gradient(135deg,#fb923c,#db2777)", "#2a1a14"),
 "Klasör": ("folder", "linear-gradient(135deg,#7dd3fc,#3b82f6)", "#eef4fb"),
 "Posta": ("mail", "linear-gradient(135deg,#7dd3fc,#0284c7)", "#f3f7fb"),
 "Tasarım": ("pen", "linear-gradient(135deg,#c084fc,#7c3aed)", "#1d1630"),
 "Ayarlar": ("gear", "linear-gradient(135deg,#9ca3af,#4b5563)", "#e5e7eb"),
}

def icon(app, size=56):
    g, bg, _ = APPS[app]
    s = int(size * .62)
    return (f'<div class="icon" style="width:{size}px;height:{size}px;background:{bg}">'
            f'<svg width="{s}" height="{s}" viewBox="0 0 24 24">{G[g]}</svg></div>')

def thumb(app, w, h, variant=0):
    """Pencere önizlemesi: başlık çubuğu + uygulamaya özgü içerik blokları."""
    _, _, bg = APPS[app]
    light = bg in ("#fef3c7", "#e8f5ec", "#f8fafc", "#eef4fb", "#f3f7fb", "#e5e7eb")
    ink = "rgba(0,0,0,.14)" if light else "rgba(255,255,255,.14)"
    ink2 = "rgba(0,0,0,.28)" if light else "rgba(255,255,255,.3)"
    bar = "#d1d5db" if light else "#2b2b3a"
    body = ""
    if app in ("Tarayıcı", "Posta", "Mesajlar"):
        body = (f'<div style="height:{h*.16}px;margin:6px;border-radius:6px;background:{ink2}"></div>'
                + "".join(f'<div style="height:{h*.07}px;margin:5px 6px;width:{88 - (i*13+variant*7)%40}%;border-radius:3px;background:{ink}"></div>' for i in range(5)))
    elif app in ("Terminal", "Kod"):
        cols = ["#4ade80", "#60a5fa", "#f472b6", "#facc15"]
        body = "".join(f'<div style="height:{max(3,h*.05)}px;margin:5px 8px;width:{30+(i*17+variant*11)%60}%;border-radius:2px;background:{cols[(i+variant)%4]};opacity:.75"></div>' for i in range(8))
    elif app in ("Fotoğraflar", "Tasarım"):
        tiles = ["#fb923c", "#f472b6", "#a78bfa", "#38bdf8", "#34d399", "#facc15"]
        body = ('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:6px">'
                + "".join(f'<div style="aspect-ratio:1.3;border-radius:4px;background:{tiles[(i+variant)%6]};opacity:.8"></div>' for i in range(6)) + "</div>")
    elif app == "Takvim":
        body = ('<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:3px;padding:6px">'
                + "".join(f'<div style="height:{h*.1}px;border-radius:2px;background:{"#818cf8" if i in (9,17,23) else ink}"></div>' for i in range(28)) + "</div>")
    elif app == "Müzik":
        body = ('<div style="display:flex;gap:8px;padding:8px"><div style="width:40%;aspect-ratio:1;border-radius:6px;background:linear-gradient(135deg,#fb7185,#7c3aed)"></div><div style="flex:1">'
                + "".join(f'<div style="height:{h*.06}px;margin:5px 0;width:{90-i*12}%;border-radius:2px;background:{ink2}"></div>' for i in range(5)) + "</div></div>")
    else:
        body = "".join(f'<div style="height:{h*.08}px;margin:6px 8px;width:{80-(i*9)%30}%;border-radius:3px;background:{ink}"></div>' for i in range(5))
    return (f'<div style="width:{w}px;height:{h}px;border-radius:9px;overflow:hidden;background:{bg};box-shadow:0 6px 18px rgba(0,0,0,.35)">'
            f'<div style="height:14px;background:{bar};display:flex;gap:4px;align-items:center;padding-left:6px">'
            '<i style="width:6px;height:6px;border-radius:50%;background:#f87171;display:block"></i>'
            '<i style="width:6px;height:6px;border-radius:50%;background:#fbbf24;display:block"></i>'
            '<i style="width:6px;height:6px;border-radius:50%;background:#34d399;display:block"></i></div>'
            f'{body}</div>')

LOGO = ('<svg width="18" height="18" viewBox="210 260 580 480"><path fill="rgba(255,255,255,.45)" d="M282,260 H638 A72,72 0 0 1 710,332 V578 A72,72 0 0 1 638,650 H282 A72,72 0 0 1 210,578 V332 A72,72 0 0 1 282,260 Z"/>'
        '<path fill="#fff" fill-rule="evenodd" d="M362,350 H718 A72,72 0 0 1 790,422 V668 A72,72 0 0 1 718,740 H362 A72,72 0 0 1 290,668 V422 A72,72 0 0 1 362,350 Z '
        'M442,475 h0 a32,32 0 0 1 32,32 v76 a32,32 0 0 1 -64,0 v-76 a32,32 0 0 1 32,-32 Z M540,420 a32,32 0 0 1 32,32 v186 a32,32 0 0 1 -64,0 v-186 a32,32 0 0 1 32,-32 Z M638,455 a32,32 0 0 1 32,32 v116 a32,32 0 0 1 -64,0 v-116 a32,32 0 0 1 32,-32 Z"/></svg>')

def menubar(extra=""):
    return f'<div class="menubar">{extra}<span>{LOGO}</span><span>Cmt 31 Eki 16:40</span></div>'

def page(name, w, h, inner):
    doc = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head>'
           f'<body><div class="frame" style="width:{w}px;height:{h}px">{inner}</div></body></html>')
    with open(os.path.join(OUT, f"{name}.html"), "w") as f:
        f.write(translate(doc))
    print(f"{name} {w} {h}")

def esc(s): return html.escape(s)

def win_btns():
    return '<div class="btns"><i style="background:#ef4444"></i><i style="background:rgba(255,255,255,.35)"></i></div>'

# --- Sahneler -------------------------------------------------------------------------------

def preview_card(app, title, w, h, sel=False, variant=0, badge=None, audio=False):
    b = ""
    if badge:
        b += f'<span class="badge" style="left:14px;top:14px;background:#22c55e;color:#04210f">{esc(badge)}</span>'
    if audio:
        b += ('<span class="badge" style="left:14px;bottom:44px;background:rgba(0,0,0,.6);color:#fff">'
              '<svg width="10" height="10" viewBox="0 0 24 24" style="vertical-align:-1px"><path d="M4 14v-2a8 8 0 0116 0v2" fill="none" stroke="#fff" stroke-width="2.6"/><rect x="3" y="13" width="5" height="8" rx="2" fill="#fff"/><rect x="16" y="13" width="5" height="8" rx="2" fill="#fff"/></svg> Kulaklık</span>')
    return (f'<div class="card{" sel" if sel else ""}" style="width:{w+20}px">{win_btns() if sel else ""}{thumb(app, w, h, variant)}{b}'
            f'<div class="row" style="gap:6px;margin-top:8px;max-width:{w}px">{icon(app, 18)}<div class="title" style="margin:0">{esc(title)}</div></div></div>')

def scene_hero():
    cards = [("Tarayıcı", "Proje panosu — Tarayıcı", 0, "İş", False), ("Kod", "main.swift — Kod", 0, None, False),
             ("Müzik", "Çalma listesi", 0, None, True), ("Notlar", "Toplantı notları", 0, None, False),
             ("Terminal", "~/projeler — zsh", 1, None, False), ("Takvim", "Ekim 2026", 0, None, False),
             ("Fotoğraflar", "Tatil albümü", 0, None, False), ("Mesajlar", "Ekip sohbeti", 0, None, False)]
    rows = ""
    for r in range(2):
        rows += '<div class="row" style="gap:14px;justify-content:center;margin:7px 0">'
        for i, (a, t, v, b, au) in enumerate(cards[r*4:(r+1)*4]):
            rows += preview_card(a, t, 210, 132, sel=(r == 0 and i == 1), variant=v, badge=b, audio=au)
        rows += "</div>"
    inner = menubar() + f'<div class="glass center" style="padding:18px 20px;top:53%">{rows}</div>'
    page("hero", 1200, 620, inner)

def scene_cmd_tab():
    apps = [("Tarayıcı", "Proje panosu", "İş"), ("Kod", "main.swift", None), ("Notlar", "Toplantı notları", None),
            ("Müzik", "Çalma listesi", None), ("Terminal", "zsh", None), ("Posta", "Gelen kutusu", None),
            ("Takvim", "Ekim 2026", None), ("Mesajlar", "Ekip sohbeti", None), ("Tasarım", "Logo taslağı", None),
            ("Klasör", "İndirilenler", None)]
    cells = ""
    for i, (a, t, b) in enumerate(apps):
        sel = i == 1
        bd = f'<span class="badge" style="right:8px;top:8px;background:#22c55e;color:#04210f">{b}</span>' if b else ""
        au = ('<span class="badge" style="left:8px;top:8px;background:rgba(0,0,0,.55)">🎧</span>' if a == "Müzik" else "")
        cells += (f'<div class="card{" sel" if sel else ""}" style="width:132px;height:136px;justify-content:center">{win_btns() if sel else ""}{bd}{au}'
                  f'{icon(a, 64)}<div class="title">{esc(t)}</div><div class="sub">{a}</div></div>')
    inner = (menubar() + f'<div class="glass center" style="padding:20px;display:grid;grid-template-columns:repeat(5,132px);gap:12px;top:50%">{cells}</div>'
             '<div class="hint" style="position:absolute;bottom:22px;left:0;right:0">⌘ basılı · Tab sonraki · ⇧Tab önceki · bırakınca o pencereye geçer</div>')
    page("cmd-tab", 1200, 520, inner)

def scene_opt_tab_scroll():
    apps = ["Tarayıcı", "Kod", "Notlar", "Terminal", "Takvim", "Fotoğraflar", "Mesajlar", "Müzik", "Posta", "Tasarım", "Tarayıcı", "Kod"]
    titles = ["Dokümantasyon", "Switcher.swift", "Alışveriş", "~/build", "Hafta", "Albüm", "Aile", "Radyo", "Bülten", "Afiş", "Haberler", "README.md"]
    rows = ""
    for r in range(3):
        rows += '<div class="row" style="gap:12px;justify-content:center;margin:6px 0">'
        for i in range(4):
            k = r*4+i
            rows += preview_card(apps[k], titles[k], 176, 108, sel=(k == 10), variant=k % 3)
        rows += "</div>"
    inner = (menubar() +
             f'<div class="glass center" style="padding:24px 20px 30px;top:52%">'
             '<div class="hint" style="margin:-12px 0 6px">↑ 4 pencere daha</div>'
             f'{rows}<div class="hint" style="margin-top:8px">↓ 6 pencere daha</div></div>')
    page("opt-tab-scroll", 1200, 640, inner)

def scene_grouped():
    groups = [("Tarayıcılar", [("Tarayıcı", "Proje panosu"), ("Tarayıcı", "Haberler")]),
              ("Projeler", [("Kod", "audiotab"), ("Tasarım", "Logo")]),
              ("Geliştirme", [("Terminal", "zsh"), ("Kod", "server.ts")]),
              ("Uygulamalar", [("Müzik", "Radyo"), ("Mesajlar", "Ekip"), ]),
              ("Klasörler", [("Klasör", "İndirilenler"), ("Klasör", "Belgeler")])]
    cols = ""
    for gi, (name, items) in enumerate(groups):
        sep = "border-left:1px solid rgba(255,255,255,.12);padding-left:16px;" if gi else ""
        cards = "".join(preview_card(a, t, 150, 92, sel=(gi == 2 and j == 0), variant=j) for j, (a, t) in enumerate(items))
        cols += f'<div style="{sep}display:flex;flex-direction:column;gap:10px"><div class="sec">{name}</div>{cards}</div>'
    inner = menubar() + f'<div class="glass center" style="padding:20px;display:flex;gap:16px;top:52%">{cols}</div>'
    page("grouped", 1200, 560, inner)

def scene_filter_sidebar():
    chips = "".join(f'<span class="pill{" on" if i == 1 else ""}">{t}</span>' for i, t in enumerate(["Tümü", "Tarayıcı", "Kod", "Notlar", "Terminal"]))
    cards = "".join(preview_card("Tarayıcı", t, 170, 104, sel=(i == 0), variant=i) for i, t in enumerate(["Proje panosu", "Haberler", "Dokümantasyon", "Alışveriş"]))
    fav = "".join(f'<div class="row" style="gap:8px;padding:6px 8px;border-radius:8px;{"background:rgba(255,255,255,.08);" if i == 0 else ""}">{icon("Klasör", 20)}<span style="font-size:13px">{t}</span></div>'
                  for i, t in enumerate(["Masaüstü", "İndirilenler", "Belgeler", "Projeler", "Fotoğraflar"]))
    inner = (menubar() + '<div class="glass center" style="padding:18px;display:flex;gap:18px;top:52%">'
             f'<div><div class="row" style="gap:8px;margin-bottom:12px">{chips}</div>'
             f'<div style="display:grid;grid-template-columns:repeat(2,auto);gap:12px">{cards}</div></div>'
             f'<div style="width:190px;border-left:1px solid rgba(255,255,255,.12);padding-left:14px"><div class="sec" style="margin-bottom:8px">Favoriler</div>{fav}</div></div>'
             '<div class="hint" style="position:absolute;bottom:20px;left:0;right:0">F: yalnızca seçili uygulamanın pencereleri · A: filtreyi değiştir · kenar çubuğundan klasöre tek tık</div>')
    page("filter-sidebar", 1200, 600, inner)

def scene_keys():
    keys = [("Tab", "sonraki"), ("⇧ Tab", "önceki"), ("← → ↑ ↓", "gezin"), ("↩", "geç"), ("W", "pencereyi kapat"), ("M", "küçült"),
            ("H", "gizle"), ("Q", "uygulamadan çık"), ("S", "ses cihazını değiştir"), ("F", "sadece bu uygulama"), ("A", "filtreyi değiştir"), ("Esc", "vazgeç")]
    cells = "".join(f'<div class="row" style="gap:14px;padding:10px 14px;border-radius:12px;background:rgba(255,255,255,.05)"><span class="kbd">{k}</span><span style="font-size:15px">{t}</span></div>' for k, t in keys)
    inner = ('<div class="glass center" style="padding:26px;width:900px"><div class="sec" style="margin-bottom:16px">Panel açıkken</div>'
             f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">{cells}</div></div>')
    page("panel-keys", 1200, 440, inner)

def device_row(name, kind, on=False):
    ic = {"hp": '<path d="M4 14v-2a8 8 0 0116 0v2" fill="none" stroke="#fff" stroke-width="2.4"/><rect x="3" y="13" width="5" height="8" rx="2" fill="#fff"/><rect x="16" y="13" width="5" height="8" rx="2" fill="#fff"/>',
          "sp": '<rect x="6" y="3" width="12" height="18" rx="3" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="12" cy="14" r="3" fill="#fff"/><circle cx="12" cy="7.5" r="1.4" fill="#fff"/>',
          "mon": '<rect x="3" y="4" width="18" height="12" rx="2" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M9 20h6M12 16v4" stroke="#fff" stroke-width="2.2"/>',
          "lap": '<rect x="5" y="5" width="14" height="10" rx="1.5" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M3 18h18" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'}[kind]
    st = "background:#6366f1;" if on else "background:rgba(255,255,255,.06);"
    ck = '<span style="margin-left:auto;font-weight:700">✓</span>' if on else ""
    return (f'<div class="row" style="{st}padding:12px 16px;border-radius:12px;font-size:15px;font-weight:600">'
            f'<svg width="22" height="22" viewBox="0 0 24 24">{ic}</svg>{name}{ck}</div>')

def scene_audio():
    hud = ('<div class="glass" style="position:absolute;left:90px;top:120px;width:420px;padding:26px;text-align:center">'
           '<svg width="74" height="74" viewBox="0 0 24 24"><path d="M4 14v-2a8 8 0 0116 0v2" fill="none" stroke="#fff" stroke-width="2"/><rect x="3" y="13" width="5" height="8" rx="2" fill="#fff"/><rect x="16" y="13" width="5" height="8" rx="2" fill="#fff"/></svg>'
           '<div style="font-size:22px;font-weight:700;margin-top:10px">Kablosuz Kulaklık</div><div class="sub" style="margin-top:4px">Ses çıkışı değişti</div>'
           '<div class="row" style="justify-content:center;gap:8px;margin-top:22px"><span class="kbd">⌘</span><span style="opacity:.6">basılıyken</span><span class="kbd">⇧</span></div></div>')
    lst = ('<div class="glass" style="position:absolute;right:90px;top:90px;width:440px;padding:18px"><div class="sec" style="margin:2px 4px 12px">Ses cihazları · sırayla</div>'
           + device_row("MacBook Hoparlörleri", "lap") + '<div style="height:8px"></div>'
           + device_row("Kablosuz Kulaklık", "hp", True) + '<div style="height:8px"></div>'
           + device_row("Masaüstü Hoparlör", "sp") + '<div style="height:8px"></div>'
           + device_row("Harici Monitör", "mon")
           + '<div class="hint" style="margin-top:14px;text-align:left">Çıkarılan kulaklığı hatırlar, takınca geri döner</div></div>')
    page("audio-switch", 1200, 520, menubar() + hud + lst)

def scene_per_app_audio():
    rows = [("Müzik", "Masaüstü Hoparlör", "sp"), ("Mesajlar", "Kablosuz Kulaklık", "hp"), ("Tarayıcı", "Kablosuz Kulaklık", "hp"), ("Kod", "MacBook Hoparlörleri", "lap")]
    body = "".join(f'<div class="row" style="padding:12px 4px;border-bottom:1px solid rgba(255,255,255,.08)">{icon(a, 34)}<span style="font-size:15px;font-weight:600;width:150px">{a}</span>'
                   f'<span style="opacity:.5">→</span><span class="pill" style="font-size:13px">{d}</span></div>' for a, d, _ in rows)
    left = (f'<div class="glass" style="position:absolute;left:80px;top:90px;width:560px;padding:22px"><div class="sec" style="margin-bottom:8px">Uygulamaya göre ses cihazı</div>{body}'
            '<div class="hint" style="text-align:left;margin-top:14px">Uygulama öne gelince ses kendiliğinden o cihaza geçer</div></div>')
    card = preview_card("Müzik", "Çalma listesi", 230, 144, sel=True, audio=True)
    right = (f'<div class="glass" style="position:absolute;right:110px;top:110px;padding:22px;text-align:center">{card}'
             '<div class="row" style="justify-content:center;gap:8px;margin-top:16px"><span class="kbd">S</span><span style="font-size:14px">⌘Tab panelinde ses cihazını değiştir</span></div></div>')
    page("per-app-audio", 1200, 520, menubar() + left + right)

LAYOUTS = [("Tam ekran", [(0, 0, 1, 1)]), ("2 dikey", [(0, 0, .5, 1), (.5, 0, .5, 1)]), ("2 yatay", [(0, 0, 1, .5), (0, .5, 1, .5)]),
           ("3 dikey", [(0, 0, 1/3, 1), (1/3, 0, 1/3, 1), (2/3, 0, 1/3, 1)]), ("⅓ + ⅔", [(0, 0, 1/3, 1), (1/3, 0, 2/3, 1)]),
           ("⅔ + ⅓", [(0, 0, 2/3, 1), (2/3, 0, 1/3, 1)]), ("½ + ¼ ¼", [(0, 0, .5, 1), (.5, 0, .5, .5), (.5, .5, .5, .5)]),
           ("4 (2×2)", [(0, 0, .5, .5), (.5, 0, .5, .5), (0, .5, .5, .5), (.5, .5, .5, .5)]),
           ("6 (3×2)", [(x/3, y/2, 1/3, .5) for y in range(2) for x in range(3)])]

def layout_tile(name, zones, w=150, h=90, sel=False):
    z = "".join(f'<div style="position:absolute;left:{x*w+2}px;top:{y*h+2}px;width:{zw*w-4}px;height:{zh*h-4}px;border-radius:5px;'
                f'background:{"rgba(99,102,241,.6)" if sel and i == 0 else "rgba(255,255,255,.16)"};border:1px solid {"#a5b4fc" if sel and i == 0 else "rgba(255,255,255,.28)"}"></div>'
                for i, (x, y, zw, zh) in enumerate(zones))
    return (f'<div class="card{" sel" if sel else ""}" style="width:{w+24}px;padding:12px"><div style="position:relative;width:{w}px;height:{h}px">{z}</div>'
            f'<div class="title">{esc(name)}</div></div>')

def scene_tiling():
    tiles = "".join(layout_tile(n, z, sel=(i == 1)) for i, (n, z) in enumerate(LAYOUTS))
    head = (f'<div class="row" style="margin-bottom:14px">{icon("Tarayıcı", 40)}<div><div style="font-size:17px;font-weight:700">Tarayıcı</div><div class="sub">Ekranın hangi bölmesine?</div></div>'
            '<div class="row" style="margin-left:auto;gap:8px"><span class="pill">1 · Dahili ekran · buradasın</span><span class="pill on">2 · Harici monitör</span></div></div>')
    picker = (f'<div class="glass" style="position:absolute;left:60px;top:70px;padding:20px">{head}'
              f'<div style="display:grid;grid-template-columns:repeat(3,auto);gap:10px">{tiles}</div>'
              '<div class="hint" style="margin-top:12px">1–9 düzen seç · ↩ seç · Tab monitör değiştir · Esc kapat</div></div>')
    badge = ('<div class="glass" style="position:absolute;right:70px;top:60px;width:200px;padding:16px;text-align:center;border:3px solid #6366f1">'
             '<div style="font-size:64px;font-weight:800;line-height:1">2</div><div style="font-weight:600;margin-top:6px">Harici monitör</div>'
             '<div style="color:#a5b4fc;font-size:12px;font-weight:600;margin-top:2px">Hedef monitör</div></div>')
    result = ('<div style="position:absolute;right:60px;bottom:60px;width:340px;height:210px;border-radius:12px;background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.15);padding:8px;display:flex;gap:8px">'
              f'<div style="flex:1">{thumb("Tarayıcı", 158, 192)}</div><div style="flex:1">{thumb("Kod", 158, 192, 1)}</div></div>'
              '<div class="hint" style="position:absolute;right:60px;bottom:30px;width:340px">Sonuç: 2 dikey bölme</div>')
    head_keys = '<div class="row" style="position:absolute;right:120px;top:300px;gap:8px"><span class="kbd">⌘</span><span class="kbd">&lt;</span></div>'
    page("tiling", 1200, 680, menubar() + picker + badge + head_keys + result)

def scene_capture():
    sel = ('<div style="position:absolute;left:300px;top:110px;width:520px;height:300px;border:2px dashed #fff;border-radius:6px;box-shadow:0 0 0 2000px rgba(0,0,0,.45)">'
           f'<div style="position:absolute;inset:8px">{thumb("Tarayıcı", 500, 280)}</div>'
           '<span class="pill" style="position:absolute;right:-2px;bottom:-34px;background:rgba(0,0,0,.7)">1040 × 600</span></div>')
    opts = [("⌘⇧3", "Bulunduğun ekran"), ("⌘⇧4", "Alan"), ("⌘⇧6", "Kaydırmalı"), ("⌘⇧5", "Kayıt")]
    tools = "".join(f'<div style="text-align:center;padding:8px 14px;border-radius:10px;{"background:#6366f1;" if i == 1 else ""}"><div style="font-size:14px;font-weight:700;white-space:nowrap">{t}</div><div class="sub" style="color:rgba(255,255,255,.7)">{k}</div></div>' for i, (k, t) in enumerate(opts))
    fmts = "".join(f'<span class="pill{" on" if i == 0 else ""}">{f}</span>' for i, f in enumerate(["MP4 · H.264", "H.265", "ProRes 4444"]))
    bar = (f'<div class="glass" style="position:absolute;left:50%;transform:translateX(-50%);bottom:40px;padding:10px 14px;display:flex;align-items:center;gap:6px">{tools}'
           f'<div style="width:1px;height:40px;background:rgba(255,255,255,.15);margin:0 8px"></div><div class="row" style="gap:6px">{fmts}</div>'
           '<div style="width:1px;height:40px;background:rgba(255,255,255,.15);margin:0 8px"></div><span style="width:22px;height:22px;flex:0 0 22px;border-radius:50%;background:#ef4444;display:block;box-shadow:0 0 0 4px rgba(239,68,68,.3)"></span></div>')
    page("capture", 1200, 600, menubar() + sel + bar)

def scene_scrolling():
    view = ('<div style="position:absolute;left:110px;top:90px">'
            f'<div style="position:relative;border-radius:10px;border:2px solid #818cf8;padding:6px;background:rgba(0,0,0,.25)">{thumb("Tarayıcı", 380, 260)}</div>'
            '<div style="position:absolute;right:-46px;top:40px;height:200px;display:flex;flex-direction:column;align-items:center;gap:6px;color:#a5b4fc;font-size:26px">⇣<div style="width:3px;flex:1;background:linear-gradient(#818cf8,transparent);border-radius:2px"></div></div>'
            '<div class="hint" style="margin-top:12px">Sen kaydırırsın, AudioTab yakalar</div></div>')
    arrow = '<div style="position:absolute;left:600px;top:230px;font-size:44px;color:rgba(255,255,255,.6)">→</div>'
    blocks = "".join(f'<div style="height:{36 if i % 4 == 0 else 12}px;margin:{14 if i % 4 == 0 else 7}px 10px 0;width:{92 if i % 4 == 0 else 85 - (i*13) % 35}%;border-radius:{8 if i % 4 == 0 else 3}px;background:rgba(255,255,255,{.3 if i % 4 == 0 else .14})"></div>' for i in range(22))
    long = (f'<div style="width:300px;height:494px;border-radius:9px;overflow:hidden;background:#1e3a8a;box-shadow:0 6px 18px rgba(0,0,0,.35)">'
            f'<div style="height:14px;background:#2b2b3a"></div>{blocks}</div>')
    out = (f'<div class="glass" style="position:absolute;right:120px;top:50px;padding:12px;height:520px;overflow:hidden">{long}</div>'
           '<div class="hint" style="position:absolute;right:120px;bottom:24px;width:324px">Tek parça uzun ekran görüntüsü · ⌘⇧6</div>')
    page("scrolling", 1200, 620, menubar() + view + arrow + out)

def monitor(w, h, inner, label, dark=False):
    return (f'<div style="text-align:center"><div style="width:{w}px;height:{h}px;border-radius:10px;border:6px solid #1f1d2e;'
            f'background:{"#000" if dark else "rgba(255,255,255,.08)"};position:relative;overflow:hidden">{inner}</div>'
            f'<div style="width:{w*.18}px;height:24px;margin:0 auto;background:#1f1d2e"></div><div style="width:{w*.4}px;height:6px;margin:0 auto;border-radius:3px;background:#1f1d2e"></div>'
            f'<div class="sub" style="margin-top:10px">{label}</div></div>')

def slider(label, val, glyph):
    return (f'<div class="row" style="gap:10px;margin:8px 0"><span style="width:20px;text-align:center">{glyph}</span>'
            f'<div style="flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.15);position:relative"><div style="width:{val}%;height:100%;border-radius:4px;background:#fff"></div></div>'
            f'<span style="font-size:12px;width:34px;text-align:right">{val}%</span></div>')

def scene_displays():
    hud = (f'<div class="glass" style="position:absolute;inset:auto 30px 30px 30px;padding:14px 16px"><div style="font-size:13px;font-weight:700;margin-bottom:4px">Harici monitör · DDC/CI</div>'
           f'{slider("Parlaklık", 70, "☀︎")}{slider("Ses", 40, "🔈")}</div>')
    m1 = monitor(460, 280, f'<div style="position:absolute;inset:16px;display:flex;gap:10px">{thumb("Kod", 200, 150)}{thumb("Terminal", 200, 150, 1)}</div>{hud}', "Monitör 1 · DDC/CI ile parlaklık ve ses, menü çubuğundan")
    m2 = monitor(400, 280, '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:12px;color:rgba(255,255,255,.35)">'
                 '<div class="row" style="gap:8px"><span class="kbd" style="opacity:.6">⌘</span><span class="kbd" style="opacity:.6">⇧</span><span class="kbd" style="opacity:.6">&lt;</span></div>'
                 '<div style="font-size:13px">tamamen karartıldı</div></div>', "Monitör 2 · ⌘⇧< ile tam karartma", dark=True)
    page("displays", 1200, 520, f'<div class="row center" style="gap:60px;top:52%">{m1}{m2}</div>')

def scene_finder_dock():
    mouse = ('<svg width="120" height="170" viewBox="0 0 120 170"><rect x="10" y="10" width="100" height="150" rx="50" fill="#e5e7eb"/>'
             '<path d="M60 10v58" stroke="#9ca3af" stroke-width="2"/><rect x="2" y="70" width="14" height="26" rx="6" fill="#6366f1"/><rect x="2" y="100" width="14" height="26" rx="6" fill="#6366f1"/></svg>')
    left = (f'<div class="glass" style="position:absolute;left:70px;top:80px;width:500px;height:390px;padding:24px">'
            '<div class="sec">FINDER</div><div class="row" style="gap:24px;margin-top:18px">'
            f'{mouse}<div><div class="row" style="gap:10px"><span class="kbd">‹ Geri</span><span class="kbd">İleri ›</span></div>'
            '<div class="hint" style="text-align:left;margin-top:14px;max-width:220px">Farenin yan tuşları Finder klasörlerinde geri ve ileri gider</div></div></div>'
            '<div style="margin-top:22px;border-radius:10px;overflow:hidden;background:#eef2f7;color:#334155">'
            '<div class="row" style="gap:8px;padding:8px 10px;background:#dfe5ee;font-size:13px;font-weight:600"><span style="background:#6366f1;color:#fff;border-radius:6px;padding:1px 8px">‹</span><span style="opacity:.5">›</span><span>Projeler › audiotab</span></div>'
            '<div class="row" style="gap:22px;padding:12px 14px">' + "".join(f'<div style="text-align:center;font-size:11px">{icon("Klasör", 36)}<div style="margin-top:4px">{n}</div></div>' for n in ["Sources", "docs", "tools", "Icon"]) + '</div></div></div>')
    dock_icons = "".join(f'<div style="{"transform:translateY(-14px) scale(1.25);" if a == "Tasarım" else ""}">{icon(a, 52)}</div>' for a in ["Klasör", "Tarayıcı", "Posta", "Tasarım", "Notlar", "Müzik"])
    file_ = ('<div style="position:absolute;left:250px;top:150px;transform:rotate(-8deg)"><div style="width:58px;height:72px;border-radius:6px;background:#fff;box-shadow:0 10px 24px rgba(0,0,0,.4)">'
             '<div style="height:14px;background:#a78bfa;border-radius:6px 6px 0 0"></div></div><div class="sub" style="margin-top:6px;color:#fff">afiş.png</div></div>')
    right = (f'<div class="glass" style="position:absolute;right:70px;top:80px;width:520px;height:390px;padding:24px">'
             f'<div class="sec">Dock\'a sürükle-bırak</div>{file_}'
             '<div style="position:absolute;left:300px;top:240px;font-size:30px;color:rgba(255,255,255,.7)">↘</div>'
             f'<div class="row" style="position:absolute;left:28px;right:28px;bottom:28px;justify-content:center;gap:12px;padding:10px;border-radius:18px;background:rgba(255,255,255,.1)">{dock_icons}</div>'
             '<div class="hint" style="position:absolute;left:24px;right:24px;top:70px;text-align:left">Dosyayı Dock\'taki uygulamanın üstüne getir: beklemeden öne gelir, dosyayı doğrudan penceresine bırakırsın</div></div>')
    page("finder-dock", 1200, 560, left + right)

def scene_secure():
    hud = ('<div class="glass center" style="padding:22px 30px;display:flex;align-items:center;gap:18px;top:45%">'
           '<svg width="44" height="44" viewBox="0 0 24 24"><rect x="5" y="10" width="14" height="11" rx="2.5" fill="#fff"/><path d="M8 10V7.5a4 4 0 018 0V10" fill="none" stroke="#fff" stroke-width="2.4"/></svg>'
           '<div><div style="font-size:18px;font-weight:700">Tarayıcı klavyeyi kilitledi</div><div class="sub" style="font-size:13px;margin-top:3px">⌘Tab şimdilik macOS\'unki · kilit kalkınca AudioTab devralır</div></div></div>'
           '<div class="hint center" style="top:72%">Parola alanları ve "güvenli klavye girişi" tuşları her uygulamadan gizler; AudioTab bunu fark eder</div>')
    page("secure-input", 1200, 380, menubar() + hud)

def scene_settings():
    tabs = "".join(f'<span class="pill{" on" if i == 3 else ""}" style="font-size:13px;padding:7px 14px">{t}</span>' for i, t in enumerate(["Ses", "Pencereler", "Ekran", "İzinler", "Genel", "Sürümler"]))
    perm = lambda t, d: (f'<div class="row" style="padding:12px 0;border-top:1px solid rgba(255,255,255,.08)"><div style="flex:1"><div style="font-weight:600">{t}</div><div class="sub" style="white-space:normal">{d}</div></div>'
                         '<span style="color:#4ade80;font-weight:700;font-size:13px">● Verildi</span></div>')
    body = ('<div class="glass" style="padding:16px 18px;border-radius:16px;margin-top:16px"><div class="row" style="gap:10px"><span style="color:#4ade80;font-size:20px">✓</span>'
            '<div><div style="font-weight:700">Her şey hazır</div><div class="sub">Kısayollar çalışıyor</div></div></div></div>'
            '<div class="glass" style="padding:6px 18px 4px;border-radius:16px;margin-top:12px"><div class="sec" style="margin:10px 0 6px">Gerekli izinler</div>'
            + perm("Erişilebilirlik", "⌘Tab, ⌥Tab ve ses kısayolu için; pencereleri kapatmak ve küçültmek için")
            + perm("Ekran Kaydı", "Pencere önizlemeleri, ekran görüntüsü ve kayıt için") + "</div>"
            '<div class="glass" style="padding:14px 18px;border-radius:16px;margin-top:12px"><div class="sub" style="white-space:normal">Basılan tuşlar kaydedilmez, saklanmaz. Yalnızca güncelleme kontrolü için GitHub\'a bağlanır.</div></div>')
    win = (f'<div class="glass center" style="width:640px;padding:16px 22px 22px;border-radius:18px">'
           '<div class="row" style="gap:7px;margin-bottom:14px"><i style="width:12px;height:12px;border-radius:50%;background:#f87171;display:block"></i><i style="width:12px;height:12px;border-radius:50%;background:#fbbf24;display:block"></i><i style="width:12px;height:12px;border-radius:50%;background:#34d399;display:block"></i></div>'
           f'<div class="row" style="gap:6px;justify-content:center;padding:6px;border-radius:14px;background:rgba(255,255,255,.06)">{tabs}</div>{body}</div>')
    page("settings", 1200, 660, menubar() + win)

def scene_updates():
    chain = "".join(f'<div class="row" style="gap:10px;padding:7px 0"><span style="color:#4ade80;font-weight:800">✓</span><span style="font-size:14px">{t}</span></div>'
                    for t in ["Apple Developer ID ile imzalı", "Aynı Team ID", "Apple tarafından notarize edilmiş", "Sertifika iptal edilmemiş", "Yalnızca GitHub · HTTPS (TLS 1.2+)"])
    pop = ('<div class="glass" style="position:absolute;right:70px;top:44px;width:430px;padding:22px">'
           '<div class="row"><div style="font-size:18px;font-weight:700">Yeni sürüm: 2.6.0</div><span class="pill" style="margin-left:auto">2.5.2 → 2.6.0</span></div>'
           f'<div style="margin-top:12px">{chain}</div>'
           '<div class="row" style="margin-top:16px;gap:10px"><span class="pill on" style="padding:9px 16px;font-size:13px">Güncelle ve yeniden başlat</span><span class="pill" style="padding:9px 16px;font-size:13px">Sonra</span></div></div>')
    gk = ('<div class="glass" style="position:absolute;left:70px;top:80px;width:520px;padding:24px">'
          '<div class="sec">İndir · aç · çalıştır</div><div class="row" style="gap:18px;margin-top:18px">'
          '<svg width="86" height="86" viewBox="0 0 24 24"><path d="M12 2l8 3v6c0 5-3.4 9.3-8 11-4.6-1.7-8-6-8-11V5z" fill="#22c55e"/><path d="M8 12l3 3 5-6" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
          '<div><div style="font-size:18px;font-weight:700">"Apple could not verify…" yok</div><div class="sub" style="white-space:normal;margin-top:6px;font-size:13px">Notarize edilmiş ve bileti zımbalanmış uygulama Gatekeeper\'dan uyarısız geçer. Karantina bayrağına dokunulmaz.</div></div></div></div>')
    page("trusted-updates", 1200, 440, menubar() + gk + pop)

for fn in [scene_hero, scene_cmd_tab, scene_opt_tab_scroll, scene_grouped, scene_filter_sidebar, scene_keys, scene_audio,
           scene_per_app_audio, scene_tiling, scene_capture, scene_scrolling, scene_displays, scene_finder_dock,
           scene_secure, scene_settings, scene_updates]:
    fn()
