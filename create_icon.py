"""生成应用图标 - 芝士郊狼控制软件"""
from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(output_path="app_icon.ico"):
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        s = size

        # Background circle - dark blue-purple
        margin = max(1, s // 16)
        draw.ellipse([margin, margin, s - margin - 1, s - margin - 1], fill=(25, 25, 60, 255))

        # Cheese wedge (yellow triangle) - left side
        cx, cy = s // 2, s // 2
        wedge_r = int(s * 0.38)
        cheese_points = [
            (cx - int(s * 0.05), cy - wedge_r),
            (cx - wedge_r, cy + int(s * 0.25)),
            (cx + int(s * 0.15), cy + int(s * 0.25)),
        ]
        draw.polygon(cheese_points, fill=(255, 210, 60, 255))

        # Cheese holes
        hole_r = max(1, s // 20)
        holes = [
            (cx - int(s * 0.15), cy - int(s * 0.05)),
            (cx + int(s * 0.02), cy + int(s * 0.12)),
            (cx - int(s * 0.08), cy + int(s * 0.08)),
        ]
        for hx, hy in holes:
            draw.ellipse([hx - hole_r, hy - hole_r, hx + hole_r, hy + hole_r],
                         fill=(220, 180, 40, 255))

        # Lightning bolt (shock symbol) - right side, overlapping cheese
        bolt_color = (0, 200, 255, 255)
        bolt_w = max(2, s // 10)
        bx = cx + int(s * 0.08)
        by_top = cy - int(s * 0.35)
        by_mid = cy + int(s * 0.02)
        by_bot = cy + int(s * 0.35)
        bx_left = bx - int(s * 0.12)
        bx_right = bx + int(s * 0.12)

        bolt_points = [
            (bx + int(s * 0.02), by_top),
            (bx_left, by_mid),
            (bx + int(s * 0.02), by_mid),
            (bx_right, by_bot),
            (bx - int(s * 0.02), by_mid),
            (bx + int(s * 0.02), by_mid),
        ]
        draw.polygon(bolt_points, fill=bolt_color)

        # Border ring
        draw.ellipse([margin, margin, s - margin - 1, s - margin - 1],
                     outline=(0, 180, 255, 200), width=max(1, s // 32))

        images.append(img)

    # Save as .ico with multiple sizes
    images[-1].save(output_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[:-1])
    print(f"Icon saved to {output_path}")

    # Also save PNG for reference
    png_path = output_path.replace(".ico", ".png")
    images[-1].save(png_path)
    print(f"PNG saved to {png_path}")


if __name__ == "__main__":
    create_icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico"))
