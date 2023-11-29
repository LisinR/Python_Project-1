import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size):
        self.font = pygame.font.SysFont(None, font_size)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.clicked:
                self.clicked = False
                return self.rect.collidepoint(event.pos)
        return False

class Text:
    def __init__(self, font_size, text, text_color, dest):
        self.font = pygame.font.SysFont(None, font_size)
        self.text = self.font.render(text, True, text_color)
        self.dest = dest

    def draw(self, screen):
        screen.blit(self.text, self.dest)