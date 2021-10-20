import pygame

pygame.init()


# Classes
class Button:
    def __init__(self, x, y, img, img2):
        self.x = x
        self.y = y
        self.img = img
        self.img2 = img2

    def simple_button_blit(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def button_blit(self, screen, mouse_pos):
        if self.isAbove(mouse_pos):
            screen.blit(self.img2, (self.x, self.y))
        else:
            screen.blit(self.img, (self.x, self.y))

    def isAbove(self, mouse_pos):
        """Return True if the mouse is at the image, else return False"""
        condition = ((self.x < mouse_pos[0] < self.x + self.img.get_width())
                     and (self.y < mouse_pos[1] < self.y + self.img.get_height()))
        return condition


class ContinueButton(Button):
    def __init__(self, x, y, img, img2):
        super().__init__(x, y, img, img2)
        self.tag = "continue"

    def click_continue(self, mouse_pos):
        if self.isAbove(mouse_pos):
            return True


class ExitButton(Button):
    def __init__(self, x, y, img, img2):
        super().__init__(x, y, img, img2)
        self.tag = "exit"

    def click_exit(self, mouse_pos):
        if self.isAbove(mouse_pos):
            return True


class ReplayButton(Button):
    def __init__(self, x, y, img, img2):
        super().__init__(x, y, img, img2)
        self.tag = "replay"

    def click_replay(self, mouse_pos):
        if self.isAbove(mouse_pos):
            return True


class Screen:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def screen_blit(self, screen):
        screen.blit(self.img, (self.x, self.y))
