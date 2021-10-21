class GlobalVar():
    def __init__(self):
        self.player_vel_multiplier = 1.25
        self.block_vel_multiplier = 1.3
        self.block_distance_multiplier = 1.1
        self.score_multiplier = 2.3


var = GlobalVar()
player_vel = 6
block_distance = 80
block_distance2 = 170
block_vel = -5
score = 15
bullet_vel = 12

for i in range(6):
    bullet_vel = int(bullet_vel * var.player_vel_multiplier)
    player_vel = int(player_vel * var.player_vel_multiplier)
    print(bullet_vel, player_vel)