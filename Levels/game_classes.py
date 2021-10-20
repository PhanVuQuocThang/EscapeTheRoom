import pygame
from random import randint, choice

pygame.init()

"""
etr in etr_classes stands for EscapeTheRoom, the game"s old name
"""


# Classes

class GlobalVar():
    def __init__(self):
        self.player_vel_multiplier = 1.25
        self.block_vel_multiplier = 1.3
        self.block_distance_multiplier = 1.1
        self.score_multiplier = 2.4
        self.multiplier_counter = 0


class Player():
    def __init__(self, startpos_x, startpos_y, img, shield_img, bullet_img):
        self.img = img
        self.shield_img = shield_img
        self.bullet_img = bullet_img
        self.pos_x = startpos_x
        self.pos_y = startpos_y
        self.vel = 6
        # Counting variables
        self.score = 0
        self.shield_count = 0
        self.laser_count = 0
        # Bullet variables
        self.bullet = []
        self.max_bullet = 2
        self.bullet_vel = 12
        self.reload_sec = 2
        self.reload_sec_reset = 2
        self.bullet.append([0])  # Bullet counter
        self.score_knot = 15
        self.mask = pygame.mask.from_surface(self.img)

    def update_player(self, SCREEN):
        if self.shield_count < 1:
            SCREEN.blit(self.img, (self.pos_x, self.pos_y))
        else:
            SCREEN.blit(self.shield_img, (self.pos_x, self.pos_y))

    def bullet_gen(self):
        if len(self.bullet) - 1 < self.max_bullet:
            if self.bullet[0][0] < self.max_bullet:
                self.bullet[0][0] += 1
                self.bullet.append([self.pos_x + 16, self.pos_y + 8])
                return True
            return False

    def bullet_blit(self, SCREEN):
        if len(self.bullet) - 1 == 0:
            return None
        bullet_len = len(self.bullet) - 1
        for i in range(bullet_len, 0, -1):
            self.bullet[i][0] += self.bullet_vel  # # #
            SCREEN.blit(self.bullet_img,
                        (self.bullet[i][0], self.bullet[i][1]))
            self.bullet_check(SCREEN, i)

    def bullet_check(self, SCREEN, index):
        out_of_screen = ((self.bullet[index][0] > SCREEN.get_width()) or (self.bullet[index][0] < 0)
                         or (self.bullet[index][1] > SCREEN.get_height()) or self.bullet[index][1] < 0)
        if out_of_screen:
            self.bullet.pop(index)

    def player_collide_single(self, block_obj):
        if len(block_obj.block_list) < 3:
            return False
        for i in range(3):
            top_left_check = ((block_obj.block_list[i][0] <= self.pos_x <= block_obj.block_list[0][2]) and
                           (block_obj.block_list[i][1] <= self.pos_y <= block_obj.block_list[i][3]))

            bottom_left_check = ((block_obj.block_list[i][0] <= self.pos_x <= block_obj.block_list[0][2]) and
                           (block_obj.block_list[i][1] <= self.pos_y + 31<= block_obj.block_list[i][3]))

            top_right_check = ((block_obj.block_list[i][0] <= self.pos_x + 31 <= block_obj.block_list[0][2]) and
                           (block_obj.block_list[i][1] <= self.pos_y <= block_obj.block_list[i][3]))

            bottom_right_check = ((block_obj.block_list[i][0] <= self.pos_x + 31 <= block_obj.block_list[0][2]) and
                            (block_obj.block_list[i][1] <= self.pos_y + 31 <= block_obj.block_list[i][3]))
            condition = (top_left_check or bottom_left_check or top_right_check or bottom_right_check)
            if condition:
                block_obj.block_list.pop(i)
                return True



class BlockBreakable():
    def __init__(self, img):
        self.block_vel = -5
        self.img = img
        self.block_distance = 170
        self.block_list = []
        self.block_tag = {"single": 0, "triple": 0, "ver_line": 0, "hor_line": 0, "gen_type": "random"}
        self.type_list = ["random", "player"]

    def block_gen_single(self, gen_type, player_pos=(0, 0)):
        if self.block_tag["single"] > 11:
            return False
        if gen_type == "random":
            x_00 = 1005
            if len(self.block_list) > 0 and (x_00 - self.block_list[-1][2]) <= self.block_distance:
                return False
            y_00 = randint(0, 552)
            x_01 = x_00 + 47
            y_01 = y_00 + 47
            self.block_list.append([x_00, y_00, x_01, y_01])
            self.block_tag["single"] += 1
            self.block_tag["gen_type"] = choice(self.type_list)
            return True
        if gen_type == "player":
            start = ((player_pos[1] - 80) if (player_pos[1] - 80) >= 0 else 0)
            end = ((player_pos[1] + 80) if (player_pos[1] + 80) <= 553 else 553)
            x_10 = 1005
            if len(self.block_list) > 0 and (x_10 - self.block_list[-1][2]) < self.block_distance:
                return False
            y_10 = randint(start, end)
            x_11 = x_10 + 47
            y_11 = y_10 + 47
            self.block_list.append([x_10, y_10, x_11, y_11])
            self.block_tag["single"] += 1
            self.block_tag["gen_type"] = choice(self.type_list)
            return True

    def block_blit(self, SCREEN, player):
        length = len(self.block_list) - 1
        if length < 0:
            return False
        for i in range(length, -1, -1):
            SCREEN.blit(self.img, (self.block_list[i][0], self.block_list[i][1]))
            self.block_list[i][0] += self.block_vel  # x0
            self.block_list[i][2] += self.block_vel  # x1
            self.block_check_single(i, player)
        return True

    def block_check_single(self, index, player):
        if self.bullet_collide(index, player):
            self.block_tag["single"] -= 1
            return True
        precision = 2
        outOfScreen = (self.block_list[index][2] + precision < 0)
        if outOfScreen:
            self.block_list.pop(index)
            self.block_tag["single"] -= 1
            return True

    def bullet_collide(self, block_idx, player):
        for i in range(1, len(player.bullet)):
            bullet_x = player.bullet[i][0] + 13
            bullet_y0 = player.bullet[i][1] + 4
            bullet_y1 = player.bullet[i][1] + 11
            collide = (bullet_x > self.block_list[block_idx][0]
                       and ((self.block_list[block_idx][1] <= bullet_y0 <= self.block_list[block_idx][3])
                            or (self.block_list[block_idx][1] <= bullet_y1 <= self.block_list[block_idx][3])))
            if collide:
                self.block_list.pop(block_idx)
                player.bullet.pop(i)
                player.score += 1
                return True


class BlockUnbreakable(BlockBreakable):
    def __init__(self, img):
        super().__init__(img)
        self.block_distance = 80
        self.block_tag = {"single": 0, "triple": 0, "ver_line": 0, "large_cube": 0, "gen_type": "random"}

    def block_check_single(self, index, player):
        if self.bullet_collide(index, player):
            return True
        precision = 5
        outOfScreen = (self.block_list[index][2] + precision < 0)
        if outOfScreen:
            self.block_list.pop(index)
            self.block_tag["single"] -= 1
            return True

    def bullet_collide(self, block_idx, player):
        for i in range(1, len(player.bullet)):
            bullet_x = player.bullet[i][0] + 13
            bullet_y0 = player.bullet[i][1] + 4
            bullet_y1 = player.bullet[i][1] + 11
            collide = (bullet_x > self.block_list[block_idx][0]
                       and ((self.block_list[block_idx][1] <= bullet_y0 <= self.block_list[block_idx][3])
                            or (self.block_list[block_idx][1] <= bullet_y1 <= self.block_list[block_idx][3])))
            if collide:
                player.bullet.pop(i)
                return True


class GameFunction():
    def __init__(self):
        self.nothing = None

    def var_multiply(self, player, breakable_block, unbreakable_block, powerup, global_var):
        if global_var.multiplier_counter <= 5:
            if player.score == player.score_knot:
                player.vel = int(player.vel * global_var.player_vel_multiplier)
                breakable_block.block_vel = int(breakable_block.block_vel * global_var.block_vel_multiplier)
                unbreakable_block.block_vel = int(unbreakable_block.block_vel * global_var.block_vel_multiplier)
                powerup.vel = int(powerup.vel * global_var.block_vel_multiplier)
                breakable_block.block_distance = int(
                    breakable_block.block_distance * global_var.block_distance_multiplier)
                unbreakable_block.block_distance = int(
                    unbreakable_block.block_distance * global_var.block_distance_multiplier)
                player.score_knot = int(player.score_knot * global_var.score_multiplier)
                return True

    def block_overlap(self, block_breakable_obj, block_unbreakable_obj):
        if (len(block_breakable_obj.block_list) < 1) or (len(block_unbreakable_obj.block_list) < 1):
            return False
        breakable = block_breakable_obj.block_list[-1]
        unbreakable = block_unbreakable_obj.block_list[-1]
        top_left = ((breakable[0] <= unbreakable[0] <= breakable[2]) and
                          (breakable[1] <= unbreakable[1] <= breakable[3]))
        bottom_left = ((breakable[0] <= unbreakable[0] <= breakable[2]) and
                          (breakable[1] <= unbreakable[3] <= breakable[3]))
        top_right = ((breakable[0] <= unbreakable[2] <= breakable[2]) and
                          (breakable[1] <= unbreakable[1] <= breakable[3]))
        bottom_right = ((breakable[0] <= unbreakable[2] <= breakable[2]) and
                          (breakable[1] <= unbreakable[3] <= breakable[3]))
        # # #
        condition = (top_left or bottom_left or top_right or bottom_right)
        if condition:
            block_breakable_obj.block_list.pop()
            block_breakable_obj.block_tag["single"] -= 1


class Powerup():
    def __init__(self, shield_img, laser_img):
        self.shield = 0
        self.laser = 0
        self.shield_img = shield_img
        self.laser_img = laser_img
        self.power_type = ["shield", "laser"]
        self.font = pygame.font.SysFont("Calibri", 25)
        #
        self.distance = 100
        self.vel = -5
        self.block_list = []
        self.block_tag = {"single": 0}      # This does nothing
        self.laser_list = []

    def gen_shield(self, player):
        """20s/shield on average, about 5% chance to appear per second,
        Each number has an equal chance to appear, so any number can be used"""
        num = randint(1, 1200)     # 1-1200
        if num == 900:
            self.shield += 1
            x0 = 1005
            if (len(self.block_list) > 0) and ((x0 - self.block_list[-1][2]) < self.distance):
                return False
            y0 = randint(0, 552)
            x1 = x0 + 31
            y1 = y0 + 31
            self.block_list.append([x0, y0, x1, y1])
            self.block_tag["single"] = 0    # Still does nothing
            return True
        return False

    def gen_laser(self, player):    # Function not completed yet
        """28s/laser on average, about 0.035% chance to appear per frame,
        Each number has an equal chance to appear, so any number can be used"""
        num = randint(1, 1680)
        if num == 900:
            self.laser += 1
            print("Laser")
            return True

    def powerup_blit(self, SCREEN, player, power_type="shield"):
        if power_type == "shield":
            if len(self.block_list) < 0:
                return False
            img = self.shield_img
            length = len(self.block_list) - 1
            new_range = range(length, -1, -1)
            for i in new_range:
                self.block_list[i][0] += self.vel
                self.block_list[i][2] += self.vel
                SCREEN.blit(img, (self.block_list[i][0], self.block_list[i][1]))
                self.block_check_single(i, player)
            return True

        if power_type == "laser":
            if len(self.laser_list) < 0:
                return False

    def block_check_single(self, index, player):
        if self.bullet_collide(index, player):
            player.shield_count += 1
            return True
        precision = 2
        outOfScreen = (self.block_list[index][2] + precision < 0)
        if outOfScreen:
            self.block_list.pop(index)
            self.shield -= 1
            return True

    def bullet_collide(self, block_idx, player):
        for i in range(1, len(player.bullet)):
            bullet_x = player.bullet[i][0] + 13
            bullet_y0 = player.bullet[i][1] + 4
            bullet_y1 = player.bullet[i][1] + 11
            collide = (bullet_x > self.block_list[block_idx][0]
                       and ((self.block_list[block_idx][1] <= bullet_y0 <= self.block_list[block_idx][3])
                            or (self.block_list[block_idx][1] <= bullet_y1 <= self.block_list[block_idx][3])))
            if collide:
                self.block_list.pop(block_idx)
                self.shield -= 1
                player.bullet.pop(i)
                player.score += 1
                return True
