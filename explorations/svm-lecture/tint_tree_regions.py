"""Colour the regions of the decision-tree figure (assets/decision_tree_orig.png) by majority class.

Light blue where triangles are the majority, light yellow where circles are. The tint is a
multiply blend, so lines, markers and labels keep their darkness. Region pixel bounds were
measured from the image (frame x 111..971, y 91..736; h0 at x=386, h2 at y=521, h3 at y=347,
h4 at x=206, h5 at x=637).

Run: .venv/bin/python tint_tree_regions.py
"""
from PIL import Image

SRC, OUT = "assets/decision_tree_orig.png", "assets/decision_tree_regions.png"
BLUE, YELLOW = (200, 228, 250), (255, 241, 180)
# (x0, x1, y0, y1, colour), inclusive pixel bounds inside the frame
REGIONS = [
    (112, 385, 92, 520, YELLOW),   # R1: x < 5.45, y > 2.8   mostly circles
    (112, 205, 521, 735, YELLOW),  # R3: x < 4.7,  y < 2.8   one circle
    (206, 385, 521, 735, BLUE),    # R4: 4.7 < x < 5.45, y < 2.8   triangles
    (387, 636, 92, 346, YELLOW),   # R5: 5.45 < x < 6.5, y > 3.45  circles
    (637, 970, 92, 346, BLUE),     # R6: x > 6.5, y > 3.45   triangles
    (387, 970, 347, 735, BLUE),    # R2: x > 5.45, y < 3.45  triangles
]

im = Image.open(SRC).convert("RGB")
px = im.load()
for x0, x1, y0, y1, c in REGIONS:
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            r, g, b = px[x, y]
            px[x, y] = (r * c[0] // 255, g * c[1] // 255, b * c[2] // 255)
im.save(OUT)
print("wrote", OUT)
