#!/usr/bin/env python3
"""Generate TypeSafe / Windows 3.1 wallpapers and theme preview images."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG = ROOT / "backgrounds"

PINK = (255, 128, 192)  # Windows 3.1 system pink #ff80c0
WHITE = (254, 254, 254)
NEAR_WHITE = (255, 255, 255)
DARK = (30, 30, 30)
MAGENTA = (212, 91, 182)
TEAL = (9, 174, 161)
GREEN = (3, 170, 92)
SAGE = (171, 186, 185)
GRAY = (222, 222, 222)
MID = (133, 133, 133)
NAVY = (0, 0, 128)
SILVER = (192, 192, 192)
DARKGRAY = (128, 128, 128)
BLACK = (0, 0, 0)
VGA_TEAL = (0, 128, 128)
LIGHT_CYAN = (128, 255, 255)
YELLOW = (201, 162, 39)

W, H = 1920, 1080


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def pixel_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return font(size)


def dither(size: tuple[int, int], a: tuple[int, int, int], b: tuple[int, int, int], scale: int = 2) -> Image.Image:
    """Bayer 4x4 dither between two colors, then nearest-neighbor upscale."""
    matrix = [
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5],
    ]
    w, h = size[0] // scale, size[1] // scale
    img = Image.new("RGB", (w, h), a)
    px = img.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = b if matrix[y % 4][x % 4] > 7 else a
    return img.resize(size, Image.NEAREST)


def checker(size: tuple[int, int], a, b, cell: int = 8) -> Image.Image:
    img = Image.new("RGB", (size[0] // 2, size[1] // 2), a)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if ((x // cell) + (y // cell)) % 2:
                px[x, y] = b
    return img.resize(size, Image.NEAREST)


def weave(size: tuple[int, int], a, b, period: int = 6) -> Image.Image:
    img = Image.new("RGB", (size[0] // 2, size[1] // 2), a)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if (x + y) % period == 0 or (x - y) % period == 0:
                px[x, y] = b
    return img.resize(size, Image.NEAREST)


def bricks(size: tuple[int, int], fill, grout, bw: int = 24, bh: int = 12) -> Image.Image:
    img = Image.new("RGB", (size[0] // 2, size[1] // 2), grout)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    row = 0
    y = 0
    while y < h:
        offset = (bw // 2) if row % 2 else 0
        x = -offset
        while x < w:
            draw.rectangle([x + 1, y + 1, x + bw - 2, y + bh - 2], fill=fill)
            x += bw
        y += bh
        row += 1
    return img.resize(size, Image.NEAREST)


def bevel(draw: ImageDraw.ImageDraw, box, highlight=WHITE, shadow=DARKGRAY, fill=SILVER, width: int = 2) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=fill)
    for i in range(width):
        draw.line([(x0 + i, y0 + i), (x1 - i, y0 + i)], fill=highlight)
        draw.line([(x0 + i, y0 + i), (x0 + i, y1 - i)], fill=highlight)
        draw.line([(x0 + i, y1 - i), (x1 - i, y1 - i)], fill=shadow)
        draw.line([(x1 - i, y0 + i), (x1 - i, y1 - i)], fill=shadow)
    draw.rectangle([x0, y0, x1, y1], outline=BLACK)


def inset(draw: ImageDraw.ImageDraw, box, width: int = 2) -> None:
    bevel(draw, box, highlight=DARKGRAY, shadow=WHITE, fill=WHITE, width=width)


def win31_window(
    canvas: Image.Image,
    box,
    title: str,
    active: bool = True,
    client_fill=WHITE,
    content: str | None = None,
) -> None:
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    # Drop shadow — the Windows 3.1 tell.
    draw.rectangle([x0 + 4, y0 + 4, x1 + 4, y1 + 4], fill=BLACK)
    bevel(draw, box, fill=SILVER, width=3)

    title_h = 22
    tb = [x0 + 4, y0 + 4, x1 - 4, y0 + 4 + title_h]
    draw.rectangle(tb, fill=NAVY if active else DARKGRAY)
    # System menu box
    sys = [tb[0] + 2, tb[1] + 3, tb[0] + 16, tb[3] - 3]
    bevel(draw, sys, fill=SILVER, width=1)
    draw.line([(sys[0] + 3, (sys[1] + sys[3]) // 2), (sys[2] - 3, (sys[1] + sys[3]) // 2)], fill=BLACK, width=2)
    # Min / max
    for i, glyph in enumerate(["_", "\u25a1"]):
        bx0 = tb[2] - 36 + i * 16
        btn = [bx0, tb[1] + 3, bx0 + 14, tb[3] - 3]
        bevel(draw, btn, fill=SILVER, width=1)
        draw.text((bx0 + 3, tb[1] + 2), glyph, fill=BLACK, font=pixel_font(10))

    tfont = pixel_font(13)
    draw.text((tb[0] + 22, tb[1] + 3), title, fill=WHITE, font=tfont)

    client = [x0 + 6, y0 + 4 + title_h + 4, x1 - 6, y1 - 6]
    draw.rectangle(client, fill=client_fill, outline=DARKGRAY)
    if content:
        draw.multiline_text(
            (client[0] + 10, client[1] + 8),
            content,
            fill=DARK,
            font=pixel_font(13),
            spacing=6,
        )


def wallpaper_typesafe_desktop() -> Image.Image:
    img = Image.new("RGB", (W, H), PINK)
    # Subtle VGA-style dither toward a slightly deeper pink.
    overlay = dither((W, H), PINK, (192, 64, 128), scale=2)
    return Image.blend(img, overlay, 0.18)


def wallpaper_win31_teal() -> Image.Image:
    return dither((W, H), VGA_TEAL, (0, 112, 112), scale=2)


def wallpaper_program_manager() -> Image.Image:
    img = wallpaper_typesafe_desktop()
    win31_window(
        img,
        (180, 140, 820, 620),
        "Program Manager",
        content="File    Options    Window    Help\n\n"
        "  [TS]  TypeSafe AI\n"
        "  [..]  File Manager\n"
        "  [><]  MS-DOS Prompt\n"
        "  [++]  Control Panel\n"
        "  [??]  Windows Setup\n\n"
        "  TS.AI.0S1  \u2014  System One",
    )
    win31_window(
        img,
        (980, 220, 1680, 760),
        "Jev \u2014 typed decisions",
        content="C:\\TYPESAFE> jev --calibrate\n\n"
        "  decisions, not strings\n"
        "  calibrated confidence  0.97\n"
        "  more like code\n\n"
        "  $42 / billion input tokens\n"
        "  238x lower than chat\n\n"
        "  [b.64]  ready.",
        client_fill=(20, 20, 20),
    )
    # Recolor DOS prompt text by redrawing over dark client? Keep as-is;
    # dark client with dark text is wrong. Redraw that window's text in sage.
    draw = ImageDraw.Draw(img)
    draw.rectangle([986, 250, 1674, 754], fill=(18, 18, 18))
    draw.multiline_text(
        (1000, 270),
        "C:\\TYPESAFE> jev --calibrate\n\n"
        "  decisions, not strings\n"
        "  calibrated confidence  0.97\n"
        "  more like code\n\n"
        "  $42 / billion input tokens\n"
        "  238x lower than chat\n\n"
        "  [b.64]  ready.",
        fill=GREEN,
        font=pixel_font(14),
        spacing=6,
    )
    return img


def wallpaper_tiles() -> Image.Image:
    # Classic Win3.1 "Squares" using TypeSafe pink / magenta / teal.
    cell = 16
    src_w, src_h = W // 2, H // 2
    img = Image.new("RGB", (src_w, src_h), PINK)
    draw = ImageDraw.Draw(img)
    colors = [PINK, MAGENTA, TEAL, SAGE, SILVER]
    i = 0
    for y in range(0, src_h, cell):
        for x in range(0, src_w, cell):
            c = colors[(x // cell + y // cell) % len(colors)]
            draw.rectangle([x, y, x + cell - 2, y + cell - 2], fill=c, outline=DARK)
            i += 1
    return img.resize((W, H), Image.NEAREST)


def wallpaper_argyle() -> Image.Image:
    img = Image.new("RGB", (W // 2, H // 2), PINK)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    step = 48
    for y in range(-h, h * 2, step):
        for x in range(-w, w * 2, step):
            diamond = [
                (x, y + step // 2),
                (x + step // 2, y),
                (x + step, y + step // 2),
                (x + step // 2, y + step),
            ]
            color = TEAL if ((x + y) // step) % 2 == 0 else MAGENTA
            draw.polygon(diamond, fill=color, outline=DARK)
    return img.resize((W, H), Image.NEAREST)


def wallpaper_sage_weave() -> Image.Image:
    return weave((W, H), SAGE, (154, 170, 169), period=8)


def wallpaper_hot_magenta() -> Image.Image:
    return dither((W, H), MAGENTA, (190, 70, 160), scale=2)


def wallpaper_navy_dots() -> Image.Image:
    img = Image.new("RGB", (W // 2, H // 2), NAVY)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if x % 8 == 0 and y % 8 == 0:
                px[x, y] = PINK
            elif x % 8 == 4 and y % 8 == 4:
                px[x, y] = TEAL
    return img.resize((W, H), Image.NEAREST)


def wallpaper_bricks() -> Image.Image:
    return bricks((W, H), PINK, DARK, bw=28, bh=14)


def make_preview() -> Image.Image:
    """Theme-switcher preview: a composed Win31 desktop."""
    pw, ph = 1440, 900
    desktop = wallpaper_typesafe_desktop().resize((pw, ph), Image.NEAREST)
    img = desktop.copy()
    draw = ImageDraw.Draw(img)

    # Waybar as a pink title strip.
    draw.rectangle([0, 0, pw, 36], fill=PINK)
    draw.line([(0, 36), (pw, 36)], fill=DARK, width=2)
    draw.text((14, 8), "Omarchy   1  2  3  4  5", fill=DARK, font=pixel_font(16))
    draw.text((pw - 280, 8), "Fri 13:31    100%    12:00", fill=DARK, font=pixel_font(16))

    win31_window(
        img,
        (70, 80, 620, 520),
        "File Manager",
        content="C:\\OMARCHY\\THEMES\\WINDOWS-3\n\n"
        "  colors.toml\n"
        "  waybar.css\n"
        "  hyprland.conf\n"
        "  gtk.css\n"
        "  neovim.lua\n"
        "  backgrounds\\",
    )
    win31_window(
        img,
        (560, 160, 1360, 780),
        "TypeSafe \u2014 TS.AI.0S1",
        content="",
        client_fill=WHITE,
    )
    # Inner typesafe content
    draw.rectangle([568, 190, 1352, 772], fill=PINK)
    draw.text((600, 230), "We took the opposite", fill=DARK, font=font(36, bold=True))
    draw.text((600, 276), "research direction", fill=DARK, font=font(36, bold=True))
    draw.rectangle([600, 360, 780, 392], fill=MAGENTA)
    draw.text((612, 366), "not chat", fill=WHITE, font=pixel_font(16))
    draw.text(
        (600, 420),
        "Typed outputs. Calibrated confidence.\nMore like code.",
        fill=DARK,
        font=pixel_font(18),
        spacing=8,
    )
    draw.rectangle([600, 520, 920, 560], fill=TEAL)
    draw.text((620, 530), "accent  #09AEA1", fill=WHITE, font=pixel_font(16))
    draw.rectangle([940, 520, 1260, 560], fill=DARK)
    draw.text((960, 530), "chrome  #1E1E1E", fill=WHITE, font=pixel_font(16))

    # Palette swatches
    swatches = [
        ("pink", PINK),
        ("teal", TEAL),
        ("magenta", MAGENTA),
        ("navy", NAVY),
        ("sage", SAGE),
        ("green", GREEN),
    ]
    x = 90
    y = 800
    for name, color in swatches:
        draw.rectangle([x, y, x + 70, y + 40], fill=color, outline=BLACK)
        draw.text((x, y + 44), name, fill=DARK, font=pixel_font(11))
        x += 90

    return img


def make_unlock() -> Image.Image:
    """Transparent 128x128 Win31 window glyph for Plymouth unlock."""
    rgb = Image.new("RGB", (128, 128), (255, 0, 255))
    win31_window(rgb, (6, 8, 118, 116), "Lock", content="  * * * *")
    rgba = rgb.convert("RGBA")
    px = rgba.load()
    for y in range(128):
        for x in range(128):
            r, g, b, a = px[x, y]
            if (r, g, b) == (255, 0, 255):
                px[x, y] = (0, 0, 0, 0)
    return rgba


def make_preview_unlock() -> Image.Image:
    img = wallpaper_typesafe_desktop().resize((800, 500), Image.NEAREST)
    win31_window(img, (180, 90, 620, 380), "Omarchy", content="\n\n     Enter password\n\n     [ ************  ]\n\n         [ OK ]")
    return img


def save_jpeg(img: Image.Image, path: Path, quality: int = 92) -> None:
    img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True)


def save_png(img: Image.Image, path: Path) -> None:
    img.save(path, "PNG", optimize=True)


def main() -> None:
    BG.mkdir(parents=True, exist_ok=True)

    assets = {
        "01-typesafe-desktop.jpg": wallpaper_typesafe_desktop(),
        "02-program-manager.jpg": wallpaper_program_manager(),
        "03-win31-teal.jpg": wallpaper_win31_teal(),
        "04-typesafe-tiles.jpg": wallpaper_tiles(),
        "05-argyle.jpg": wallpaper_argyle(),
        "06-sage-weave.jpg": wallpaper_sage_weave(),
        "07-hot-magenta.jpg": wallpaper_hot_magenta(),
        "08-navy-dots.jpg": wallpaper_navy_dots(),
        "09-pink-bricks.jpg": wallpaper_bricks(),
    }
    for name, image in assets.items():
        save_jpeg(image, BG / name)
        print(f"wrote {BG / name} {image.size}")

    save_png(make_preview(), ROOT / "preview.png")
    save_png(make_unlock(), ROOT / "unlock.png")
    save_png(make_preview_unlock(), ROOT / "preview-unlock.png")
    print("wrote preview + unlock images")


if __name__ == "__main__":
    main()
