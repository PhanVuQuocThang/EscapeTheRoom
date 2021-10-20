import pygame
import os
import read_high_score as high_score
from Levels import tutorial, endless

pygame.init()

QUIT = True     # QUIT #


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


class Button2(Button):
    def __init__(self, x, y, img, img2, moveType):
        super().__init__(x, y, img, img2)
        self.moveType = (1 if moveType == "Forward" else 0)
        self.page = 1  # Used to count pages, starts at 1
        self.max = (4 if self.moveType else 1)

    def button_blit(self, screen, mouse_pos):
        if self.moveType:
            if self.page < self.max:
                if self.isAbove(mouse_pos):
                    screen.blit(self.img2, (self.x, self.y))
                else:
                    screen.blit(self.img, (self.x, self.y))
        else:
            if self.page > self.max:
                if self.isAbove(mouse_pos):
                    screen.blit(self.img2, (self.x, self.y))
                else:
                    screen.blit(self.img, (self.x, self.y))


class ButtonLevel(Button):
    def __init__(self, x, y, img, img2):
        super().__init__(x, y, img, img2)
        self.onClick = False
    def call_tutorial(self, mouse_pos):
        if self.isAbove(mouse_pos):
            tutorial.tutorial_lvl()
            lvl_quit()
    def call_endless(self, mouse_pos):
        if self.isAbove(mouse_pos):
            endless.endless_lvl()
            lvl_quit()


class PageCheck:
    def __init__(self):
        pass
    def render_text_1(self, screen, x, y):
        temp = font.render("Use W, S, A, D to move up, down, left, right.", True, (0, 0, 0))
        screen.blit(temp, (x, y))

    def render_text_2(self, screen, x, y):
        temp = font.render("Turrets will shoot bullets.", True, (0, 0, 0))
        temp2 = font.render("If you get hit by a bullet, your health is decrease by 1.", True, (0, 0, 0))
        temp3 = font.render("You start with 3 health. If your health reaches 0, you die.", True, (0, 0, 0))
        screen.blit(temp, (x, y))
        screen.blit(temp2, (x, y+40))
        screen.blit(temp3, (x, y+80))

    def render_text_0(self, screen, x, y):
        temp = font.render("Each Levels has a number of phases.", True, (0, 0, 0))
        temp2 = font.render("Depends on the Levels, it can have 3, 5, or 7 phases.", True, (0, 0, 0))
        temp3 = font.render("The \"Special Level\" has 22 phases, which are", True, (0, 0, 0))
        temp4 = font.render("the combination of the previous 20 phases and 2 special phases.", True, (0, 0, 0))
        screen.blit(temp, (x, y))
        screen.blit(temp2, (x, y + 40))
        screen.blit(temp3, (x, y + 80))
        screen.blit(temp4, (x, y + 120))

    def render_text_3(self, screen, x, y):
        temp = font.render("To reach the next phase, you must get to", True, (0, 0, 0))
        temp2 = font.render("the red button placed at somewhere in the Levels.", True, (0, 0, 0))
        temp3 = font.render("Once you reach the final phase, the button becomes purples.", True, (0, 0, 0))
        temp4 = font.render("Remember that reaching the next phase will NOT reset your health.", True, (0, 0, 0))
        screen.blit(temp, (x, y))
        screen.blit(temp2, (x, y + 40))
        screen.blit(temp3, (x, y + 80))
        screen.blit(temp4, (x, y + 120))

    def render_text_4(self, screen, x, y):
        temp = font.render("Please enjoy!", True, (255, 80, 0))
        screen.blit(temp, (x, y))

# Functions
def lvl_quit(no_global=False):
    isQUIT = (tutorial.QUIT or endless.QUIT)
    if not no_global:
        if isQUIT:
            global QUIT
            QUIT = True
    else:
        return isQUIT

# Things
WIDTH, HEIGHT = 1000, 600
MENU_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Calibri", 25)

# Load Backgrounds
menu_bg = pygame.image.load("Textures/Backgrounds/menu_bg.png")
howtoplay_bg = pygame.image.load("Textures/Backgrounds/howtoplay_bg.png")
# Load Graphics
icon = pygame.image.load(os.path.join("Textures/Graphics", "icon.png"))
button_play_img = pygame.image.load("Textures/Graphics/button_play_1.png")
button_howtoplay_img = pygame.image.load("Textures/Graphics/button_howtoplay_1.png")
button_quit_img = pygame.image.load("Textures/Graphics/button_quit_1.png")
button_info_img = pygame.image.load("Textures/Graphics/button_info_1.png")

pygame.display.set_icon(icon)
pygame.display.set_caption("Space Travel")

# Instantiate Objects
play_button = Button(423, 190, button_play_img, button_play_img)
howtoplay_button = Button(423, 255, button_howtoplay_img, button_howtoplay_img)
info_button = Button(423, 320, button_info_img, button_info_img)
exit_button = Button(423, 385, button_quit_img, button_quit_img)


def intro_main():
    FPS = 60
    clock = pygame.time.Clock()
    # count = 0     # Test variable
    isOn = True
    global QUIT
    QUIT = False
    while isOn:
        # if count < 10:  count +=1
        # else: isOn = False
        event_list = pygame.event.get()
        pos = pygame.mouse.get_pos()
        MENU_SCREEN.blit(menu_bg, (0, 0))
        play_button.button_blit(MENU_SCREEN, pos)
        howtoplay_button.button_blit(MENU_SCREEN, pos)
        info_button.button_blit(MENU_SCREEN, pos)
        exit_button.button_blit(MENU_SCREEN, pos)
        for ev in event_list:  # Events check
            if ev.type == pygame.QUIT:
                isOn = False
                QUIT = True
            if ev.type == pygame.MOUSEBUTTONDOWN:  # Check click
                if play_button.isAbove(pos):  # Play
                    lvl_list()
                    if on_lvl_1.onClick:
                        isOn = False
                    if QUIT:  # if QUIT == True
                        isOn = False
                if howtoplay_button.isAbove(pos):  # How to play
                    howtoplay_main()
                    if QUIT:  # if QUIT == True
                        isOn = False
                if exit_button.isAbove(pos):  # Quit
                    isOn = False
                    QUIT = True

        pygame.display.update()
        clock.tick(FPS)


# Load How-to-play images
player_orb = pygame.image.load("Textures/Objects/player_orb.png")
button_back = pygame.image.load("Textures/Graphics/button_back.png")
button_forward = pygame.image.load("Textures/Graphics/button_forward.png")
button_backward = pygame.image.load("Textures/Graphics/button_backward.png")
# Instantiate How-to-play Objects
back_button = Button(15, 15, button_back, button_back)
forward_button = Button2(953, 284, button_forward, button_forward, "Forward")
backward_button = Button2(15, 284, button_backward, button_backward, "Backward")
page_check = PageCheck()


def howtoplay_main():
    #count = 0
    # How-to-play Texts
    _move = font.render("Use W, S, A, D to move up, down, left, right", True, (0, 0, 0))
    # _test = font.render(f"{backward_button.moveType}", True, (0, 0, 0))
    FPS = 60
    clock = pygame.time.Clock()
    isOn = True
    global QUIT
    QUIT = False
    while isOn:
        #if count < 10:  count +=1
        #else: isOn = False
        event_list = pygame.event.get()
        pos = pygame.mouse.get_pos()
        for ev in event_list:  # Events check
            if ev.type == pygame.QUIT:
                isOn = False
                QUIT = True
            if ev.type == pygame.MOUSEBUTTONDOWN:  # Check click
                if back_button.isAbove(pos):  # Play
                    isOn = False
                if forward_button.isAbove(pos) and forward_button.page < forward_button.max:
                    forward_button.page += 1
                    backward_button.page += 1
                if backward_button.isAbove(pos) and backward_button.page > backward_button.max:
                    backward_button.page -= 1
                    forward_button.page -= 1
        MENU_SCREEN.blit(howtoplay_bg, (0, 0))
        back_button.button_blit(MENU_SCREEN, pos)
        forward_button.button_blit(MENU_SCREEN, pos)
        backward_button.button_blit(MENU_SCREEN, pos)
        MENU_SCREEN.blit(player_orb, (483, 284))
        # Render Texts
        enjoy = (430 if backward_button.page == 5 else 253)
        getattr(page_check, "render_text_" + str(backward_button.page), "")(MENU_SCREEN, enjoy, 336)
        pygame.display.update()
        clock.tick(FPS)


# Load lvl-list images
lvl_bg = pygame.image.load("Textures/Backgrounds/lvl_bg.png")
level_1_img = pygame.image.load("Textures/Graphics/lvl_1.png")
level_2_img = pygame.image.load("Textures/Graphics/lvl_2.png")
level_3_img = pygame.image.load("Textures/Graphics/lvl_3.png")
level_4_img = pygame.image.load("Textures/Graphics/lvl_4.png")
level_special_img = pygame.image.load("Textures/Graphics/lvl_special.png")
# Instantiate lvl-list Objects
# Instantiate lvl-list Objects
on_lvl_1 = ButtonLevel(200, 260, level_1_img, level_1_img)
on_endless = ButtonLevel(721, 260, level_special_img, level_special_img)


def lvl_list():
    color = (255, 116, 17)
    text_tutorial = font.render("Tutorial", True, color)
    text_endless = font.render("Endless", True, color)
    text_high_score = font.render("Highest Score: " + high_score.read_file(), True, (0, 0, 0))
    FPS = 60
    clock = pygame.time.Clock()
    global QUIT
    QUIT = False
    isOn = True
    #count = 0
    while isOn:
        #if count < 10:  count +=1
        #else: isOn = False
        event_list = pygame.event.get()
        pos = pygame.mouse.get_pos()
        MENU_SCREEN.blit(lvl_bg, (0, 0))
        back_button.button_blit(MENU_SCREEN, pos)
        on_lvl_1.button_blit(MENU_SCREEN, pos)
        on_endless.button_blit(MENU_SCREEN, pos)
        MENU_SCREEN.blit(text_tutorial, (200, 340))
        MENU_SCREEN.blit(text_endless, (721, 340))
        MENU_SCREEN.blit(text_high_score, (680, 370))
        for ev in event_list:
            if ev.type == pygame.QUIT:
                isOn = False
                QUIT = True
            if ev.type == pygame.MOUSEBUTTONDOWN:  # Check click
                if back_button.isAbove(pos):  # Play
                    isOn = False
                on_lvl_1.call_tutorial(pos)
                # Small note: Quitting Levels midway was handle by lvl_quit
                if lvl_quit(no_global=True):
                    isOn = False

            if ev.type == pygame.MOUSEBUTTONDOWN:  # Check click
                if back_button.isAbove(pos):  # Play
                    isOn = False
                on_endless.call_endless(pos)
                text_high_score = font.render("Highest Score: " + high_score.read_file(), True, (0, 0, 0))
                MENU_SCREEN.blit(text_high_score, (680, 370))
                # Small note: Quitting Levels midway was handle by lvl_quit
                if lvl_quit(no_global=True):
                    isOn = False

        pygame.display.update()
        clock.tick(FPS)


def main():     # Main game loop
    """I do not use 'isOn' for this loop because this is the main game
    loop, the variable 'QUIT' will determine if the game run or not."""
    global QUIT
    QUIT = False
    while not QUIT:
        event_list = pygame.event.get()
        for ev in event_list:
            if ev.type == pygame.QUIT:
                QUIT = True
        intro_main()
