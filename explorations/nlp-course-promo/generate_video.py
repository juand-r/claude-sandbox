#!/usr/bin/env python3
"""
Generate a meme-style promo video for Greg Durrett's
"Building LLM Reasoners" course at NYU, Spring 2026.

Style: Gen Z / TikTok energy, kinetic typography, bold neon-on-dark,
glitch effects, rapid cuts, meme text.
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import VideoClip, AudioClip, concatenate_videoclips

# ── Config ──────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1080, 1920  # Vertical (9:16) for YouTube Shorts / TikTok
FPS = 30

# Colors (neon cyberpunk palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 16, 240)
NEON_BLUE = (0, 200, 255)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
ELECTRIC_PURPLE = (191, 0, 255)
HOT_RED = (255, 36, 0)

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_text_centered(draw, text, y, font, fill=WHITE, stroke_width=0,
                       stroke_fill=BLACK):
    """Draw text horizontally centered at given y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)


def draw_text_centered_xy(draw, text, cx, cy, font, fill=WHITE,
                          stroke_width=0, stroke_fill=BLACK):
    """Draw text centered at (cx, cy)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = cx - tw // 2
    y = cy - th // 2
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)


def add_scanlines(img, alpha=30):
    """Add CRT scanline effect."""
    pixels = np.array(img)
    for y in range(0, HEIGHT, 3):
        pixels[y, :] = np.clip(pixels[y, :].astype(int) - alpha, 0, 255)
    return Image.fromarray(pixels.astype(np.uint8))


def add_noise(img, amount=15):
    """Add subtle noise grain."""
    pixels = np.array(img).astype(np.int16)
    noise = np.random.randint(-amount, amount + 1, pixels.shape, dtype=np.int16)
    pixels = np.clip(pixels + noise, 0, 255)
    return Image.fromarray(pixels.astype(np.uint8))


def add_vignette(img, strength=0.6):
    """Add dark vignette around edges."""
    pixels = np.array(img).astype(np.float32)
    cy, cx = HEIGHT / 2, WIDTH / 2
    max_dist = math.sqrt(cx**2 + cy**2)
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2) / max_dist
    vignette = 1.0 - strength * dist**2
    vignette = np.clip(vignette, 0, 1)
    pixels *= vignette[:, :, np.newaxis]
    return Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))


def glitch_offset(img, t, intensity=20):
    """RGB channel offset glitch."""
    pixels = np.array(img)
    offset = int(intensity * math.sin(t * 15))
    r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
    r = np.roll(r, offset, axis=1)
    b = np.roll(b, -offset, axis=1)
    return Image.fromarray(np.stack([r, g, b], axis=2))


def draw_grid_bg(draw, color, alpha_factor=0.3):
    """Draw a subtle grid background."""
    grid_color = tuple(int(c * alpha_factor) for c in color)
    for x in range(0, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)


def draw_particles(draw, t, count=30, color=NEON_GREEN):
    """Draw floating particles."""
    random.seed(42)  # Deterministic for consistency
    for i in range(count):
        base_x = random.randint(0, WIDTH)
        base_y = random.randint(0, HEIGHT)
        speed = random.uniform(0.5, 2.0)
        x = (base_x + int(t * speed * 60)) % WIDTH
        y = (base_y - int(t * speed * 40)) % HEIGHT
        size = random.randint(2, 6)
        alpha = random.uniform(0.3, 1.0)
        c = tuple(int(v * alpha) for v in color)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=c)


def draw_glowing_text(draw, text, cx, cy, font, color, glow_radius=4):
    """Draw text with a glow effect."""
    # Draw glow layers
    for offset in range(glow_radius, 0, -1):
        alpha = 0.15
        glow_color = tuple(int(c * alpha) for c in color)
        for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset)]:
            draw_text_centered_xy(draw, text, cx + dx, cy + dy, font,
                                  fill=glow_color)
    # Main text
    draw_text_centered_xy(draw, text, cx, cy, font, fill=color,
                          stroke_width=3, stroke_fill=BLACK)


# ── Scene Definitions ───────────────────────────────────────────────────────

def scene_intro(t):
    """SCENE 1: Dark screen, glitch in the title. 'YO.' then 'YOU NEED THIS COURSE.'"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, NEON_GREEN)
    draw_particles(draw, t, color=NEON_GREEN)

    if t < 0.5:
        # Flash white
        flash = int(255 * max(0, 1 - t * 4))
        img = Image.new("RGB", (WIDTH, HEIGHT), (flash, flash, flash))
        draw = ImageDraw.Draw(img)
    elif t < 1.5:
        font = load_font(FONT_BOLD, 160)
        draw_glowing_text(draw, "YO.", WIDTH // 2, HEIGHT // 2, font, NEON_GREEN)
    elif t < 2.0:
        # Glitch transition
        font = load_font(FONT_BOLD, 160)
        draw_glowing_text(draw, "YO.", WIDTH // 2, HEIGHT // 2, font, NEON_GREEN)
        img = glitch_offset(img, t, intensity=40)
    else:
        font = load_font(FONT_BOLD, 90)
        draw_glowing_text(draw, "YOU NEED", WIDTH // 2, HEIGHT // 2 - 80,
                          font, NEON_PINK)
        draw_glowing_text(draw, "THIS COURSE.", WIDTH // 2, HEIGHT // 2 + 80,
                          font, NEON_PINK)

    img = add_scanlines(img)
    img = add_noise(img)
    return np.array(img)


def scene_course_name(t):
    """SCENE 2: Course name reveal with dramatic zoom feel."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, NEON_BLUE)
    draw_particles(draw, t, color=NEON_BLUE)

    # Pulsing background accent
    pulse = int(20 * abs(math.sin(t * 3)))
    draw.rectangle([40, 600, WIDTH - 40, 1320], outline=NEON_BLUE, width=3 + pulse // 10)

    font_big = load_font(FONT_BOLD, 100)
    font_med = load_font(FONT_BOLD, 70)
    font_small = load_font(FONT_REGULAR, 50)

    # Staggered reveal
    if t > 0.2:
        draw_glowing_text(draw, "BUILDING", WIDTH // 2, 750, font_big, NEON_BLUE)
    if t > 0.6:
        draw_glowing_text(draw, "LLM", WIDTH // 2, 900, font_big, NEON_YELLOW)
    if t > 1.0:
        draw_glowing_text(draw, "REASONERS", WIDTH // 2, 1050, font_big, HOT_RED)
    if t > 1.6:
        draw_glowing_text(draw, "NYU // Spring 2026", WIDTH // 2, 1220,
                          font_small, WHITE)

    # Top decoration
    font_label = load_font(FONT_MONO, 36)
    draw_text_centered_xy(draw, "[ NEW COURSE ALERT ]", WIDTH // 2, 500,
                          font_label, NEON_GREEN)

    img = add_scanlines(img)
    img = add_noise(img, 10)
    img = add_vignette(img)
    return np.array(img)


def scene_instructor(t):
    """SCENE 3: Greg Durrett introduction."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, ELECTRIC_PURPLE)
    draw_particles(draw, t, 20, ELECTRIC_PURPLE)

    font_big = load_font(FONT_BOLD, 100)
    font_med = load_font(FONT_BOLD, 65)
    font_small = load_font(FONT_REGULAR, 45)
    font_label = load_font(FONT_MONO, 32)

    draw_text_centered_xy(draw, "TAUGHT BY", WIDTH // 2, 650,
                          font_label, NEON_GREEN)
    draw_glowing_text(draw, "GREG", WIDTH // 2, 800, font_big, WHITE)
    draw_glowing_text(draw, "DURRETT", WIDTH // 2, 940, font_big, NEON_PINK)

    if t > 1.0:
        draw_text_centered_xy(draw, "the meme trailer guy", WIDTH // 2, 1100,
                              font_small, NEON_YELLOW)
    if t > 1.5:
        draw_text_centered_xy(draw, "yes, THAT greg durrett", WIDTH // 2, 1180,
                              font_small, NEON_ORANGE)

    img = add_scanlines(img)
    img = add_noise(img)
    img = add_vignette(img)
    return np.array(img)


def scene_topics_scroll(t):
    """SCENE 4: Rapid-fire topics with hype text."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    topics = [
        ("TRANSFORMERS", NEON_BLUE, "not the movie"),
        ("FLASH ATTENTION", NEON_GREEN, "it's literally faster"),
        ("RLHF", NEON_PINK, "teach AI to be less unhinged"),
        ("SCALING LAWS", NEON_YELLOW, "bigger = better???"),
        ("TOKENIZERS", NEON_ORANGE, "why 'ChatGPT' is 3 tokens"),
        ("GPU GO BRRR", HOT_RED, "memory layouts & optimization"),
        ("GRPO / RLVR", ELECTRIC_PURPLE, "bleeding edge RL"),
        ("AGENTS", NEON_GREEN, "AI with a to-do list"),
        ("SAFETY", NEON_BLUE, "keeping skynet chill"),
    ]

    font_topic = load_font(FONT_BOLD, 80)
    font_sub = load_font(FONT_REGULAR, 40)

    # Calculate which topic to show based on time
    topic_duration = 0.55
    idx = min(int(t / topic_duration), len(topics) - 1)
    topic, color, subtitle = topics[idx]

    # Background flash on transition
    frac = (t / topic_duration) - int(t / topic_duration)
    if frac < 0.08:
        flash = int(180 * (1 - frac / 0.08))
        bg = tuple(int(c * flash / 255) for c in color)
        img = Image.new("RGB", (WIDTH, HEIGHT), bg)
        draw = ImageDraw.Draw(img)

    draw_grid_bg(draw, color)

    # Topic text
    draw_glowing_text(draw, topic, WIDTH // 2, HEIGHT // 2 - 50,
                      font_topic, color)
    draw_text_centered_xy(draw, f"({subtitle})", WIDTH // 2, HEIGHT // 2 + 80,
                          font_sub, WHITE)

    # Progress dots at bottom
    for i in range(len(topics)):
        x = WIDTH // 2 + (i - len(topics) // 2) * 30
        dot_color = color if i == idx else (60, 60, 60)
        draw.ellipse([x - 6, 1700, x + 6, 1712], fill=dot_color)

    img = add_scanlines(img)
    img = add_noise(img, 12)
    return np.array(img)


def scene_meme_no_cap(t):
    """SCENE 5: 'no cap' meme moment."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, NEON_PINK)
    draw_particles(draw, t, 40, NEON_PINK)

    font_huge = load_font(FONT_BOLD, 140)
    font_big = load_font(FONT_BOLD, 90)
    font_med = load_font(FONT_REGULAR, 55)

    draw_glowing_text(draw, "THIS COURSE", WIDTH // 2, 700, font_big, WHITE)
    draw_glowing_text(draw, "IS GONNA BE", WIDTH // 2, 840, font_big, WHITE)

    if t > 0.6:
        # Shake effect
        shake_x = int(8 * math.sin(t * 30))
        shake_y = int(5 * math.cos(t * 25))
        draw_glowing_text(draw, "FIRE", WIDTH // 2 + shake_x,
                          1050 + shake_y, font_huge, HOT_RED, glow_radius=8)

    if t > 1.2:
        draw_text_centered_xy(draw, "no cap fr fr", WIDTH // 2, 1250,
                              font_med, NEON_YELLOW)

    img = add_scanlines(img)
    img = add_noise(img)
    img = add_vignette(img)
    return np.array(img)


def scene_what_youll_build(t):
    """SCENE 6: What you'll actually build."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, NEON_GREEN)

    font_title = load_font(FONT_BOLD, 75)
    font_item = load_font(FONT_BOLD, 55)
    font_sub = load_font(FONT_REGULAR, 38)

    draw_glowing_text(draw, "YOU WILL", WIDTH // 2, 500, font_title, NEON_GREEN)
    draw_glowing_text(draw, "ACTUALLY BUILD", WIDTH // 2, 610, font_title,
                      NEON_GREEN)

    items = [
        ("Fine-tune LLMs", 0.5),
        ("Train with RLHF", 1.0),
        ("Implement FlashAttention", 1.5),
        ("Deploy reasoning agents", 2.0),
        ("Final project of your choice", 2.5),
    ]

    y = 780
    for text, threshold in items:
        if t > threshold:
            # Slide in from right
            progress = min(1.0, (t - threshold) / 0.3)
            offset_x = int((1 - progress) * 400)
            draw_text_centered_xy(draw, f"> {text}",
                                  WIDTH // 2 + offset_x, y, font_item, WHITE)
        y += 100

    img = add_scanlines(img)
    img = add_noise(img, 8)
    img = add_vignette(img)
    return np.array(img)


def scene_schedule(t):
    """SCENE 7: When & where."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, NEON_BLUE)
    draw_particles(draw, t, 15, NEON_BLUE)

    font_big = load_font(FONT_BOLD, 80)
    font_med = load_font(FONT_BOLD, 60)
    font_detail = load_font(FONT_REGULAR, 50)
    font_label = load_font(FONT_MONO, 34)

    draw_text_centered_xy(draw, "[ THE DEETS ]", WIDTH // 2, 600,
                          font_label, NEON_GREEN)

    draw_glowing_text(draw, "FRIDAYS", WIDTH // 2, 780, font_big, NEON_YELLOW)
    draw_text_centered_xy(draw, "12:30 - 2:30 PM", WIDTH // 2, 900,
                          font_med, WHITE)
    draw_text_centered_xy(draw, "CIWW 101", WIDTH // 2, 1000,
                          font_detail, NEON_BLUE)

    if t > 1.0:
        draw_text_centered_xy(draw, "only one day a week", WIDTH // 2, 1150,
                              font_detail, NEON_PINK)
        draw_text_centered_xy(draw, "maximum learning density", WIDTH // 2, 1220,
                              font_label, NEON_GREEN)

    img = add_scanlines(img)
    img = add_noise(img)
    img = add_vignette(img)
    return np.array(img)


def scene_persuade(t):
    """SCENE 8: The hard sell / meme persuasion."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, HOT_RED)

    font_big = load_font(FONT_BOLD, 85)
    font_med = load_font(FONT_BOLD, 60)
    font_small = load_font(FONT_REGULAR, 45)

    lines = [
        ("POV:", NEON_GREEN, 650, 0.0),
        ("you didn't take", WHITE, 780, 0.4),
        ("this course", WHITE, 870, 0.4),
        ("and now you're", WHITE, 1010, 1.0),
        ("STILL CONFUSED", HOT_RED, 1120, 1.0),
        ("about LLMs", WHITE, 1230, 1.5),
    ]

    for text, color, y, threshold in lines:
        if t > threshold:
            font = font_big if text in ("STILL CONFUSED", "POV:") else font_med
            draw_glowing_text(draw, text, WIDTH // 2, y, font, color)

    img = add_scanlines(img)
    img = add_noise(img)
    img = add_vignette(img)
    return np.array(img)


def scene_code_terminal(t):
    """SCENE: Fake terminal showing LLM code being typed."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 15, 25))
    draw = ImageDraw.Draw(img)

    # Terminal chrome
    draw.rectangle([30, 200, WIDTH - 30, HEIGHT - 200], fill=(25, 25, 40),
                   outline=(60, 60, 80), width=2)
    # Title bar
    draw.rectangle([30, 200, WIDTH - 30, 260], fill=(40, 40, 55))
    # Traffic light dots
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([60 + i * 35, 218, 80 + i * 35, 238], fill=c)
    font_title = load_font(FONT_MONO, 24)
    draw_text_centered_xy(draw, "train_llm_reasoner.py", WIDTH // 2, 230,
                          font_title, (180, 180, 200))

    # Code lines that appear over time
    code_lines = [
        ("import", " torch", NEON_BLUE, NEON_GREEN),
        ("from", " transformers ", NEON_BLUE, NEON_GREEN),
        ("import", " AutoModelForCausalLM", NEON_BLUE, NEON_YELLOW),
        ("", "", None, None),  # blank
        ("# Fine-tune with GRPO", "", (100, 100, 120), None),
        ("model", " = load_reasoner(", NEON_PINK, WHITE),
        ("    ", '"meta-llama/Llama-3"', WHITE, NEON_YELLOW),
        (")", "", WHITE, None),
        ("", "", None, None),
        ("optimizer", " = torch.optim.AdamW(", NEON_PINK, WHITE),
        ("    ", "model.parameters(),", WHITE, NEON_ORANGE),
        ("    ", "lr=2e-5", WHITE, NEON_GREEN),
        (")", "", WHITE, None),
        ("", "", None, None),
        ("# Train reasoning with RL", "", (100, 100, 120), None),
        ("rewards", " = grpo_step(model,", NEON_PINK, WHITE),
        ("    ", "prompts, responses)", WHITE, NEON_ORANGE),
        ("loss", ".backward()", NEON_PINK, NEON_YELLOW),
        ("print", '(f"reward: {rewards.mean():.3f}")', NEON_BLUE, NEON_GREEN),
    ]

    font_code = load_font(FONT_MONO, 32)
    chars_per_sec = 40
    total_chars = 0
    y = 290

    for kw, rest, kw_color, rest_color in code_lines:
        line_len = len(kw) + len(rest)
        chars_visible = int(t * chars_per_sec) - total_chars
        if chars_visible <= 0:
            break
        # Draw keyword part
        kw_show = kw[:min(len(kw), chars_visible)]
        if kw_show and kw_color:
            draw.text((60, y), kw_show, font=font_code, fill=kw_color)
        # Draw rest part
        rest_start = max(0, chars_visible - len(kw))
        rest_show = rest[:rest_start]
        if rest_show and rest_color:
            kw_bbox = draw.textbbox((0, 0), kw, font=font_code)
            kw_w = kw_bbox[2] - kw_bbox[0]
            draw.text((60 + kw_w, y), rest_show, font=font_code, fill=rest_color)
        # Cursor
        shown = kw_show + rest_show
        cursor_bbox = draw.textbbox((0, 0), shown, font=font_code) if shown else (0, 0, 0, 0)
        cursor_x = 60 + (cursor_bbox[2] - cursor_bbox[0] if shown else 0)
        if int(t * 3) % 2 == 0 and chars_visible < line_len + 5:
            draw.rectangle([cursor_x, y, cursor_x + 16, y + 36], fill=NEON_GREEN)

        total_chars += line_len
        y += 44

    # Label at top
    font_label = load_font(FONT_BOLD, 50)
    draw_text_centered_xy(draw, "HANDS-ON CODE", WIDTH // 2, 120,
                          font_label, NEON_GREEN)

    img = add_scanlines(img, 15)
    img = add_noise(img, 5)
    return np.array(img)


def scene_training_viz(t):
    """SCENE: Fake training loss curve going down."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw, NEON_BLUE)

    font_title = load_font(FONT_BOLD, 60)
    font_label = load_font(FONT_MONO, 30)
    font_big = load_font(FONT_BOLD, 80)

    draw_glowing_text(draw, "TRAINING LOSS", WIDTH // 2, 500, font_title, NEON_BLUE)

    # Draw axes
    ax_left, ax_right = 120, WIDTH - 80
    ax_top, ax_bottom = 620, 1400
    draw.line([(ax_left, ax_bottom), (ax_right, ax_bottom)], fill=WHITE, width=2)
    draw.line([(ax_left, ax_top), (ax_left, ax_bottom)], fill=WHITE, width=2)

    # Axis labels
    draw.text((ax_right - 60, ax_bottom + 10), "steps", font=font_label, fill=WHITE)
    draw.text((ax_left - 30, ax_top - 40), "loss", font=font_label, fill=WHITE)

    # Loss curve (animated — more points revealed over time)
    num_points = int(t / 3.5 * 200)
    num_points = min(num_points, 200)
    if num_points > 1:
        points = []
        for i in range(num_points):
            frac = i / 200
            x = ax_left + int(frac * (ax_right - ax_left))
            # Exponential decay with noise
            loss = 2.5 * math.exp(-3 * frac) + 0.15
            noise = 0.08 * math.sin(i * 0.7) * math.exp(-2 * frac)
            loss += noise
            y = ax_top + int((1 - (loss - 0.1) / 2.6) * (ax_bottom - ax_top))
            y = max(ax_top, min(ax_bottom, y))
            points.append((x, y))

        # Draw the curve
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=NEON_GREEN, width=3)

        # Current value label
        last_x, last_y = points[-1]
        draw.ellipse([last_x - 6, last_y - 6, last_x + 6, last_y + 6],
                     fill=NEON_YELLOW)
        current_loss = 2.5 * math.exp(-3 * (num_points / 200)) + 0.15
        draw.text((last_x + 15, last_y - 15), f"{current_loss:.3f}",
                  font=font_label, fill=NEON_YELLOW)

    # Bottom text
    if t > 2.0:
        draw_text_centered_xy(draw, "LOSS GO DOWN", WIDTH // 2, 1550,
                              font_big, NEON_GREEN)
    if t > 2.5:
        draw_text_centered_xy(draw, "(that's the goal)", WIDTH // 2, 1650,
                              font_label, NEON_YELLOW)

    img = add_scanlines(img, 15)
    img = add_noise(img, 8)
    img = add_vignette(img)
    return np.array(img)


def scene_cta(t):
    """SCENE: Call to action — register now."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    # Animated gradient background (vectorized for speed)
    phase = t * 2
    ys = np.arange(HEIGHT)
    fracs = ys / HEIGHT
    rs = (40 * np.abs(np.sin(fracs * math.pi + phase))).astype(np.uint8)
    gs = (10 * np.abs(np.sin(fracs * math.pi * 2 + phase))).astype(np.uint8)
    bs = (60 * np.abs(np.sin(fracs * math.pi * 0.5 + phase))).astype(np.uint8)
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    pixels[:, :, 0] = rs[:, np.newaxis]
    pixels[:, :, 1] = gs[:, np.newaxis]
    pixels[:, :, 2] = bs[:, np.newaxis]
    img = Image.fromarray(pixels)
    draw = ImageDraw.Draw(img)

    draw_grid_bg(draw, NEON_PINK)
    draw_particles(draw, t, 50, NEON_PINK)

    font_big = load_font(FONT_BOLD, 90)
    font_med = load_font(FONT_BOLD, 60)
    font_url = load_font(FONT_MONO, 30)

    draw_glowing_text(draw, "ENROLL", WIDTH // 2, 700, font_big, NEON_GREEN,
                      glow_radius=6)
    draw_glowing_text(draw, "NOW", WIDTH // 2, 830, font_big, NEON_GREEN,
                      glow_radius=6)

    if t > 0.8:
        draw_text_centered_xy(draw, "CSCI-GA.3033-131", WIDTH // 2, 1000,
                              font_med, NEON_YELLOW)
    if t > 1.2:
        draw_text_centered_xy(draw, "DS-GA.3001-009", WIDTH // 2, 1080,
                              font_med, NEON_BLUE)
    if t > 1.6:
        draw_text_centered_xy(draw, "gregdurrett.github.io", WIDTH // 2, 1220,
                              font_url, WHITE)

    # Pulsing border
    border_alpha = int(128 + 127 * math.sin(t * 6))
    border_color = (border_alpha, 0, border_alpha)
    for i in range(4):
        draw.rectangle([10 + i * 5, 10 + i * 5,
                        WIDTH - 10 - i * 5, HEIGHT - 10 - i * 5],
                       outline=border_color, width=2)

    img = add_scanlines(img)
    img = add_noise(img, 8)
    img = add_vignette(img, 0.4)
    return np.array(img)


def scene_outro(t):
    """SCENE 10: Final meme sign-off."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    draw_particles(draw, t, 60, NEON_GREEN)

    font_huge = load_font(FONT_BOLD, 120)
    font_med = load_font(FONT_REGULAR, 50)

    if t < 1.0:
        # Shake effect for energy
        shake = int(6 * math.sin(t * 40))
        draw_glowing_text(draw, "LFG", WIDTH // 2 + shake, HEIGHT // 2,
                          font_huge, NEON_GREEN, glow_radius=10)
    else:
        draw_glowing_text(draw, "LFG", WIDTH // 2, HEIGHT // 2 - 100,
                          font_huge, NEON_GREEN, glow_radius=10)
        draw_text_centered_xy(draw, "see you in class", WIDTH // 2,
                              HEIGHT // 2 + 80, font_med, WHITE)
        draw_text_centered_xy(draw, "spring 2026", WIDTH // 2,
                              HEIGHT // 2 + 160, font_med, NEON_YELLOW)

    # Fade to black at the end
    if t > 1.8:
        fade = min(1.0, (t - 1.8) / 0.7)
        pixels = np.array(img).astype(np.float32)
        pixels *= (1 - fade)
        img = Image.fromarray(pixels.astype(np.uint8))

    img = add_scanlines(img)
    img = add_noise(img)
    return np.array(img)


# ── Scene timeline ──────────────────────────────────────────────────────────

SCENES = [
    (scene_intro, 3.0),
    (scene_course_name, 3.0),
    (scene_instructor, 2.5),
    (scene_topics_scroll, 5.0),
    (scene_meme_no_cap, 2.0),
    (scene_code_terminal, 4.0),
    (scene_training_viz, 3.5),
    (scene_what_youll_build, 3.5),
    (scene_schedule, 2.5),
    (scene_persuade, 2.5),
    (scene_cta, 3.0),
    (scene_outro, 2.5),
]

TOTAL_DURATION = sum(d for _, d in SCENES)

# Precompute scene transition times for audio SFX
SCENE_STARTS = []
_t = 0
for _, dur in SCENES:
    SCENE_STARTS.append(_t)
    _t += dur


def make_frame(t_global):
    """Route global time to the correct scene."""
    elapsed = 0
    for scene_fn, duration in SCENES:
        if t_global < elapsed + duration:
            return scene_fn(t_global - elapsed)
        elapsed += duration
    # Fallback: black frame
    return np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)


# ── Audio: vectorized electronic beat + SFX ─────────────────────────────────

def make_audio(t):
    """Generate electronic beat soundtrack. t can be a numpy array."""
    t = np.asarray(t, dtype=np.float64)
    bpm = 130
    beat_freq = bpm / 60.0

    # Layer 1: bass kick (4 on the floor)
    beat_phase = (t * beat_freq) % 1.0
    kick_mask = beat_phase < 0.1
    kick_env = np.where(kick_mask, 1.0 - beat_phase / 0.1, 0.0)
    kick_freq = 80 * (1.0 + kick_env * 3)
    kick = 0.6 * kick_env * np.sin(2 * np.pi * kick_freq * t)

    # Layer 2: hi-hat on off-beats
    hihat_phase = (t * beat_freq * 2) % 1.0
    hihat_mask = hihat_phase < 0.04
    hihat_env = np.where(hihat_mask, 1.0 - hihat_phase / 0.04, 0.0)
    # Deterministic noise based on sample index
    noise = np.sin(t * 12345.6789) * np.cos(t * 98765.4321)
    hihat = 0.12 * hihat_env * noise

    # Layer 3: sub-bass drone
    sub = 0.15 * np.sin(2 * np.pi * 55 * t)

    # Layer 4: synth stab every 2 beats
    stab_phase = (t * beat_freq / 2) % 1.0
    stab_mask = stab_phase < 0.12
    stab_env = np.where(stab_mask, 1.0 - stab_phase / 0.12, 0.0)
    stab = 0.25 * stab_env * np.sin(2 * np.pi * 220 * t)
    stab += 0.12 * stab_env * np.sin(2 * np.pi * 330 * t)

    # Layer 5: rising sweep in last 3 seconds (builds tension for ending)
    sweep_start = TOTAL_DURATION - 3.0
    sweep_mask = t > sweep_start
    sweep_progress = np.where(sweep_mask, (t - sweep_start) / 3.0, 0.0)
    sweep_freq = 200 + 800 * sweep_progress
    sweep = 0.15 * sweep_progress * np.sin(2 * np.pi * sweep_freq * t)

    # Layer 6: transition "whoosh" at scene changes
    whoosh = np.zeros_like(t)
    for sc_t in SCENE_STARTS[1:]:  # skip first scene
        dt = np.abs(t - sc_t)
        wmask = dt < 0.15
        wenv = np.where(wmask, 1.0 - dt / 0.15, 0.0)
        whoosh += 0.3 * wenv * np.sin(2 * np.pi * (500 + 2000 * wenv) * t)

    sample = kick + hihat + sub + stab + sweep + whoosh

    # Soft clip via tanh
    sample = np.tanh(sample * 1.2) * 0.8

    # Return stereo
    return np.column_stack([sample, sample])


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"Generating {TOTAL_DURATION:.1f}s promo video at {WIDTH}x{HEIGHT} @ {FPS}fps")
    print(f"Scenes: {len(SCENES)}")

    video = VideoClip(make_frame, duration=TOTAL_DURATION)
    video = video.with_fps(FPS)

    audio = AudioClip(make_audio, duration=TOTAL_DURATION, fps=44100)
    video = video.with_audio(audio)

    output_path = "/home/user/claude-sandbox/explorations/nlp-course-promo/promo_video.mp4"
    print(f"Rendering to {output_path}...")
    video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        preset="medium",
        logger="bar",
    )
    print(f"Done! Video saved to {output_path}")


if __name__ == "__main__":
    main()
