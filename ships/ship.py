"""This module defines a basic ship model."""
import pygame


class Ship:
    """This class is the base of the battleships."""

    def __init__(self, x: float, y: float, health_points: int) -> None:
        self.x = x
        self.y = y
        self.health_points = health_points

        self.width = 40
        self.height = 40 * self.health_points

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.is_dragging = False

    def render(self, window: pygame.Surface) -> None:
        """Render the ship."""
        pygame.draw.rect(window, (0, 0, 0), self.rect)

    def update(self) -> None:
        """Update the ship."""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def rotate(self) -> None:
        """Rotates the ship so it can be placed horizontally/vertically."""
        if self.width == 40:
            self.width = 40 * self.health_points
            self.height = 40
        elif self.height == 40:
            self.width = 40
            self.height = 40 * self.health_points

        self.update()
