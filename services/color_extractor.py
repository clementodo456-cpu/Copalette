import io
from PIL import Image
import math

def get_color_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
    """Calculates Euclidean distance between two RGB colors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def extract_palette(img: Image.Image, num_colors: int = 5) -> list[tuple[str, tuple[int, int, int]]]:
    """
    Extracts distinct dominant colors from an image.
    Handles RGB and RGBA transparency gracefully.
    Returns list of tuples: [("#HEX", (R, G, B)), ...]
    """
    # Optimize image size for color extraction to save CPU/memory
    image_copy = img.copy()
    image_copy.thumbnail((400, 400), Image.Resampling.LANCZOS)

    # Handle transparency by flattening onto a neutral white background
    if image_copy.mode in ("RGBA", "LA") or (image_copy.mode == "P" and "transparency" in image_copy.info):
        background = Image.new("RGB", image_copy.size, (255, 255, 255))
        if image_copy.mode != "RGBA":
            image_copy = image_copy.convert("RGBA")
        background.paste(image_copy, mask=image_copy.split()[3])
        image_copy = background
    else:
        image_copy = image_copy.convert("RGB")

    # Quantize to an intermediate palette to aggregate similar colors
    quantized_count = max(num_colors * 4, 32)
    quantized = image_copy.quantize(colors=quantized_count, method=Image.Quantize.MEDIANCUT)
    palette_raw = quantized.getpalette()[:quantized_count * 3]
    color_counts = quantized.getcolors(maxcolors=400 * 400)

    if not color_counts:
        # Fallback to standard RGB conversion
        colors_sorted = [(1, (255, 255, 255))]
    else:
        # Sort colors by frequency descending
        color_counts.sort(key=lambda x: x[0], reverse=True)
        colors_sorted = []
        for count, idx in color_counts:
            r = palette_raw[idx * 3]
            g = palette_raw[idx * 3 + 1]
            b = palette_raw[idx * 3 + 2]
            colors_sorted.append((count, (r, g, b)))

    # Filter out visually redundant colors
    distinct_colors: list[tuple[int, int, int]] = []
    min_distance = 35.0  # Color distinction threshold

    for _, rgb in colors_sorted:
        if len(distinct_colors) >= num_colors:
            break
        if not any(get_color_distance(rgb, existing) < min_distance for existing in distinct_colors):
            distinct_colors.append(rgb)

    # Fallback if distance filtering was too strict
    if len(distinct_colors) < num_colors:
        for _, rgb in colors_sorted:
            if len(distinct_colors) >= num_colors:
                break
            if rgb not in distinct_colors:
                distinct_colors.append(rgb)

    # Convert to standard HEX/RGB format output
    final_palette = []
    for rgb in distinct_colors[:num_colors]:
        hex_code = f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
        final_palette.append((hex_code, rgb))

    return final_palette
