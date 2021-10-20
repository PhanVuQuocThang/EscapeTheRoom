import pygame
import os
from Levels import game_classes
from Levels import game_mini_screen
import read_high_score as high_score

pygame.init()

# Functions
def rotate_center(img, angle, x, y):
    pass

def bullet_sphere_blit(length):
    if length == 0:
        SCREEN.blit(bullet_sphere_2, (200, 5))
        return None
    if length == 1:
        SCREEN.blit(bullet_sphere_1, (200, 5))
        return None
    if length == 2:
        SCREEN.blit(bullet_sphere_0, (200, 5))
        return None
    SCREEN.blit(bullet_sphere_reload, (200, 5))


# Variables
QUIT = None
WIDTH, HEIGHT = 1000, 600
res = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(res)

# pygame.image.load(os.path.join("Textures/", ""))

# Load background images
bg = pygame.image.load(os.path.join("Textures/Backgrounds", "level_bg_2.png"))
# Load graphics images
icon = pygame.image.load(os.path.join("Textures/Graphics", "icon.png"))
bullet_sphere_0 = pygame.image.load(os.path.join("Textures/Graphics", "bullet_sphere_0.png"))
bullet_sphere_1 = pygame.image.load(os.path.join("Textures/Graphics", "bullet_sphere_1.png"))
bullet_sphere_2 = pygame.image.load(os.path.join("Textures/Graphics", "bullet_sphere_2.png"))
bullet_sphere_reload = pygame.image.load(os.path.join("Textures/Graphics", "bullet_sphere_reload.png"))
# Load object images
player_orb_img = pygame.image.load(os.path.join("Textures/Objects", "player_orb.png"))   # player_orb
shield_orb_img = pygame.image.load(os.path.join("Textures/Objects", "shield_orb.png"))
bullet_img = pygame.image.load(os.path.join("Textures/Objects", "bullet_1_red.png"))
stable_turret_img = pygame.image.load(os.path.join("Textures/Objects", "turret_stable.png"))
block_breakable_img = pygame.image.load(os.path.join("Textures/Objects", "block_breakable.png"))
block_unbreakable_img = pygame.image.load(os.path.join("Textures/Objects", "block_unbreakable.png"))
block_shield_img = pygame.image.load(os.path.join("Textures/Objects", "block_shield.png"))
laser_img = pygame.image.load(os.path.join("Textures/Objects", "laser.png"))

SCREEN.get_height()
SCREEN.get_width()
def endless_lvl():
    global QUIT
    QUIT = False
    # Instantiate objects
    player = game_classes.Player(30, 285, player_orb_img, shield_orb_img, bullet_img)   # Main player
    breakable_block = game_classes.BlockBreakable(block_breakable_img)
    unbreakable_block = game_classes.BlockUnbreakable(block_unbreakable_img)
    powerup = game_classes.Powerup(block_shield_img, laser_img)
    game_function = game_classes.GameFunction()
    global_var = game_classes.GlobalVar()

    # Variables
    player.shield_count = 1
    font = pygame.font.SysFont("Calibri", 24, italic=True)
    FPS = 60
    fpsClock = pygame.time.Clock()
    # Display
    SCREEN.blit(player.img, (player.pos_x, player.pos_y))
    # In main() Variables
    color = (255, 255, 12)
    isOn = True
    # Move
    direction = 1
    #check = 0
    # Game loop
    while isOn:
        #if check < 10:  check += 1
        #else:   break

        # SCREEN displays
        SCREEN.blit(bg, (0, 0))
        event_list = pygame.event.get()
        for ev in event_list:   # Events check
            if ev.type == pygame.QUIT:
                isOn = False
                QUIT = True
            if ev.type == pygame.USEREVENT:
                player.reload_sec -= 1
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_d:
                    player.bullet_gen()
                if ev.key == pygame.K_f:
                    direction = direction*(-1)
                if ev.key == pygame.K_ESCAPE:       # ESCAPE
                    is_exit = ecs_screen()
                    if is_exit:
                        isOn = False
        # End event check
        display_score = font.render(f"Score: {player.score}", True, color)
        display_reload = font.render(str(player.reload_sec), True, color)
        display_shield = powerup.font.render("Shield(s): " + str(player.shield_count), True, color)
        SCREEN.blit(display_score, (5, 5))
        SCREEN.blit(display_reload, (209, 45))
        SCREEN.blit(display_shield, (WIDTH - 150, 5))
        # Bullet timer
        if player.bullet[0][0] == player.max_bullet:       # Start timer
            player.bullet[0][0] = player.max_bullet + 10    # A number > max_bullet
            # player.bullet[0][0] = 0
            pygame.time.set_timer(pygame.USEREVENT, 1000)   # 1000ms = 1s
        if player.reload_sec <= 0:       # Reset timer
            player.reload_sec = player.reload_sec_reset
            player.bullet[0][0] = 0
            pygame.time.set_timer(pygame.USEREVENT, 0)
        move_condition = ((player.pos_y + direction*player.vel + player.img.get_height() < HEIGHT) and
                          (player.pos_y + direction*player.vel + 1 > 0))
        if move_condition:
            player.pos_y += direction * player.vel

        bullet_sphere_blit(player.bullet[0][0])

        # Block gen
        unbreakable_block.block_gen_single(gen_type=unbreakable_block.block_tag["gen_type"],
                                           player_pos=(player.pos_x, player.pos_y))

        breakable_block.block_gen_single(gen_type=breakable_block.block_tag["gen_type"],
                                         player_pos=(player.pos_x, player.pos_y))

        powerup.gen_shield(player)

        game_function.block_overlap(breakable_block, unbreakable_block)
        game_function.block_overlap(unbreakable_block, powerup)

        # Block blit
        unbreakable_block.block_blit(SCREEN, player)

        breakable_block.block_blit(SCREEN, player)

        powerup.powerup_blit(SCREEN, player, power_type="shield")

        player.bullet_blit(SCREEN)
        if player.player_collide_single(breakable_block):
            if player.shield_count > 0:
                player.shield_count -= 1
            else:
                game_complete_screen(player, game_state="lose")
                isOn = False
        if player.player_collide_single(unbreakable_block):
            if player.shield_count > 0:
                player.shield_count -= 1
            else:
                game_complete_screen(player, game_state="lose")
                isOn = False

        player.update_player(SCREEN)

        # Multiplier
        game_function.var_multiply(player, breakable_block, unbreakable_block, powerup, global_var)

        #if player.score == 30:
        #    isOn = False

        pygame.display.update()
        fpsClock.tick(FPS)


# pygame.image.load(os.path.join("Textures/", ""))
# Load Background
esc_background = pygame.image.load(os.path.join("Textures/Backgrounds", "esc_background.png"))
lvl_button_continue = pygame.image.load(os.path.join("Textures/Graphics", "lvl_button_continue.png"))
lvl_button_exit = pygame.image.load(os.path.join("Textures/Graphics", "lvl_button_exit.png"))


def ecs_screen():
    global QUIT
    FPS = 60
    fpsClock = pygame.time.Clock()
    # Instantiate Objects
    button_continue = game_mini_screen.ContinueButton(383, 258, lvl_button_continue, lvl_button_continue)
    button_exit = game_mini_screen.ExitButton(561, 258, lvl_button_exit, lvl_button_exit)
    isOn = True
    while isOn:
        event_list = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        for ev in event_list:  # Events check
            if ev.type == pygame.QUIT:
                QUIT = True
                return True
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False
            if ev.type == pygame.MOUSEBUTTONDOWN:  # Check click
                if button_continue.click_continue(mouse_pos):
                    return False
                if button_exit.click_exit(mouse_pos):  # Quit
                    return True
        SCREEN.blit(esc_background, (200, 100))

        button_continue.button_blit(SCREEN, mouse_pos)
        button_exit.button_blit(SCREEN, mouse_pos)

        pygame.display.update()
        fpsClock.tick(FPS)


def game_complete_screen(player, game_state="lose"):
    global QUIT
    FPS = 60
    fpsClock = pygame.time.Clock()
    font = pygame.font.SysFont("Calibri", 60)
    color = (127, 0, 255)
    if game_state == "win":
        display_win = font.render("Level completed", True, color)
    # Instantiate Objects
    button_continue = game_mini_screen.ContinueButton(383, 258, lvl_button_continue, lvl_button_continue)
    button_exit = game_mini_screen.ExitButton(561, 258, lvl_button_exit, lvl_button_exit)
    isOn = True
    while isOn:
        event_list = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        for ev in event_list:  # Events check
            if ev.type == pygame.QUIT:
                QUIT = True
                return True
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False
            if ev.type == pygame.MOUSEBUTTONDOWN:  # Check click
                if button_continue.click_continue(mouse_pos):
                    return False
                if button_exit.click_exit(mouse_pos):  # Quit
                    return True
        SCREEN.blit(esc_background, (200, 100))
        if game_state == "lose":
            high_score_num = high_score.read_file()
            if int(high_score_num) < player.score:
                high_score.write_file(player.score)
            display_lose = font.render("Score: " + str(player.score), True, color)
            SCREEN.blit(display_lose, (380, 150))

        button_continue.button_blit(SCREEN, mouse_pos)
        button_exit.button_blit(SCREEN, mouse_pos)

        pygame.display.update()
        fpsClock.tick(FPS)

