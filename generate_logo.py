"""Generate application logo for CIH."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def generate_logo(output_path: str = "assets/logo.png") -> None:
    """Create a simple enterprise logo."""
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle with gradient effect (approximated)
    for i in range(size // 2, 0, -1):
        ratio = i / (size // 2)
        r = int(59 + (37 - 59) * (1 - ratio))
        g = int(130 + (99 - 130) * (1 - ratio))
        b = int(246 + (235 - 246) * (1 - ratio))
        draw.ellipse(
            [size // 2 - i, size // 2 - i, size // 2 + i, size // 2 + i],
            fill=(r, g, b, 255),
        )

    # Inner dark circle
    draw.ellipse([28, 28, 100, 100], fill=(15, 23, 42, 255))

    # Building icon (simple rectangles)
    draw.rectangle([48, 55, 58, 85], fill=(59, 130, 246, 255))
    draw.rectangle([62, 45, 72, 85], fill=(96, 165, 250, 255))
    draw.rectangle([76, 60, 86, 85], fill=(59, 130, 246, 255))

    # Crane arm
    draw.line([(40, 50), (90, 50)], fill=(255, 255, 255, 200), width=2)
    draw.line([(90, 50), (90, 65)], fill=(255, 255, 255, 200), width=2)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG")
    print(f"Logo saved to {path}")


if __name__ == "__main__":
    generate_logo()
