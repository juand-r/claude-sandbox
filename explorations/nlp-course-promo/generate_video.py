#!/usr/bin/env python3
"""
Generate a meme-style promo video for Greg Durrett's
"Building LLM Reasoners" course at NYU, Spring 2026.

v2: Complete rewrite with better audio, varied backgrounds,
beat-synced effects, zoom/scale transforms, and more visual energy.
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from moviepy import VideoClip, AudioClip

# ── Config ──────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1080, 1920  # 9:16 vertical
FPS = 30
BPM = 140  # Faster tempo for more energy
BEAT_SEC = 60.0 / BPM  # seconds per beat

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 16, 240)
NEON_BLUE = (0, 200, 255)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
ELECTRIC_PURPLE = (191, 0, 255)
HOT_RED = (255, 36, 0)
DARK_BLUE = (8, 8, 30)
DARK_PURPLE = (15, 5, 25)
DARK_GREEN = (5, 15, 8)
DARK_RED = (20, 5, 5)

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# Font cache
_font_cache = {}
def load_font(path, size):
    key = (path, size)
    if key not in _font_cache:
        try:
            _font_cache[key] = ImageFont.truetype(path, size)
        except Exception:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


# ── Drawing helpers ─────────────────────────────────────────────────────────

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_text_xy(draw, text, cx, cy, font, fill=WHITE,
                 stroke_width=0, stroke_fill=BLACK):
    """Draw text centered at (cx, cy)."""
    tw, th = text_size(draw, text, font)
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)


def draw_glow_text(draw, text, cx, cy, font, color, glow=5):
    """Text with bloom/glow."""
    for r in range(glow, 0, -1):
        a = max(10, int(40 / r))
        gc = tuple(min(255, int(c * a / 100)) for c in color)
        for dx, dy in [(-r, 0), (r, 0), (0, -r), (0, r),
                       (-r, -r), (r, r), (-r, r), (r, -r)]:
            draw_text_xy(draw, text, cx + dx, cy + dy, font, fill=gc)
    draw_text_xy(draw, text, cx, cy, font, fill=color,
                 stroke_width=2, stroke_fill=BLACK)


def ease_out_back(t):
    """Overshoot ease-out for punchy animations."""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


def ease_out_elastic(t):
    """Elastic bounce ease-out."""
    if t == 0 or t == 1:
        return t
    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1


def lerp(a, b, t):
    return a + (b - a) * max(0, min(1, t))


# ── Background generators (varied!) ────────────────────────────────────────

def bg_gradient_radial(color1, color2, cx=0.5, cy=0.5, radius=1.0):
    """Radial gradient background."""
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    dist = np.sqrt(((X / WIDTH - cx) ** 2 + (Y / HEIGHT - cy) ** 2)) / radius
    dist = np.clip(dist, 0, 1)
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for i in range(3):
        pixels[:, :, i] = (color1[i] * (1 - dist) + color2[i] * dist).astype(np.uint8)
    return Image.fromarray(pixels)


def bg_diagonal_stripes(color1, color2, stripe_width=80, angle_offset=0):
    """Diagonal stripe pattern."""
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    pattern = ((X + Y + angle_offset) // stripe_width) % 2
    for i in range(3):
        pixels[:, :, i] = np.where(pattern == 0, color1[i], color2[i]).astype(np.uint8)
    return Image.fromarray(pixels)


def bg_moving_gradient(t, color_top, color_bot, wave_color, wave_amp=40):
    """Animated horizontal gradient with wave distortion."""
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    Y = np.arange(HEIGHT)[:, np.newaxis]
    frac = Y / HEIGHT
    wave = wave_amp * np.sin(frac * 6 + t * 4) / HEIGHT
    frac_warped = np.clip(frac + wave, 0, 1)
    for i in range(3):
        base = color_top[i] * (1 - frac_warped) + color_bot[i] * frac_warped
        # Add wave accent
        wave_brightness = 0.3 * np.abs(np.sin(frac * 8 + t * 3))
        pixels[:, :, i] = base + wave_color[i] * wave_brightness
    return Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))


def bg_concentric_rings(t, color, bg_color=(10, 10, 20), num_rings=12):
    """Animated expanding concentric rings."""
    pixels = np.full((HEIGHT, WIDTH, 3), bg_color, dtype=np.uint8)
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    dist = np.sqrt((X - WIDTH / 2) ** 2 + (Y - HEIGHT / 2) ** 2)
    for i in range(num_rings):
        ring_r = (t * 200 + i * 150) % (WIDTH * 1.2)
        ring_mask = np.abs(dist - ring_r) < 4
        brightness = max(0.1, 1.0 - i * 0.08)
        for c in range(3):
            pixels[:, :, c] = np.where(ring_mask,
                                       int(color[c] * brightness), pixels[:, :, c])
    return Image.fromarray(pixels)


# ── Post-processing ─────────────────────────────────────────────────────────

def apply_zoom(img, scale):
    """Zoom into center of image."""
    if abs(scale - 1.0) < 0.001:
        return img
    w, h = img.size
    new_w, new_h = int(w / scale), int(h / scale)
    left = (w - new_w) // 2
    top = (h - new_h) // 2
    cropped = img.crop((left, top, left + new_w, top + new_h))
    return cropped.resize((w, h), Image.BILINEAR)


def apply_shake(img, amount_x, amount_y):
    """Translate image for screen shake."""
    return ImageChops.offset(img, int(amount_x), int(amount_y))


def apply_chromatic_aberration(img, offset):
    """RGB split for glitch look."""
    if offset == 0:
        return img
    pixels = np.array(img)
    r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
    r = np.roll(r, offset, axis=1)
    b = np.roll(b, -offset, axis=1)
    return Image.fromarray(np.stack([r, g, b], axis=2))


def apply_scanlines(pixels_np, strength=25):
    """Fast scanlines on numpy array."""
    pixels_np[::3, :] = np.clip(pixels_np[::3, :].astype(np.int16) - strength, 0, 255).astype(np.uint8)
    return pixels_np


def apply_vignette(pixels_np, strength=0.5):
    """Apply vignette to numpy array."""
    cy, cx = HEIGHT / 2, WIDTH / 2
    max_dist = math.sqrt(cx ** 2 + cy ** 2)
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2) / max_dist
    vignette = (1.0 - strength * dist ** 1.5)[:, :, np.newaxis]
    return np.clip(pixels_np * vignette, 0, 255).astype(np.uint8)


def beat_phase(t):
    """Returns 0-1 phase within current beat."""
    return (t / BEAT_SEC) % 1.0


def on_beat(t, window=0.08):
    """True if near a beat hit."""
    return beat_phase(t) < window


def beat_intensity(t, decay=0.15):
    """Exponential decay from last beat, 1.0 at beat, decays to 0."""
    phase = beat_phase(t)
    if phase < decay:
        return 1.0 - phase / decay
    return 0.0


# ── Scene Definitions ───────────────────────────────────────────────────────

def scene_intro(t):
    """Opening: flash, 'YO.' with zoom, then 'YOU NEED THIS COURSE' slam."""
    # Background: radial gradient that pulses
    pulse = beat_intensity(t)
    bg_r = int(lerp(5, 40, pulse))
    img = bg_gradient_radial((bg_r, bg_r + 5, bg_r), BLACK, radius=0.8)
    draw = ImageDraw.Draw(img)

    if t < 0.4:
        # Hard white flash
        flash = max(0, 1.0 - t / 0.4)
        pixels = np.array(img).astype(np.float32)
        pixels += flash * 255
        img = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
        draw = ImageDraw.Draw(img)
    elif t < 1.8:
        # "YO." with scale-in
        progress = min(1.0, (t - 0.4) / 0.25)
        scale = ease_out_back(progress)
        font_size = int(180 * scale)
        font = load_font(FONT_BOLD, max(10, font_size))
        draw_glow_text(draw, "YO.", WIDTH // 2, HEIGHT // 2, font, NEON_GREEN, glow=8)
        # Chromatic aberration on beat
        if pulse > 0.3:
            img = apply_chromatic_aberration(img, int(pulse * 25))
    elif t < 2.1:
        # Glitch transition
        font = load_font(FONT_BOLD, 180)
        draw_glow_text(draw, "YO.", WIDTH // 2, HEIGHT // 2, font, NEON_GREEN, glow=8)
        img = apply_chromatic_aberration(img, int(40 * math.sin(t * 50)))
        # Horizontal glitch bars
        pixels = np.array(img)
        for _ in range(8):
            y_start = random.randint(0, HEIGHT - 40)
            h = random.randint(5, 30)
            shift = random.randint(-60, 60)
            pixels[y_start:y_start + h] = np.roll(pixels[y_start:y_start + h], shift, axis=1)
        img = Image.fromarray(pixels)
    else:
        # "YOU NEED THIS COURSE." — slam in with shake
        slam_t = t - 2.1
        scale = ease_out_back(min(1.0, slam_t / 0.15))
        shake_x = int(15 * math.sin(slam_t * 40) * max(0, 1 - slam_t * 3))
        shake_y = int(10 * math.cos(slam_t * 35) * max(0, 1 - slam_t * 3))

        font_size = int(90 * scale)
        font = load_font(FONT_BOLD, max(10, font_size))
        draw_glow_text(draw, "YOU NEED", WIDTH // 2 + shake_x,
                       HEIGHT // 2 - 80 + shake_y, font, NEON_PINK, glow=6)
        draw_glow_text(draw, "THIS COURSE.", WIDTH // 2 + shake_x,
                       HEIGHT // 2 + 80 + shake_y, font, NEON_PINK, glow=6)

    result = np.array(img)
    apply_scanlines(result, 20)
    return result


def scene_course_name(t):
    """Course name with concentric rings background."""
    img = bg_moving_gradient(t, DARK_BLUE, (5, 5, 20), (0, 40, 80))
    draw = ImageDraw.Draw(img)

    # Beat pulse flash
    pulse = beat_intensity(t)
    if pulse > 0.5:
        pixels = np.array(img).astype(np.float32)
        pixels += pulse * 30
        img = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
        draw = ImageDraw.Draw(img)

    font_label = load_font(FONT_MONO, 40)
    draw_text_xy(draw, "[ NEW COURSE DROP ]", WIDTH // 2, 480,
                 font_label, NEON_GREEN, stroke_width=2, stroke_fill=BLACK)

    # Staggered word reveal with scale animation
    words = [
        ("BUILDING", 0.3, NEON_BLUE, 750),
        ("LLM", 0.8, NEON_YELLOW, 920),
        ("REASONERS", 1.3, HOT_RED, 1090),
    ]
    for word, threshold, color, y in words:
        if t > threshold:
            progress = min(1.0, (t - threshold) / 0.2)
            scale = ease_out_back(progress)
            font = load_font(FONT_BOLD, max(10, int(110 * scale)))
            draw_glow_text(draw, word, WIDTH // 2, y, font, color, glow=6)

    if t > 2.0:
        font_sub = load_font(FONT_REGULAR, 48)
        draw_text_xy(draw, "NYU  //  Spring 2026", WIDTH // 2, 1260,
                     font_sub, WHITE, stroke_width=2, stroke_fill=BLACK)

    # Decorative box
    if t > 1.3:
        box_alpha = min(1.0, (t - 1.3) / 0.3)
        box_color = tuple(int(c * box_alpha) for c in NEON_BLUE)
        draw.rectangle([60, 680, WIDTH - 60, 1180], outline=box_color, width=3)

    result = np.array(img)
    apply_scanlines(result, 15)
    result = apply_vignette(result, 0.4)
    return result


def scene_instructor(t):
    """Greg Durrett intro with diagonal stripes bg."""
    stripe_offset = int(t * 120)
    img = bg_diagonal_stripes(DARK_PURPLE, (20, 8, 30), stripe_width=100,
                              angle_offset=stripe_offset)
    draw = ImageDraw.Draw(img)

    pulse = beat_intensity(t)

    font_label = load_font(FONT_MONO, 36)
    font_big = load_font(FONT_BOLD, 110)
    font_small = load_font(FONT_REGULAR, 48)

    draw_text_xy(draw, "TAUGHT BY", WIDTH // 2, 620, font_label, NEON_GREEN,
                 stroke_width=2, stroke_fill=BLACK)

    # Name with beat-synced glow
    glow_r = int(5 + pulse * 8)
    draw_glow_text(draw, "GREG", WIDTH // 2, 790, font_big, WHITE, glow=glow_r)
    draw_glow_text(draw, "DURRETT", WIDTH // 2, 940, font_big, NEON_PINK, glow=glow_r)

    if t > 0.8:
        alpha = min(1.0, (t - 0.8) / 0.3)
        c = tuple(int(v * alpha) for v in NEON_YELLOW)
        draw_text_xy(draw, "NLP + LLM researcher", WIDTH // 2, 1100,
                     font_small, c, stroke_width=2, stroke_fill=BLACK)
    if t > 1.3:
        alpha = min(1.0, (t - 1.3) / 0.3)
        c = tuple(int(v * alpha) for v in NEON_ORANGE)
        draw_text_xy(draw, "NYU CS & CDS", WIDTH // 2, 1180,
                     font_small, c, stroke_width=2, stroke_fill=BLACK)

    result = np.array(img)
    apply_scanlines(result, 20)
    result = apply_vignette(result, 0.5)

    # Beat zoom
    if pulse > 0.3:
        img2 = Image.fromarray(result)
        img2 = apply_zoom(img2, 1.0 + pulse * 0.03)
        result = np.array(img2)

    return result


def scene_topics_scroll(t):
    """Rapid-fire topics with varied backgrounds per topic."""
    topics = [
        ("TRANSFORMERS", NEON_BLUE, "not the movie", DARK_BLUE),
        ("FLASH ATTENTION", NEON_GREEN, "it's literally faster", DARK_GREEN),
        ("RLHF", NEON_PINK, "teach AI to not be unhinged", DARK_PURPLE),
        ("SCALING LAWS", NEON_YELLOW, "bigger = better???", (15, 15, 5)),
        ("TOKENIZERS", NEON_ORANGE, "why 'ChatGPT' is 3 tokens", DARK_RED),
        ("GPU GO BRRR", HOT_RED, "memory go zoom zoom", DARK_RED),
        ("GRPO / RLVR", ELECTRIC_PURPLE, "bleeding edge RL", DARK_PURPLE),
        ("AGENTS", NEON_GREEN, "AI with a to-do list", DARK_GREEN),
        ("SAFETY", NEON_BLUE, "keeping skynet chill", DARK_BLUE),
    ]

    topic_duration = 0.77  # ~0.77s per topic for 9 topics in 7s
    idx = min(int(t / topic_duration), len(topics) - 1)
    topic, color, subtitle, bg_color = topics[idx]
    local_t = t - idx * topic_duration

    # Alternating background styles
    if idx % 3 == 0:
        img = bg_gradient_radial(tuple(min(60, c) for c in color), bg_color, radius=0.7)
    elif idx % 3 == 1:
        img = bg_diagonal_stripes(bg_color, tuple(c // 8 for c in color),
                                  stripe_width=60, angle_offset=int(t * 80))
    else:
        img = bg_gradient_radial(tuple(min(80, c) for c in color), bg_color, radius=0.6)

    draw = ImageDraw.Draw(img)

    # Flash on transition
    if local_t < 0.06:
        flash = 1.0 - local_t / 0.06
        pixels = np.array(img).astype(np.float32)
        for c_idx in range(3):
            pixels[:, :, c_idx] += flash * color[c_idx] * 0.8
        img = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
        draw = ImageDraw.Draw(img)

    # Topic text with scale-in
    scale_progress = min(1.0, local_t / 0.12)
    scale = ease_out_back(scale_progress)
    font_size = max(10, int(85 * scale))
    font_topic = load_font(FONT_BOLD, font_size)
    font_sub = load_font(FONT_REGULAR, 42)

    # Shake on appear
    shake_x = int(12 * math.sin(local_t * 40) * max(0, 1 - local_t * 5))
    shake_y = int(8 * math.cos(local_t * 35) * max(0, 1 - local_t * 5))

    draw_glow_text(draw, topic, WIDTH // 2 + shake_x,
                   HEIGHT // 2 - 60 + shake_y, font_topic, color, glow=6)

    if local_t > 0.15:
        sub_alpha = min(1.0, (local_t - 0.15) / 0.15)
        sub_color = tuple(int(255 * sub_alpha) for _ in range(3))
        draw_text_xy(draw, f"({subtitle})", WIDTH // 2,
                     HEIGHT // 2 + 80, font_sub, sub_color,
                     stroke_width=2, stroke_fill=BLACK)

    # Progress bar at bottom
    total_w = WIDTH - 160
    filled_w = int(total_w * (idx + local_t / topic_duration) / len(topics))
    draw.rectangle([80, 1720, 80 + total_w, 1740], fill=(40, 40, 40))
    draw.rectangle([80, 1720, 80 + filled_w, 1740], fill=color)

    # Counter
    font_counter = load_font(FONT_MONO, 30)
    draw_text_xy(draw, f"{idx + 1}/{len(topics)}", WIDTH // 2, 1770,
                 font_counter, WHITE)

    result = np.array(img)
    apply_scanlines(result, 18)
    return result


def scene_fire(t):
    """'THIS COURSE IS GONNA BE FIRE' with dramatic buildup."""
    # Background: warm radial gradient
    pulse = beat_intensity(t)
    img = bg_gradient_radial((40 + int(pulse * 60), 5, 0), (10, 0, 0), radius=0.6)
    draw = ImageDraw.Draw(img)

    font_big = load_font(FONT_BOLD, 90)

    draw_glow_text(draw, "THIS COURSE", WIDTH // 2, 680, font_big, WHITE, glow=4)
    draw_glow_text(draw, "IS GONNA BE", WIDTH // 2, 830, font_big, WHITE, glow=4)

    if t > 0.5:
        # "FIRE" slams in huge with elastic bounce
        fire_t = t - 0.5
        progress = min(1.0, fire_t / 0.2)
        scale = ease_out_elastic(progress)
        font_size = max(10, int(200 * scale))
        font_fire = load_font(FONT_BOLD, font_size)

        # Screen shake on impact
        shake_x = int(20 * math.sin(fire_t * 50) * max(0, 1 - fire_t * 2))
        shake_y = int(15 * math.cos(fire_t * 45) * max(0, 1 - fire_t * 2))

        draw_glow_text(draw, "FIRE", WIDTH // 2 + shake_x,
                       1060 + shake_y, font_fire, HOT_RED, glow=12)

        # Chromatic aberration on slam
        if fire_t < 0.3:
            img = apply_chromatic_aberration(img, int(20 * (1 - fire_t / 0.3)))
            draw = ImageDraw.Draw(img)

    if t > 1.2:
        font_med = load_font(FONT_REGULAR, 55)
        alpha = min(1.0, (t - 1.2) / 0.2)
        c = tuple(int(v * alpha) for v in NEON_YELLOW)
        draw_text_xy(draw, "no cap fr fr", WIDTH // 2, 1280, font_med, c,
                     stroke_width=2, stroke_fill=BLACK)

    result = np.array(img)
    apply_scanlines(result, 20)
    result = apply_vignette(result, 0.5)

    # Zoom pulse on beat
    if pulse > 0.4:
        img2 = Image.fromarray(result)
        img2 = apply_zoom(img2, 1.0 + pulse * 0.04)
        result = np.array(img2)

    return result


def scene_code_terminal(t):
    """Terminal with code being typed — with beat-synced cursor flash."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (12, 12, 22))
    draw = ImageDraw.Draw(img)

    pulse = beat_intensity(t)

    # Subtle bg glow behind terminal
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    dist = np.sqrt((X - WIDTH / 2) ** 2 + (Y - HEIGHT * 0.45) ** 2) / 600
    glow_pixels = np.array(img).astype(np.float32)
    glow_pixels[:, :, 1] += np.clip(15 / (dist + 0.5), 0, 30)
    img = Image.fromarray(np.clip(glow_pixels, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(img)

    # Terminal window
    term_top, term_bot = 180, HEIGHT - 180
    draw.rounded_rectangle([40, term_top, WIDTH - 40, term_bot],
                           radius=15, fill=(22, 22, 38), outline=(50, 50, 70), width=2)
    # Title bar
    draw.rectangle([40, term_top, WIDTH - 40, term_top + 50], fill=(35, 35, 50))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([65 + i * 32, term_top + 15, 82 + i * 32, term_top + 32], fill=c)
    font_title = load_font(FONT_MONO, 22)
    draw_text_xy(draw, "train_llm_reasoner.py", WIDTH // 2, term_top + 25,
                 font_title, (160, 160, 180))

    code_lines = [
        ("import", " torch", NEON_BLUE, NEON_GREEN),
        ("from", " transformers ", NEON_BLUE, NEON_GREEN),
        ("import", " AutoModelForCausalLM", NEON_BLUE, NEON_YELLOW),
        ("", "", None, None),
        ("# Fine-tune with GRPO", "", (90, 90, 110), None),
        ("model", " = load_reasoner(", NEON_PINK, WHITE),
        ("    ", '"meta-llama/Llama-3"', WHITE, NEON_YELLOW),
        (")", "", WHITE, None),
        ("", "", None, None),
        ("optimizer", " = torch.optim.AdamW(", NEON_PINK, WHITE),
        ("    ", "model.parameters(),", WHITE, NEON_ORANGE),
        ("    ", "lr=2e-5", WHITE, NEON_GREEN),
        (")", "", WHITE, None),
        ("", "", None, None),
        ("# Reinforcement learning", "", (90, 90, 110), None),
        ("rewards", " = grpo_step(model,", NEON_PINK, WHITE),
        ("    ", "prompts, responses)", WHITE, NEON_ORANGE),
        ("loss", ".backward()", NEON_PINK, NEON_YELLOW),
        ("optimizer", ".step()", NEON_PINK, NEON_YELLOW),
        ("print", '(f"reward: {r.mean():.3f}")', NEON_BLUE, NEON_GREEN),
    ]

    font_code = load_font(FONT_MONO, 30)
    chars_per_sec = 50
    total_chars = 0
    y = term_top + 75
    line_height = 40

    for kw, rest, kw_color, rest_color in code_lines:
        line_len = len(kw) + len(rest)
        if line_len == 0:
            total_chars += 1
            y += line_height
            continue
        chars_visible = int(t * chars_per_sec) - total_chars
        if chars_visible <= 0:
            break

        kw_show = kw[:min(len(kw), chars_visible)]
        if kw_show and kw_color:
            draw.text((65, y), kw_show, font=font_code, fill=kw_color)

        rest_chars = max(0, chars_visible - len(kw))
        rest_show = rest[:rest_chars]
        if rest_show and rest_color:
            kw_bbox = draw.textbbox((0, 0), kw, font=font_code)
            draw.text((65 + kw_bbox[2] - kw_bbox[0], y), rest_show,
                      font=font_code, fill=rest_color)

        # Blinking cursor synced to beat
        shown = kw_show + rest_show
        if shown and chars_visible <= line_len + 3:
            cursor_bbox = draw.textbbox((0, 0), shown, font=font_code)
            cursor_x = 65 + cursor_bbox[2] - cursor_bbox[0]
            # Cursor visible on beat pulses
            if int(t * 4) % 2 == 0:
                draw.rectangle([cursor_x, y, cursor_x + 14, y + 34], fill=NEON_GREEN)

        total_chars += line_len
        y += line_height

    # "HANDS-ON CODE" label
    font_label = load_font(FONT_BOLD, 52)
    draw_glow_text(draw, "HANDS-ON CODE", WIDTH // 2, 100, font_label, NEON_GREEN, glow=4)

    result = np.array(img)
    apply_scanlines(result, 12)

    # Beat zoom
    if pulse > 0.3:
        img2 = Image.fromarray(result)
        img2 = apply_zoom(img2, 1.0 + pulse * 0.02)
        result = np.array(img2)

    return result


def scene_training_viz(t):
    """Training loss curve with animated draw and beat-synced effects."""
    img = bg_moving_gradient(t, DARK_BLUE, (5, 5, 15), (0, 30, 60))
    draw = ImageDraw.Draw(img)

    font_title = load_font(FONT_BOLD, 65)
    font_label = load_font(FONT_MONO, 30)
    font_big = load_font(FONT_BOLD, 85)

    pulse = beat_intensity(t)

    draw_glow_text(draw, "TRAINING LOSS", WIDTH // 2, 480, font_title, NEON_BLUE, glow=5)

    # Axes
    ax_l, ax_r, ax_t, ax_b = 120, WIDTH - 80, 600, 1380
    draw.line([(ax_l, ax_b), (ax_r, ax_b)], fill=(100, 100, 120), width=2)
    draw.line([(ax_l, ax_t), (ax_l, ax_b)], fill=(100, 100, 120), width=2)
    draw.text((ax_r - 60, ax_b + 15), "steps", font=font_label, fill=(150, 150, 170))
    draw.text((ax_l + 10, ax_t - 35), "loss", font=font_label, fill=(150, 150, 170))

    # Animated loss curve
    num_pts = min(int(t / 4.0 * 250), 250)  # animate curve over ~4s
    if num_pts > 1:
        points = []
        for i in range(num_pts):
            frac = i / 250
            x = ax_l + int(frac * (ax_r - ax_l))
            loss = 2.8 * math.exp(-4 * frac) + 0.12
            noise = 0.1 * math.sin(i * 0.7) * math.exp(-2.5 * frac)
            loss += noise
            y_val = ax_t + int((1 - (loss - 0.05) / 3.0) * (ax_b - ax_t))
            y_val = max(ax_t, min(ax_b, y_val))
            points.append((x, y_val))

        # Draw curve with gradient color (green at end, blue at start)
        for i in range(len(points) - 1):
            frac = i / max(len(points) - 1, 1)
            r = int(lerp(0, 57, frac))
            g = int(lerp(200, 255, frac))
            b = int(lerp(255, 20, frac))
            draw.line([points[i], points[i + 1]], fill=(r, g, b), width=3)

        # Trailing dot
        lx, ly = points[-1]
        dot_size = int(6 + pulse * 6)
        draw.ellipse([lx - dot_size, ly - dot_size, lx + dot_size, ly + dot_size],
                     fill=NEON_YELLOW)
        curr_loss = 2.8 * math.exp(-4 * (num_pts / 250)) + 0.12
        draw.text((lx + 15, ly - 20), f"{curr_loss:.3f}",
                  font=font_label, fill=NEON_YELLOW)

    # Meme text
    if t > 2.2:
        progress = min(1.0, (t - 2.2) / 0.15)
        scale = ease_out_back(progress)
        fsize = max(10, int(85 * scale))
        font_meme = load_font(FONT_BOLD, fsize)
        draw_glow_text(draw, "LOSS GO DOWN", WIDTH // 2, 1520, font_meme, NEON_GREEN, glow=6)
    if t > 2.7:
        draw_text_xy(draw, "(that's the whole goal)", WIDTH // 2, 1640,
                     font_label, NEON_YELLOW, stroke_width=1, stroke_fill=BLACK)

    result = np.array(img)
    apply_scanlines(result, 12)
    result = apply_vignette(result, 0.4)
    return result


def scene_what_youll_build(t):
    """Build list with animated entries."""
    img = bg_gradient_radial((15, 40, 15), DARK_GREEN, radius=0.9)
    draw = ImageDraw.Draw(img)

    pulse = beat_intensity(t)

    font_title = load_font(FONT_BOLD, 80)
    font_item = load_font(FONT_BOLD, 52)

    # Title with scale
    if t < 0.5:
        progress = min(1.0, t / 0.2)
        scale = ease_out_back(progress)
        fsize = max(10, int(80 * scale))
        ft = load_font(FONT_BOLD, fsize)
    else:
        ft = font_title
    draw_glow_text(draw, "YOU WILL", WIDTH // 2, 480, ft, NEON_GREEN, glow=5)
    draw_glow_text(draw, "ACTUALLY BUILD", WIDTH // 2, 600, ft, NEON_GREEN, glow=5)

    items = [
        ("Fine-tune LLMs", 0.5, NEON_BLUE),
        ("Train with RLHF", 0.9, NEON_PINK),
        ("Implement FlashAttention", 1.3, NEON_YELLOW),
        ("Deploy reasoning agents", 1.7, NEON_ORANGE),
        ("Final project (your choice)", 2.1, ELECTRIC_PURPLE),
    ]

    y = 780
    for text, threshold, color in items:
        if t > threshold:
            progress = min(1.0, (t - threshold) / 0.2)
            # Slide from right with ease
            offset_x = int((1 - ease_out_back(progress)) * 500)
            alpha = min(1.0, progress * 2)
            c = tuple(int(v * alpha) for v in color)
            # Chevron
            draw_text_xy(draw, f"> {text}", WIDTH // 2 + offset_x, y,
                         font_item, c, stroke_width=2, stroke_fill=BLACK)
        y += 95

    result = np.array(img)
    apply_scanlines(result, 15)
    result = apply_vignette(result, 0.4)
    return result


def scene_schedule(t):
    """Schedule with moving bg."""
    img = bg_moving_gradient(t, (5, 5, 25), (15, 5, 20), (0, 20, 60))
    draw = ImageDraw.Draw(img)

    pulse = beat_intensity(t)

    font_label = load_font(FONT_MONO, 38)
    font_big = load_font(FONT_BOLD, 90)
    font_med = load_font(FONT_BOLD, 60)
    font_detail = load_font(FONT_REGULAR, 50)

    draw_text_xy(draw, "[ THE DEETS ]", WIDTH // 2, 580, font_label, NEON_GREEN,
                 stroke_width=2, stroke_fill=BLACK)

    # "FRIDAYS" with beat glow
    glow_r = int(5 + pulse * 8)
    draw_glow_text(draw, "FRIDAYS", WIDTH // 2, 760, font_big, NEON_YELLOW, glow=glow_r)

    draw_text_xy(draw, "12:30 - 2:30 PM", WIDTH // 2, 900, font_med, WHITE,
                 stroke_width=2, stroke_fill=BLACK)
    draw_text_xy(draw, "CIWW 101", WIDTH // 2, 1000, font_detail, NEON_BLUE,
                 stroke_width=2, stroke_fill=BLACK)

    if t > 0.8:
        alpha = min(1.0, (t - 0.8) / 0.3)
        c = tuple(int(v * alpha) for v in NEON_PINK)
        draw_text_xy(draw, "one day a week", WIDTH // 2, 1160, font_detail, c,
                     stroke_width=2, stroke_fill=BLACK)
    if t > 1.2:
        alpha = min(1.0, (t - 1.2) / 0.3)
        c = tuple(int(v * alpha) for v in NEON_GREEN)
        draw_text_xy(draw, "maximum learning density", WIDTH // 2, 1240,
                     font_label, c, stroke_width=2, stroke_fill=BLACK)

    result = np.array(img)
    apply_scanlines(result, 18)
    result = apply_vignette(result, 0.5)
    return result


def scene_persuade(t):
    """POV meme with dramatic red tint."""
    # Red-tinged background that gets darker
    red_amount = int(lerp(20, 50, min(1, t / 2)))
    img = bg_gradient_radial((red_amount, 0, 0), (5, 0, 0), radius=0.7)
    draw = ImageDraw.Draw(img)

    font_pov = load_font(FONT_BOLD, 100)
    font_med = load_font(FONT_BOLD, 65)
    font_big = load_font(FONT_BOLD, 90)

    lines = [
        ("POV:", NEON_GREEN, 620, 0.0, font_pov),
        ("you didn't take", WHITE, 770, 0.3, font_med),
        ("this course", WHITE, 860, 0.3, font_med),
        ("and now you're", WHITE, 1010, 0.9, font_med),
        ("STILL CONFUSED", HOT_RED, 1140, 1.2, font_big),
        ("about LLMs", WHITE, 1280, 1.6, font_med),
    ]

    for text, color, y, threshold, font in lines:
        if t > threshold:
            progress = min(1.0, (t - threshold) / 0.15)
            if text == "STILL CONFUSED":
                # Slam with shake
                scale = ease_out_elastic(progress)
                fsize = max(10, int(90 * scale))
                f = load_font(FONT_BOLD, fsize)
                shake_x = int(15 * math.sin((t - threshold) * 40) * max(0, 1 - (t - threshold) * 3))
                draw_glow_text(draw, text, WIDTH // 2 + shake_x, y, f, color, glow=8)
            else:
                alpha = min(1.0, progress * 1.5)
                c = tuple(int(v * alpha) for v in color)
                draw_glow_text(draw, text, WIDTH // 2, y, font, c, glow=4)

    result = np.array(img)
    apply_scanlines(result, 22)
    result = apply_vignette(result, 0.6)

    # Chromatic aberration when "STILL CONFUSED" hits
    if 1.2 < t < 1.6:
        img2 = Image.fromarray(result)
        img2 = apply_chromatic_aberration(img2, int(15 * (1 - (t - 1.2) / 0.4)))
        result = np.array(img2)

    return result


def scene_cta(t):
    """Call to action with energetic bg."""
    img = bg_moving_gradient(t * 1.5, (25, 5, 30), (10, 0, 15), (60, 0, 80))
    draw = ImageDraw.Draw(img)

    pulse = beat_intensity(t)

    font_big = load_font(FONT_BOLD, 100)
    font_med = load_font(FONT_BOLD, 60)
    font_url = load_font(FONT_MONO, 32)

    # "ENROLL NOW" with scale-in
    if t < 0.3:
        progress = min(1.0, t / 0.2)
        scale = ease_out_back(progress)
        fsize = max(10, int(100 * scale))
        fb = load_font(FONT_BOLD, fsize)
    else:
        fb = font_big

    glow_r = int(6 + pulse * 6)
    draw_glow_text(draw, "ENROLL", WIDTH // 2, 700, fb, NEON_GREEN, glow=glow_r)
    draw_glow_text(draw, "NOW", WIDTH // 2, 840, fb, NEON_GREEN, glow=glow_r)

    if t > 0.6:
        draw_text_xy(draw, "CSCI-GA.3033-131", WIDTH // 2, 1000,
                     font_med, NEON_YELLOW, stroke_width=2, stroke_fill=BLACK)
    if t > 1.0:
        draw_text_xy(draw, "DS-GA.3001-009", WIDTH // 2, 1080,
                     font_med, NEON_BLUE, stroke_width=2, stroke_fill=BLACK)
    if t > 1.4:
        draw_text_xy(draw, "gregdurrett.github.io", WIDTH // 2, 1220,
                     font_url, WHITE, stroke_width=2, stroke_fill=BLACK)

    # Animated border
    border_phase = t * 4
    for i in range(5):
        offset = 12 + i * 6
        hue_shift = (border_phase + i * 0.3) % 1.0
        r = int(128 + 127 * math.sin(hue_shift * 2 * math.pi))
        g = int(128 + 127 * math.sin(hue_shift * 2 * math.pi + 2.094))
        b = int(128 + 127 * math.sin(hue_shift * 2 * math.pi + 4.189))
        draw.rectangle([offset, offset, WIDTH - offset, HEIGHT - offset],
                       outline=(r, g, b), width=2)

    result = np.array(img)
    apply_scanlines(result, 15)
    result = apply_vignette(result, 0.35)
    return result


def scene_outro(t):
    """LFG finale with particle explosion effect."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    pulse = beat_intensity(t)

    # Particle explosion from center
    random.seed(123)
    if t > 0.1:
        num_particles = min(int((t - 0.1) * 200), 300)
        for i in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 800)
            lifetime = random.uniform(0.5, 2.5)
            age = t - 0.1
            if age > lifetime:
                continue
            dist = speed * age * 0.8
            px = int(WIDTH / 2 + math.cos(angle) * dist)
            py = int(HEIGHT / 2 + math.sin(angle) * dist)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                fade = 1.0 - age / lifetime
                size = int(random.uniform(2, 8) * fade)
                c = random.choice([NEON_GREEN, NEON_BLUE, NEON_PINK, NEON_YELLOW])
                fc = tuple(int(v * fade) for v in c)
                draw.ellipse([px - size, py - size, px + size, py + size], fill=fc)

    font_huge = load_font(FONT_BOLD, 160)
    font_med = load_font(FONT_REGULAR, 55)

    if t < 1.2:
        # LFG with shake and glow
        shake = int(10 * math.sin(t * 50) * max(0, 1 - t))
        glow_r = int(10 + pulse * 8)
        draw_glow_text(draw, "LFG", WIDTH // 2 + shake, HEIGHT // 2,
                       font_huge, NEON_GREEN, glow=glow_r)
    else:
        draw_glow_text(draw, "LFG", WIDTH // 2, HEIGHT // 2 - 120,
                       font_huge, NEON_GREEN, glow=10)
        alpha = min(1.0, (t - 1.2) / 0.3)
        c = tuple(int(255 * alpha) for _ in range(3))
        draw_text_xy(draw, "see you in class", WIDTH // 2, HEIGHT // 2 + 60,
                     font_med, c, stroke_width=2, stroke_fill=BLACK)
        cy = tuple(int(v * alpha) for v in NEON_YELLOW)
        draw_text_xy(draw, "spring 2026", WIDTH // 2, HEIGHT // 2 + 140,
                     font_med, cy, stroke_width=2, stroke_fill=BLACK)

    # Fade to black
    result = np.array(img)
    if t > 2.0:
        fade = min(1.0, (t - 2.0) / 0.5)
        result = (result.astype(np.float32) * (1 - fade)).astype(np.uint8)

    apply_scanlines(result, 15)
    return result


# ── Scene timeline ──────────────────────────────────────────────────────────

SCENES = [
    (scene_intro, 4.0),         # was 3.0 — more time on "YO." / "YOU NEED THIS COURSE"
    (scene_course_name, 4.0),   # was 3.0 — let the title breathe
    (scene_instructor, 3.5),    # was 2.5 — read the subtitles
    (scene_topics_scroll, 7.0), # was 5.0 — 9 topics at ~0.78s each
    (scene_fire, 3.0),          # was 2.0 — let "FIRE" and "no cap" land
    (scene_code_terminal, 5.0), # was 4.0 — watch the code type
    (scene_training_viz, 4.5),  # was 3.5 — watch the curve animate
    (scene_what_youll_build, 4.5),  # was 3.5 — 5 items need time
    (scene_schedule, 3.5),      # was 2.5 — read the details
    (scene_persuade, 3.5),      # was 2.5 — let the meme land
    (scene_cta, 4.0),           # was 3.0 — register info needs reading time
    (scene_outro, 3.0),         # was 2.5 — fade out properly
]

TOTAL_DURATION = sum(d for _, d in SCENES)

# Precompute scene starts for audio SFX
SCENE_STARTS = []
_t = 0
for _, dur in SCENES:
    SCENE_STARTS.append(_t)
    _t += dur


def make_frame(t_global):
    """Route to correct scene."""
    elapsed = 0
    for scene_fn, duration in SCENES:
        if t_global < elapsed + duration:
            return scene_fn(t_global - elapsed)
        elapsed += duration
    return np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)


# ── Audio: CC0 music + real SFX ─────────────────────────────────────────────

import os
from moviepy import AudioFileClip, CompositeAudioClip

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")


def build_audio_track():
    """
    Build final audio by layering:
    1. CC0 background music track (trimmed to video duration, faded)
    2. Whoosh SFX at each scene transition
    3. Explosion/impact SFX at key dramatic moments
    All audio files are CC0 licensed from OpenGameArt.org.
    """
    print("Building audio track from CC0 files...")

    # ── Background music ──
    # Try multiple tracks in preference order
    music_candidates = [
        "dance_field.mp3",      # 54.9s electronic beat
        "montage.mp3",          # 44.6s
        "city_loop.mp3",        # 56.4s
        "empacotatron_loop.ogg",  # 80s electronic
    ]
    music_clip = None
    for candidate in music_candidates:
        path = os.path.join(AUDIO_DIR, candidate)
        if os.path.exists(path):
            print(f"  Using music: {candidate}")
            music_clip = AudioFileClip(path)
            break

    if music_clip is None:
        raise FileNotFoundError(f"No music files found in {AUDIO_DIR}")

    # Trim to video duration, add fade in/out
    music_clip = music_clip.subclipped(0, min(music_clip.duration, TOTAL_DURATION))
    if music_clip.duration < TOTAL_DURATION:
        # Loop if needed (shouldn't happen with our 37s video and 44-80s tracks)
        music_clip = music_clip.with_effects([])  # keep as is
    music_clip = music_clip.with_effects([
        # moviepy v2 fade effects
    ])
    # Apply fade via volume: ramp up first 1s, ramp down last 1.5s
    def music_volume(t):
        t = np.asarray(t, dtype=np.float64)
        vol = np.ones_like(t)
        # Fade in over 0.8s
        fade_in = t < 0.8
        vol = np.where(fade_in, t / 0.8, vol)
        # Fade out over last 1.5s
        fade_out_start = TOTAL_DURATION - 1.5
        fade_out = t > fade_out_start
        vol = np.where(fade_out, 1.0 - (t - fade_out_start) / 1.5, vol)
        return vol
    music_clip = music_clip.with_volume_scaled(0.75)  # music at 75% to leave room for SFX

    layers = [music_clip]

    # ── Whoosh SFX at scene transitions ──
    whoosh_path = os.path.join(AUDIO_DIR, "whoosh.wav")
    if os.path.exists(whoosh_path):
        print(f"  Adding whoosh SFX at {len(SCENE_STARTS)-1} transitions")
        whoosh_base = AudioFileClip(whoosh_path)
        # Trim whoosh to 0.5s and lower volume
        whoosh_dur = min(0.5, whoosh_base.duration)
        whoosh_trimmed = whoosh_base.subclipped(0, whoosh_dur).with_volume_scaled(0.6)
        for sc_t in SCENE_STARTS[1:]:  # skip first scene
            start = max(0, sc_t - 0.15)
            layers.append(whoosh_trimmed.with_start(start))

    # ── Explosion SFX at dramatic moments ──
    # "FIRE" slam, "STILL CONFUSED" slam, "LFG" finale
    explosion_candidates = ["explosion_synth.flac", "explosion.wav", "explosion_chunky.mp3"]
    explosion_clip = None
    for candidate in explosion_candidates:
        path = os.path.join(AUDIO_DIR, candidate)
        if os.path.exists(path):
            explosion_clip = AudioFileClip(path)
            print(f"  Using explosion SFX: {candidate}")
            break

    if explosion_clip:
        explosion_short = explosion_clip.subclipped(0, min(1.0, explosion_clip.duration))
        explosion_short = explosion_short.with_volume_scaled(0.8)

        # Find scene start times for dramatic moments
        scene_times = {}
        elapsed = 0
        for (fn, dur) in SCENES:
            scene_times[fn.__name__] = elapsed
            elapsed += dur

        # Explosion at "FIRE" text slam (0.5s into scene_fire)
        if "scene_fire" in scene_times:
            t_fire = scene_times["scene_fire"] + 0.5
            layers.append(explosion_short.with_start(t_fire))
            print(f"    Explosion at FIRE: {t_fire:.1f}s")

        # Explosion at "STILL CONFUSED" (1.2s into scene_persuade)
        if "scene_persuade" in scene_times:
            t_confused = scene_times["scene_persuade"] + 1.2
            layers.append(explosion_short.with_start(t_confused))
            print(f"    Explosion at STILL CONFUSED: {t_confused:.1f}s")

        # Explosion at "LFG" (start of outro)
        if "scene_outro" in scene_times:
            t_lfg = scene_times["scene_outro"] + 0.1
            layers.append(explosion_short.with_start(t_lfg))
            print(f"    Explosion at LFG: {t_lfg:.1f}s")

    # ── Compose all layers ──
    print(f"  Compositing {len(layers)} audio layers...")
    final_audio = CompositeAudioClip(layers)
    return final_audio


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"Generating {TOTAL_DURATION:.1f}s promo video at {WIDTH}x{HEIGHT} @ {FPS}fps")
    print(f"Scenes: {len(SCENES)}")

    video = VideoClip(make_frame, duration=TOTAL_DURATION)
    video = video.with_fps(FPS)

    audio = build_audio_track()
    video = video.with_audio(audio)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "promo_video.mp4")
    print(f"Rendering to {output_path}...")
    video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="6000k",
        preset="medium",
        logger="bar",
    )
    print(f"Done! Video saved to {output_path}")


if __name__ == "__main__":
    main()
