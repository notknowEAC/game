"""Text layout helpers for fitting and wrapping UI strings."""


def truncate_text(font, text, max_width):
    """Trim text to fit within a pixel width, adding an ellipsis if needed."""
    if font.size(text)[0] <= max_width:
        return text

    suffix = "..."
    if font.size(suffix)[0] > max_width:
        return ""

    trimmed = text
    while trimmed and font.size(trimmed + suffix)[0] > max_width:
        trimmed = trimmed[:-1]
    return trimmed.rstrip() + suffix


def wrap_text(font, text, max_width):
    """Split text into lines that fit within a pixel width."""
    if not text:
        return [""]

    lines = []
    current = ""

    for char in text:
        if char == "\n":
            lines.append(current.rstrip())
            current = ""
            continue

        candidate = current + char
        if font.size(candidate)[0] <= max_width:
            current = candidate
            continue

        if current:
            lines.append(current.rstrip())
            current = "" if char == " " else char
        else:
            lines.append(char)

    if current or not lines:
        lines.append(current.rstrip())

    return [line for line in lines if line] or [""]


def draw_wrapped_text(screen, font, text, color, x, y, max_width, max_lines=None):
    """Render wrapped text and return the total height used."""
    lines = wrap_text(font, text, max_width)

    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        suffix = "..."
        while lines[-1] and font.size(lines[-1] + suffix)[0] > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + suffix

    line_height = font.get_linesize()
    for idx, line in enumerate(lines):
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y + idx * line_height))

    return len(lines) * line_height
