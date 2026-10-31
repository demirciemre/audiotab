import Cocoa

// MARK: - Menü çubuğu simgesi
//
// Uygulama simgesinin (Icon/AppIcon.icon) tek renkli hali: arkada soluk bir pencere kartı,
// önde içine ses dalgası oyulmuş kart. Şablon görüntü olduğu için açık/koyu menü çubuğuna
// ve vurgulanma durumuna macOS kendisi uyar. Ölçüler 1024'lük simge tuvalinden alınır.

enum StatusIcon {
    static let image: NSImage = {
        let side: CGFloat = 18
        let img = NSImage(size: NSSize(width: side, height: side), flipped: false) { _ in
            // Simgedeki çizimin sınırları (tuval birimi): x 210…790, y 260…740
            let k: CGFloat = 17 / 580
            let ox = (side - 580 * k) / 2, oy = (side - 480 * k) / 2
            func rect(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat) -> NSRect {
                NSRect(x: ox + (x - 210) * k, y: oy + (740 - y - h) * k, width: w * k, height: h * k)
            }
            let r = 72 * k
            guard let ctx = NSGraphicsContext.current?.cgContext else { return false }

            // Arka kart (soluk)
            NSColor.black.withAlphaComponent(0.45).setFill()
            NSBezierPath(roundedRect: rect(210, 260, 500, 390), xRadius: r, yRadius: r).fill()

            // Ön kartın çevresinde ince boşluk: iki kart birbirinden ayrılsın
            let front = rect(290, 350, 500, 390)
            ctx.setBlendMode(.clear)
            NSBezierPath(roundedRect: front.insetBy(dx: -1.2, dy: -1.2), xRadius: r + 1.2, yRadius: r + 1.2).fill()
            ctx.setBlendMode(.normal)

            // Ön kart, içinden üç ses çubuğu oyulmuş
            let path = NSBezierPath(roundedRect: front, xRadius: r, yRadius: r)
            let bw: CGFloat = 64, gap: CGFloat = 34
            let x0: CGFloat = 290 + (500 - (3 * bw + 2 * gap)) / 2, mid: CGFloat = 350 + 390 / 2
            for (i, h) in [CGFloat(140), 250, 180].enumerated() {
                let bar = rect(x0 + CGFloat(i) * (bw + gap), mid - h / 2, bw, h)
                path.append(NSBezierPath(roundedRect: bar, xRadius: bar.width / 2, yRadius: bar.width / 2))
            }
            path.windingRule = .evenOdd
            NSColor.black.setFill()
            path.fill()
            return true
        }
        img.isTemplate = true
        img.accessibilityDescription = "AudioTab"
        return img
    }()
}
