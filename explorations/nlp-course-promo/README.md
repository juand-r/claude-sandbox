# NLP Course Promo Video Generator

Generates a meme-style, Gen Z-flavored promo video for Greg Durrett's
"Building LLM Reasoners" course (NYU Spring 2026).

## Style
- Kinetic typography with bold colors, fast cuts
- Meme references, internet humor
- TikTok/YouTube Shorts energy
- Hype-beast aesthetic: neon on dark, glitch effects, impact font vibes

## How to run
```bash
python3 generate_video.py
```
Outputs: `promo_video.mp4`

## Dependencies
- moviepy
- pillow
- ffmpeg (system)

## Audio assets (CC0)
Before running, download these CC0 files into `audio/`:
```bash
cd audio/
curl -sLO "https://opengameart.org/sites/default/files/dance_field_2_1.mp3" && mv dance_field_2_1.mp3 dance_field.mp3
curl -sL -o explosion_synth.flac "https://opengameart.org/sites/default/files/synthetic_explosion_1.flac"
curl -sL -o whoosh.wav "https://opengameart.org/sites/default/files/whoosh2_0.wav"
```
All audio is CC0 (public domain) from [OpenGameArt.org](https://opengameart.org).
