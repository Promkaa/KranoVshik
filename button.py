import pygame

class ImageButton:
    def __init__(self, x, y, width, height,
                 image=None, hover_image=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Обработка основного изображения
        self.image = image or pygame.Surface((width, height))
        self.image = pygame.transform.scale(self.image, (width, height))

        # Обработка изображения для ховера
        if hover_image:
            self.hover_image = pygame.transform.scale(hover_image, (width, height))
        else:
            self.hover_image = self.image

        self.sound = sound
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.sound:
                self.sound.play()
            if self.is_hovered:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'button': self}))