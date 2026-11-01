import re

with open('generate_report_diagrams.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace CSS rgba() with matplotlib tuple format
def replace_rgba(m):
    r,g,b,a = m.group(1), m.group(2), m.group(3), m.group(4)
    # Return as tuple string: (r/255, g/255, b/255, a)
    return f"({int(r)/255:.3f},{int(g)/255:.3f},{int(b)/255:.3f},{a})"

content = re.sub(
    r"'rgba\((\d+),(\d+),(\d+),([\d.]+)\)'",
    lambda m: f"({int(m.group(1))/255:.3f},{int(m.group(2))/255:.3f},{int(m.group(3))/255:.3f},{m.group(4)})",
    content
)

# Also fix hex+2digit alpha like '#6366f144' -> proper tuple
def hex_alpha(m):
    h = m.group(1)
    a_hex = m.group(2)
    r = int(h[0:2],16)/255
    g = int(h[2:4],16)/255
    b = int(h[4:6],16)/255
    a = int(a_hex,16)/255
    return f"({r:.3f},{g:.3f},{b:.3f},{a:.2f})"

content = re.sub(
    r"'#([0-9a-fA-F]{6})([0-9a-fA-F]{2})'",
    hex_alpha,
    content
)

with open('generate_report_diagrams.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed rgba and hex-alpha colors')

