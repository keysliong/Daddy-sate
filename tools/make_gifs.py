"""Генератор пиксельных гифок для открытки.  python3 tools/make_gifs.py"""
import math, random, os
from PIL import Image, ImageDraw

S = 64          # логическое разрешение
K = 4           # масштаб -> 256x256
BG = (13, 17, 23)
OUT = os.path.join(os.path.dirname(__file__), "..", "gif")
os.makedirs(OUT, exist_ok=True)


def frame():
    im = Image.new("RGB", (S, S), BG)
    return im, ImageDraw.Draw(im)


def save(name, frames, ms=90):
    big = [f.resize((S * K, S * K), Image.NEAREST) for f in frames]
    big[0].save(os.path.join(OUT, name), save_all=True, append_images=big[1:],
                duration=ms, loop=0, optimize=True)
    print("ok", name)


def heart(d, cx, cy, r, col):
    for y in range(-r * 2, r * 2):
        for x in range(-r * 2, r * 2):
            X, Y = x / r, -y / r
            if (X * X + Y * Y - 1) ** 3 - X * X * Y ** 3 <= 0:
                d.point((cx + x, cy + y), col)


# 1. Сердце бьётся (первые шаги вместе)
fr = []
for i in range(12):
    im, d = frame()
    s = 1 + 0.18 * max(0, math.sin(i / 12 * math.pi * 2))
    heart(d, 32, 30, int(14 * s), (255, 70, 110))
    heart(d, 27, 25, max(2, int(3 * s)), (255, 170, 190))
    d.text((14, 52), "<3 2019", fill=(255, 140, 170))
    fr.append(im)
save("heart.gif", fr, 80)

# 2. Сон в машине: Zzz
fr = []
for i in range(16):
    im, d = frame()
    d.ellipse((10, 34, 34, 58), fill=(255, 205, 160))         # лицо
    d.pieslice((8, 26, 36, 52), 180, 360, fill=(40, 90, 200))  # шапка
    d.ellipse((18, 22, 26, 30), fill=(90, 160, 255))           # помпон
    d.line((15, 46, 20, 46), fill=(60, 40, 30))
    d.line((24, 46, 29, 46), fill=(60, 40, 30))
    for k in range(3):
        t = (i + k * 5) % 16
        x, y = 36 + t * 1.3, 40 - t * 2.2
        c = int(255 * (1 - t / 16))
        d.text((x, y), "z" if k % 2 else "Z", fill=(c, c, 255))
    fr.append(im)
save("zzz.gif", fr, 110)

# 3. Улыбка + подмигивание + искры
fr = []
random.seed(3)
for i in range(14):
    im, d = frame()
    d.ellipse((12, 12, 52, 52), fill=(255, 210, 60))
    if i in (6, 7, 8):
        d.line((22, 26, 28, 26), fill=(40, 30, 0), width=2)
    else:
        d.ellipse((22, 22, 28, 30), fill=(40, 30, 0))
    d.ellipse((36, 22, 42, 30), fill=(40, 30, 0))
    d.arc((20, 26, 44, 44), 20, 160, fill=(40, 30, 0), width=2)
    for _ in range(5):
        x, y = random.randint(0, 63), random.randint(0, 63)
        if (x - 32) ** 2 + (y - 32) ** 2 > 420:
            d.point((x, y), (255, 255, 255))
            d.point((x + 1, y), (255, 240, 150))
    fr.append(im)
save("smile.gif", fr, 100)

# 4. Газировка с пузырьками (кафе)
fr = []
for i in range(14):
    im, d = frame()
    d.polygon([(18, 18), (46, 18), (42, 58), (22, 58)], fill=(30, 60, 140))
    d.polygon([(19, 24), (45, 24), (41.5, 56), (22.5, 56)], fill=(80, 30, 20))
    d.line((36, 6, 32, 30), fill=(255, 255, 255), width=2)
    d.line((36, 6, 44, 4), fill=(255, 80, 80), width=2)
    for k in range(6):
        t = (i * 2 + k * 7) % 30
        x = 24 + (k * 5) % 16
        d.point((x, 55 - t), (255, 220, 180))
    fr.append(im)
save("soda.gif", fr, 90)

# 5. Кофе с паром (папа-программист)
fr = []
for i in range(12):
    im, d = frame()
    d.rectangle((16, 30, 42, 56), fill=(240, 240, 240))
    d.rectangle((18, 32, 40, 36), fill=(110, 60, 30))
    d.ellipse((38, 36, 50, 50), outline=(240, 240, 240), width=3)
    d.text((20, 42), "PHP", fill=(120, 123, 180))
    for k in range(3):
        for y in range(6, 28):
            x = 22 + k * 7 + 2 * math.sin((y + i * 2) / 3 + k)
            if (y + i) % 9 < 6:
                d.point((x, y), (170, 170, 190))
    fr.append(im)
save("coffee.gif", fr, 100)

# 6. Шайба в ворота (хоккей)
fr = []
for i in range(16):
    im, d = frame()
    d.rectangle((0, 40, 63, 63), fill=(210, 235, 250))
    d.line((0, 52, 63, 52), fill=(220, 60, 60))
    d.rectangle((44, 22, 62, 46), outline=(220, 40, 40), width=2)
    for y in range(24, 46, 3):
        d.line((46, y, 61, y), fill=(200, 200, 210))
    t = i / 15
    x = 6 + t * 46
    d.ellipse((x, 42, x + 7, 46), fill=(20, 20, 20))
    if i > 11:
        d.text((8, 6), "GOAL!", fill=(255, 220, 0) if i % 2 else (255, 80, 80))
    fr.append(im)
save("puck.gif", fr, 90)

# 7. Торт со свечами
fr = []
for i in range(10):
    im, d = frame()
    d.rectangle((10, 40, 54, 58), fill=(240, 120, 170))
    d.rectangle((14, 28, 50, 40), fill=(250, 210, 230))
    for x in range(10, 55, 6):
        d.ellipse((x, 38, x + 6, 44), fill=(255, 255, 255))
    for k, x in enumerate((20, 30, 40)):
        d.rectangle((x, 16, x + 3, 28), fill=(120, 180, 255))
        fl = (i + k) % 3
        d.ellipse((x - 1, 8 - fl, x + 4, 15), fill=(255, 200, 40))
        d.point((x + 1, 12), (255, 255, 200))
    fr.append(im)
save("cake.gif", fr, 110)

# 8. Салют
fr = []
random.seed(7)
bursts = [(random.randint(12, 52), random.randint(10, 36), random.choice(
    [(255, 80, 80), (80, 200, 255), (255, 220, 60), (180, 120, 255), (90, 255, 140)]), random.randint(0, 20))
    for _ in range(5)]
for i in range(24):
    im, d = frame()
    for (cx, cy, col, st) in bursts:
        t = (i - st) % 24
        if t < 12:
            r = t * 1.6
            fade = 1 - t / 12
            c = tuple(int(v * fade + BG[j] * (1 - fade)) for j, v in enumerate(col))
            for a in range(12):
                ang = a / 12 * math.tau
                d.point((cx + r * math.cos(ang), cy + r * math.sin(ang) + t * 0.2), c)
    fr.append(im)
save("fireworks.gif", fr, 70)

# 9. Ноты (концерт)
fr = []
for i in range(16):
    im, d = frame()
    for k, col in enumerate([(255, 90, 200), (120, 200, 255), (255, 230, 90)]):
        t = (i + k * 5) % 16
        x, y = 10 + k * 17, 50 - t * 2.4
        d.ellipse((x, y, x + 7, y + 5), fill=col)
        d.line((x + 6, y + 2, x + 6, y - 12), fill=col, width=2)
        d.line((x + 6, y - 12, x + 11, y - 8), fill=col, width=2)
    if i % 4 < 2:
        d.text((20, 2), "WOW!", fill=(255, 255, 255))
    fr.append(im)
save("notes.gif", fr, 90)

# 10. Баня: шайка и пар
fr = []
for i in range(12):
    im, d = frame()
    d.rectangle((0, 0, 63, 63), fill=(120, 70, 30))
    for y in range(0, 64, 8):
        d.line((0, y, 63, y), fill=(95, 55, 22))
    d.polygon([(14, 40), (50, 40), (46, 58), (18, 58)], fill=(200, 140, 70))
    d.line((14, 46, 50, 46), fill=(90, 50, 20), width=2)
    d.line((16, 53, 48, 53), fill=(90, 50, 20), width=2)
    for k in range(4):
        for y in range(6, 38):
            x = 18 + k * 8 + 2 * math.sin((y + i * 2) / 3 + k)
            if (y + i + k * 2) % 10 < 6:
                d.point((x, y), (235, 235, 235))
    d.rectangle((54, 6, 58, 30), fill=(240, 240, 240))
    lv = 22 - (i % 6)
    d.rectangle((55, 6 + lv - 16, 57, 30), fill=(230, 40, 40))
    fr.append(im)
save("sauna.gif", fr, 100)

# 11. Звезда 1UP (сын — главный проект)
fr = []
for i in range(12):
    im, d = frame()
    s = 1 + 0.15 * math.sin(i / 12 * math.tau)
    pts = []
    for a in range(10):
        r = (22 if a % 2 == 0 else 9) * s
        ang = -math.pi / 2 + a * math.pi / 5
        pts.append((32 + r * math.cos(ang), 30 + r * math.sin(ang)))
    d.polygon(pts, fill=(255, 210, 40))
    d.rectangle((26, 24, 28, 30), fill=(40, 30, 0))
    d.rectangle((36, 24, 38, 30), fill=(40, 30, 0))
    d.text((22, 52), "1UP", fill=(90, 255, 140) if i % 2 else (255, 255, 255))
    fr.append(im)
save("star.gif", fr, 90)
