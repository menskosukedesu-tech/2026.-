"""
Instagram Story Generator — @ko__sukedesu
出力: story/story_final.png (1080×1920)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# ── Paths ──────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_PATH = os.path.join(BASE_DIR, "images", "after-01.jpeg")
OUT_PATH   = os.path.join(BASE_DIR, "story", "story_final.png")

FONT_PATH  = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

# ── Canvas ─────────────────────────────────────────────────
W, H = 1080, 1920

# ── Colours ────────────────────────────────────────────────
GOLD      = (201, 168,  76)
GOLD_L    = (232, 201, 106)
WHITE     = (245, 240, 232)
WHITE_DIM = (245, 240, 232, 190)
BLACK     = (  0,   0,   0)

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_centered_text(draw, text, y, font, fill, anchor="mm"):
    draw.text((W // 2, y), text, font=font, fill=fill, anchor=anchor)

def draw_gradient_rect(img, x, y, w, h, color_top, color_bot):
    """Vertical RGBA gradient overlaid on img."""
    grad = Image.new("RGBA", (w, h))
    for row in range(h):
        t   = row / h
        a   = int(color_top[3] + (color_bot[3] - color_top[3]) * t)
        r   = int(color_top[0] + (color_bot[0] - color_top[0]) * t)
        g   = int(color_top[1] + (color_bot[1] - color_top[1]) * t)
        b   = int(color_top[2] + (color_bot[2] - color_top[2]) * t)
        grad.paste((r, g, b, a), (0, row, w, row + 1))
    img.alpha_composite(grad, (x, y))

# ── 1. Background photo ────────────────────────────────────
photo = Image.open(PHOTO_PATH).convert("RGB")
pw, ph = photo.size
canvas_ratio = W / H
img_ratio    = pw / ph

if img_ratio > canvas_ratio:
    new_h = H
    new_w = int(H * img_ratio)
else:
    new_w = W
    new_h = int(W / img_ratio)

photo = photo.resize((new_w, new_h), Image.LANCZOS)

# Portrait: keep upper 85% (face area)
crop_x = (new_w - W) // 2
crop_y = int((new_h - H) * 0.10)
photo  = photo.crop((crop_x, crop_y, crop_x + W, crop_y + H))

# Convert to RGBA for compositing
canvas = photo.convert("RGBA")

# ── 2. Gradient overlays ───────────────────────────────────
# Top vignette
draw_gradient_rect(canvas, 0, 0, W, 560,
    (0, 0, 0, 185), (0, 0, 0, 0))

# Bottom heavy
draw_gradient_rect(canvas, 0, H - 900, W, 900,
    (0, 0, 0,   0), (0, 0, 0, 245))

# Mid fade (helps text pop)
draw_gradient_rect(canvas, 0, H - 1100, W, 280,
    (0, 0, 0,  0), (0, 0, 0, 110))

# ── 3. Draw text ───────────────────────────────────────────
draw = ImageDraw.Draw(canvas)

f_28 = load_font(42)
f_36 = load_font(54)
f_44 = load_font(66)
f_56 = load_font(84)
f_72 = load_font(108)
f_96 = load_font(144)

# ── TOP LABELS ──
draw_centered_text(draw,
    "MENS PERM SPECIALIST  ·  神戸三宮",
    105, f_28, GOLD + (230,), anchor="mm")

draw_centered_text(draw,
    "@ ko__sukedesu",
    185, f_36, WHITE_DIM, anchor="mm")

# thin gold line under label
draw.line([(W//2 - 270, 216), (W//2 + 270, 216)],
          fill=GOLD + (100,), width=2)

# ── MAIN COPY (bottom) ──
BASE = H - 800

# Hook line 1
draw_centered_text(draw,
    "「おまかせします」しか",
    BASE, f_44, WHITE + (200,), anchor="mm")

# Hook line 2 — bold emphasis
draw_centered_text(draw,
    "言えなかった人へ。",
    BASE + 96, f_56, WHITE + (255,), anchor="mm")

# Divider
draw.line([(W//2 - 220, BASE + 148), (W//2 + 220, BASE + 148)],
          fill=GOLD + (120,), width=2)

# Value prop line 1
draw_centered_text(draw,
    "あなたの30%の言葉から",
    BASE + 234, f_44, WHITE + (220,), anchor="mm")

# "100%へ。" — large gold
draw_centered_text(draw,
    "100%へ。",
    BASE + 382, f_96, GOLD_L + (255,), anchor="mm")

# Subtitle
draw_centered_text(draw,
    "うまく伝えられなくても大丈夫。",
    BASE + 490, f_36, WHITE + (175,), anchor="mm")

# Spacer line
draw.line([(W//2 - 180, BASE + 540), (W//2 + 180, BASE + 540)],
          fill=GOLD + (90,), width=1)

# Name line
draw_centered_text(draw,
    "田中公亮 / メンズパーマ専門家",
    BASE + 604, f_36, WHITE + (190,), anchor="mm")

# ── CTA ──
cta_y   = H - 72
pill_w  = 680
pill_h  = 96
pill_x0 = (W - pill_w) // 2
pill_y0 = cta_y - pill_h // 2

# Pill background
pill = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
pd   = ImageDraw.Draw(pill)
r    = 48
pd.rounded_rectangle([0, 0, pill_w, pill_h], radius=r,
                     fill=(201, 168, 76, 50),
                     outline=(201, 168, 76, 200), width=2)
canvas.alpha_composite(pill, (pill_x0, pill_y0))

# CTA text
draw_centered_text(draw,
    "↑  プロフィールをチェック",
    cta_y, f_44, WHITE + (245,), anchor="mm")

# ── 4. Save ───────────────────────────────────────────────
out = canvas.convert("RGB")
out.save(OUT_PATH, "PNG", quality=95)
print(f"Saved → {OUT_PATH}")
