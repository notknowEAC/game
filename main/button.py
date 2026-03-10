"""Small UI helper for rendering and interacting with buttons."""


class Button:
    """Drawable button with a hover state and hit-test rectangle."""
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """Cache surfaces and rectangles needed for drawing and hit testing."""
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """Draw the button image (if any) and its text."""
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """Return True if a position is inside the button bounds."""
        return (
            self.rect.left <= position[0] <= self.rect.right
            and self.rect.top <= position[1] <= self.rect.bottom
        )

    def changeColor(self, position):
        """Swap text color based on hover state."""
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
