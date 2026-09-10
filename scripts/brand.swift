import AppKit

let output = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
for (name, size) in [("logo", 512), ("icon", 128)] {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    let transform = NSAffineTransform()
    transform.scale(by: CGFloat(size) / 512)
    transform.concat()
    let background = NSBezierPath(roundedRect: NSRect(x: 12, y: 12, width: 488, height: 488), xRadius: 112, yRadius: 112)
    NSGradient(starting: NSColor(srgbRed: 0.21, green: 0.13, blue: 0.49, alpha: 1),
               ending: NSColor(srgbRed: 0.49, green: 0.31, blue: 0.87, alpha: 1))!.draw(in: background, angle: 65)
    NSColor.white.setStroke()
    NSColor.white.setFill()
    for x in [168, 258] {
        NSBezierPath(roundedRect: NSRect(x: x, y: 303, width: 24, height: 83), xRadius: 12, yRadius: 12).fill()
    }
    NSBezierPath(roundedRect: NSRect(x: 128, y: 185, width: 196, height: 137), xRadius: 42, yRadius: 42).fill()
    let cord = NSBezierPath()
    cord.move(to: NSPoint(x: 226, y: 200))
    cord.line(to: NSPoint(x: 226, y: 138))
    cord.curve(to: NSPoint(x: 290, y: 102), controlPoint1: NSPoint(x: 226, y: 95), controlPoint2: NSPoint(x: 265, y: 102))
    cord.lineWidth = 24
    cord.lineCapStyle = .round
    cord.stroke()
    NSColor(srgbRed: 0.40, green: 0.92, blue: 0.82, alpha: 1).setFill()
    NSBezierPath(ovalIn: NSRect(x: 286, y: 157, width: 133, height: 133)).fill()
    NSColor(srgbRed: 0.15, green: 0.14, blue: 0.35, alpha: 1).setStroke()
    for ends in [(NSPoint(x: 324, y: 224), NSPoint(x: 381, y: 224)), (NSPoint(x: 352, y: 195), NSPoint(x: 352, y: 253))] {
        let line = NSBezierPath()
        line.move(to: ends.0)
        line.line(to: ends.1)
        line.lineWidth = 14
        line.lineCapStyle = .round
        line.stroke()
    }
    NSGraphicsContext.restoreGraphicsState()
    try bitmap.representation(using: .png, properties: [:])!.write(to: output.appendingPathComponent(name + ".png"))
}
