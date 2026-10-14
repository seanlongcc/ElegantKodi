"""Generate the skin's small, antialiased native interface textures (Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "skin.elegantfin/media/elegantfin"
MEDIA.mkdir(parents=True, exist_ok=True)


def rounded(name, size, radius, outline=None, width=1):
    scale = 4
    image = Image.new("RGBA", tuple(v * scale for v in size))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((2, 2, size[0] * scale - 3, size[1] * scale - 3),
                           radius=radius * scale, fill=None if outline else "white",
                           outline="white" if outline else None, width=width * scale)
    image.resize(size, Image.Resampling.LANCZOS).save(MEDIA / name)


rounded("round.png", (64, 64), 20)
rounded("outline.png", (64, 64), 20, outline=True)
rounded("focus.png", (64, 64), 22, outline=True, width=3)
rounded("mask-wide.png", (660, 360), 36)
rounded("mask-poster.png", (456, 684), 32)
rounded("mask-landscape.png", (804, 452), 36)
rounded("mask-cast.png", (396, 440), 32)

shade = Image.new("RGBA", (16, 1080))
draw = ImageDraw.Draw(shade)
for y in range(1080):
    alpha = round(38 + 217 * min(1, max(0, (y - 270) / 620)))
    draw.line((0, y, 16, y), fill=(17, 24, 39, alpha))
shade.save(MEDIA / "detail-shade.png")

background = Image.new("RGB", (64, 1080))
draw = ImageDraw.Draw(background)
for y in range(1080):
    t = min(1, y / 750)
    color = tuple(round(a + (b - a) * t) for a, b in zip((29, 38, 53), (17, 24, 39)))
    draw.line((0, y, 64, y), fill=color)
background.save(MEDIA / "background.png")

mark = Image.new("RGBA", (256, 256))
draw = ImageDraw.Draw(mark)
draw.rounded_rectangle((14, 14, 242, 242), radius=68, fill="#756fe2")
draw.rounded_rectangle((64, 62, 194, 85), radius=10, fill="#ffffff")
draw.rounded_rectangle((64, 116, 165, 139), radius=10, fill="#ffffff")
draw.rounded_rectangle((64, 170, 194, 193), radius=10, fill="#ffffff")
mark.save(MEDIA / "mark.png")

watched = Image.new("RGBA", (116, 116))
draw = ImageDraw.Draw(watched)
draw.ellipse((2, 2, 114, 114), fill="#32a769")
draw.line([(30, 57), (49, 76), (85, 37)], fill="white", width=10, joint="curve")
watched.resize((58, 58), Image.Resampling.LANCZOS).save(MEDIA / "watched.png")

resources = ROOT / "skin.elegantfin/resources"
icon = Image.new("RGB", (512, 512), "#111827")
icon.paste(mark, (128, 128), mark)
icon.save(resources / "elegantfin-icon.png")
banner = background.resize((1920, 1080))
banner.paste(mark, (832, 320), mark)
draw = ImageDraw.Draw(banner)
font = ImageFont.truetype(str(ROOT / "skin.elegantfin/fonts/NotoSans-Regular.ttf"), 80)
draw.text((960, 650), "ElegantFin", font=font, anchor="mm", fill="#d1d5db")
font = ImageFont.truetype(str(ROOT / "skin.elegantfin/fonts/NotoSans-Regular.ttf"), 28)
draw.text((960, 740), "FOR KODI", font=font, anchor="mm", fill="#9ca3af")
banner.save(resources / "elegantfin-fanart.png")
print(f"Generated {len(list(MEDIA.glob('*.png')))} textures and 2 branding assets")
