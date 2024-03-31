import pygame
import dop_function


class ImageButton:

    def __init__(self, x, y, width, height, text, image, hover_image=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = dop_function.load_image(image)
        self.hover_image = self.image
        if hover_image:
            self.hover_image = dop_function.load_image(hover_image)
            # self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        self.is_hovered = False

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, (self.x, self.y))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)


class StartButton(ImageButton):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return True

