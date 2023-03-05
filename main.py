import copy
import pygame
from level0 import boards
import math

pi = math.pi

pygame.init()
pygame.font.init()

width = 690
height = 690

screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font(None, 40)

level = copy.deepcopy(boards)
chomp = pygame.mixer.Sound('sounds/pacman_chomp.wav')
eatingpowerup = pygame.mixer.Sound('sounds/pacman_eatfruit.wav')
death = pygame.mixer.Sound('sounds/pacman_death.wav')
eatingghost = pygame.mixer.Sound('sounds/pacman_eatghost.wav')
chomp.set_volume(0.3)
eatingghost.set_volume(0.3)
death.set_volume(0.3)
eatingghost.set_volume(0.3)
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load('player/' + str(i) + '.png'), (25, 25)))

pink_img = pygame.transform.scale(pygame.image.load(f'ghosts/pink.png'), (25,25))
blue_img = pygame.transform.scale(pygame.image.load(f'ghosts/blue.png'), (25,25))
red_img = pygame.transform.scale(pygame.image.load(f'ghosts/red.png'), (30,30))
orange_img = pygame.transform.scale(pygame.image.load(f'ghosts/orange.png'), (25,25))
scared_img = pygame.transform.scale(pygame.image.load(f'ghosts/scared.png'), (25,25))
dead_img = pygame.transform.scale(pygame.image.load(f'ghosts/eyes.png'), (25,25))
counter = 0
flicker = True
direction_command = 0
score = 0
lives = 3
powerup = False
moving = False
power_count = 0
startup_counter = 0
start_x = 360
start_y = 480
red_x = 40
red_y = 40
else_x = 330
else_y = 290
else_direction = 2
game_over = False
game_win = False



class PacMan():

    def __init__(self, coord_x, coord_y, speed, direction):
        self.x_position = coord_x
        self.y_postion = coord_y
        self.center_x = self.x_position + 9
        self.center_y = self.y_postion + 10
        self.speed = speed
        self.direction = direction

    def update_center(self):
        self.center_x = self.x_position + 9
        self.center_y = self.y_postion + 10
    def allowed_to_turn(self):

        num1 = (height-50)//32
        num2 = (width)//30
        num3 = 15
        allowed = [False, False, False, False]
        if self.center_x//30 < 29:
            if level[self.center_y//num1][(self.center_x-num3)//num2] < 3:
                allowed[1] = True
            if level[self.center_y//num1][(self.center_x+num3)//num2] < 3:
                allowed[0] = True
            if level[(self.center_y+num3)//num1][self.center_x//num2] < 3:
                allowed[3] = True
            if level[(self.center_y-num3)//num1][self.center_x//num2] < 3:
                allowed[2] = True
        else:

            allowed[0] = True
            allowed[1] = True
        return allowed
    def move(self, turns):

        if self.direction == 0 and turns[0]:
            self.x_position += self.speed
        if self.direction == 1 and turns[1]:
            self.x_position -= self.speed
        if self.direction == 2 and turns[2]:
            self.y_postion -= self.speed
        if self.direction == 3 and turns[3]:
            self.y_postion += self.speed
    def rectangle_pacman(self):
        pacman_rect = pygame.rect.Rect((self.center_x - 9, self.center_y - 10), (30, 30))
        return pacman_rect
    def image(self):
        if self.direction == 0:
            screen.blit(player_images[counter // 5], (self.x_position, self.y_postion))
        elif self.direction == 1:
            screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (self.x_position, self.y_postion))
        elif self.direction == 2:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (self.x_position, self.y_postion))
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (self.x_position, self.y_postion))


class Ghost():
    def __init__(self, coord_x, coord_y, speed, direction, img, scared, eaten):
        self.x_position = coord_x
        self.y_postion = coord_y
        self.center_x = self.x_position + 9
        self.center_y = self.y_postion + 10
        self.speed = speed
        self.direction = direction
        self.image = img
        self.scared = scared
        self.eaten = eaten
        self.start_x = coord_x
        self.start_y = coord_y
        self.touch = False

    def set_image(self):
        if (not powerup and not self.scared) or (self.eaten and powerup and not self.scared):
            screen.blit(self.image, (self.x_position, self.y_postion))
        elif powerup and self.scared and not self.eaten:
            screen.blit(scared_img, (self.x_position, self.y_postion))
        else:
            screen.blit(dead_img, (self.x_position, self.y_postion))

    def rectangle_ghost(self):
        ghost_rect = pygame.rect.Rect((self.center_x - 9, self.center_y - 10), (30, 30))
        return ghost_rect

    def check_box(self):
        if 270 < self.x_position < 390 and 275 < self.y_postion < 320:
            return True
        else:
            return False
    def update_center_ghost(self):
        self.center_x = self.x_position + 9
        self.center_y = self.y_postion + 10
    def allowed_to_turn_ghost(self):
        self.update_center_ghost()
        num1 = (height-50)//32
        num2 = (width)//30
        num3 = 15
        allowed = [False, False, False, False]
        if self.center_x//30 < 29:
            if level[self.center_y//num1][(self.center_x-num3)//num2] < 3:
                allowed[1] = True
            if level[self.center_y//num1][(self.center_x+num3)//num2] < 3:
                allowed[0] = True
            if level[(self.center_y+num3)//num1][self.center_x//num2] < 3 or level[(self.center_y+num3)//num1][self.center_x//num2] == 9:
                allowed[3] = True
            if level[(self.center_y-num3)//num1][self.center_x//num2] < 3 or level[(self.center_y-num3)//num1][self.center_x//num2] == 9:
                allowed[2] = True
        else:

            allowed[0] = True
            allowed[1] = True

        return allowed
    def find_target(self, target_scared):
        target = (player.x_position, player.y_postion)
        global score
        ghost_rect = self.rectangle_ghost()
        pacman_rect = player.rectangle_pacman()

        if not powerup:
            if self.eaten and not self.check_box():
                self.speed = 3
                target = (330, 300)
            else:
                self.scared = False
                self.eaten = False
                self.speed = 2
                target = (player.x_position, player.y_postion)
                if pygame.Rect.colliderect(ghost_rect, pacman_rect):
                    self.touch = True

        if powerup:
            if not self.eaten:
                self.scared = True
                target = target_scared
                if pygame.Rect.colliderect(ghost_rect, pacman_rect):
                    score += 200
                    self.eaten = True
                    eatingghost.play()
            elif self.scared and self.eaten and not self.check_box():
                self.speed = 3
                target = (330, 300)
            elif self.scared and self.eaten and self.check_box():
                self.speed = 2
                self.scared = False
                target = (player.x_position, player.y_postion)
            elif not self.scared and self.eaten:
                if pygame.Rect.colliderect(ghost_rect, pacman_rect):
                    self.touch = True

        return target
    def move_ghost(self):
        pass

class Blinky(Ghost):

    def move_ghost(self):
        self.target = self.find_target((500, 50))
        self.turns = self.allowed_to_turn_ghost()
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                if self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                else:
                    self.x_position += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                if self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                else:
                    self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_position and self.turns[1]:
                self.direction = 1
                self.x_position -= self.speed
            elif self.target[1] < self.y_postion and self.turns[2]:
                self.direction = 2
                self.y_postion -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_postion -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.y_postion += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_postion += self.speed

        if self.x_position < 0:
            self.x_position = 660
        elif self.x_position > 660:
            self.x_position = 5

class Inky(Ghost):
    def move_ghost(self):
        self.target = self.find_target((450, 550))
        self.turns = self.allowed_to_turn_ghost()
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                if self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                else:
                    self.x_position += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                if self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                else:
                    self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_postion and self.turns[2]:
                self.direction = 2
                self.y_postion -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[2]:
                self.y_postion -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.y_postion += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[3]:
                self.y_postion += self.speed

        if self.x_position < 0:
            self.x_position = 660
        elif self.x_position > 660:
            self.x_position = 5

class Pinky(Ghost):
    def move_ghost(self):
        self.target = self.find_target((150, 550))
        self.turns = self.allowed_to_turn_ghost()
        if self.direction == 0:

            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
                if self.turns[2]:
                    self.direction = 2
            elif not self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                self.x_position += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_position and self.turns[1]:
                self.direction = 1
                self.x_position -= self.speed
            elif self.target[1] < self.y_postion and self.turns[2]:
                self.direction = 2
                self.y_postion -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_postion -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.y_postion += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_postion += self.speed

        if self.x_position < 0:
            self.x_position = 660
        elif self.x_position > 660:
            self.x_position = 5

class Clyde(Ghost):
    def move_ghost(self):
        self.target = self.find_target((195, 50))
        self.turns = self.allowed_to_turn_ghost()
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                if self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                else:
                    self.x_position += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                if self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                else:
                    self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_position and self.turns[1]:
                self.direction = 1
                self.x_position -= self.speed
            elif self.target[1] < self.y_postion and self.turns[2]:
                self.direction = 2
                self.y_postion -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_postion and self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_postion += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_postion -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_postion and self.turns[3]:
                self.y_postion += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_postion and self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_postion -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_postion += self.speed

        if self.x_position < 0:
            self.x_position = 660
        elif self.x_position > 660:
            self.x_position = 5
            
def draw_board():
    num1 = ((height - 50)//32)
    num2 = (width // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j*num2 + (0.5*num2), i*num1 + (0.5*num1)), 3)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j*num2 + (0.5*num2), i*num1 + (0.5*num1)), 6)
            if level[i][j] == 3:
                pygame.draw.line(screen, 'blue', (j*num2 + (0.5*num2), i*num1), (j*num2 + (0.5*num2), i*num1+num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, 'blue', (j*num2, i*num1+ (0.5*num1)), (j*num2 + num2, i*num1+ (0.5*num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, 'blue', [(j*num2 - (0.5*num2)), (i*num1 +(0.5*num1)), num2, num1], 0, pi/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, 'blue', [(j*num2 + (0.5*num2)), (i*num1 +(0.5*num1)), num2, num1], pi/2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [(j*num2 + (0.5*num2)), (i*num1 - (0.5*num1)), num2, num1], pi, 3*pi/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, 'blue', [(j*num2 - (0.5*num2)), (i*num1 -(0.5*num1)), num2, num1], 3*pi/2, 2*pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j*num2, i*num1+ (0.5*num1)), (j*num2 + num2, i*num1+ (0.5*num1)), 3)
def draw_menu():
    score_text = font.render('Score: ' + str(score), True, 'white')
    screen.blit(score_text, (10, 660))
    if powerup:
        pygame.draw.circle(screen, 'red', (140, 670), 10)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (20, 20)), (600 + i * 25, 660))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 600, 300], 0, 10)
        pygame.draw.rect(screen, 'black', [70, 220, 560, 260], 0, 10)
        game_over_text = font.render('Game over! Space bar to restart!', True, 'white')
        screen.blit(game_over_text, (190, 350))
    if game_win:
        pygame.draw.rect(screen, 'white', [50, 200, 600, 300], 0, 10)
        pygame.draw.rect(screen, 'black', [70, 220, 560, 260], 0, 10)
        game_over_text = font.render('You win! Space bar to restart!', True, 'white')
        screen.blit(game_over_text, (190, 350))

def check_collision(score, powerup, power_count):
    chomp.fadeout(250)
    num1 = (height - 40)//32
    num2 = width//30
    if 0 < player.x_position < 780:
        if level[player.center_y//num1][player.center_x//num2] == 1:
            level[player.center_y // num1][player.center_x // num2] = 0
            score += 10
            chomp.play()

        if level[player.center_y//num1][player.center_x//num2] == 2:
            level[player.center_y // num1][player.center_x // num2] = 0
            score += 50
            eatingghost.play()
            powerup = True
            power_count = 0
    return score, powerup, power_count


player = PacMan(360, 480, 2, 0)
red = Blinky(red_x, red_y, 2, 0, red_img, False, False)
blue = Inky(else_x - 15, else_y, 2 ,else_direction, blue_img, False, False)
pink = Pinky(else_x + 15, else_y,2, else_direction, pink_img, False, False)
orange = Clyde(else_x, else_y - 15,2, else_direction, orange_img, False, False)

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter+=1
        if counter > 10:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_count < 600:
        power_count +=1
    elif powerup and power_count >=600:
        power_count = 0
        powerup = False
    if startup_counter < 180 and not game_win and not game_over:
        moving = False
        startup_counter += 1
    else:
        moving = True
    screen.fill('black')
    draw_board()
    draw_menu()
    blue.set_image()
    pink.set_image()
    orange.set_image()
    red.set_image()
    player.image()
    game_win = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_win = False

    allowed = player.allowed_to_turn()
    if moving:
        player.move(allowed)
        player.update_center()
        red.move_ghost()
        blue.move_ghost()
        pink.move_ghost()
        orange.move_ghost()

    score, powerup, power_count = check_collision(score, powerup, power_count)
    if red.touch or blue.touch or pink.touch or orange.touch:
        death.play()
        if lives > 0:
            lives -= 1
            powerup = False
            power_count = 0
            startup_counter = 0
            moving = False
            player.x_position = start_x
            player.y_postion = start_y
            red.x_position = red_x
            red.y_postion = red_y
            red.direction = 0
            blue.x_position = else_x - 15
            blue.y_postion = else_y
            blue.direction = else_direction
            pink.x_position = else_x + 15
            pink.y_postion = else_y
            pink.direction = else_direction
            orange.x_position = else_x
            orange.y_postion = else_y - 15
            orange.direction = else_direction
            orange.eaten = False
            orange.scared = False
            orange.touch = False
            pink.eaten = False
            pink.scared = False
            pink.touch = False
            blue.eaten = False
            blue.scared = False
            blue.touch = False
            red.eaten = False
            red.scared = False
            red.touch = False
        else:
            powerup = False
            power_count = 0
            startup_counter = 0
            moving = False
            game_over = True



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction_command = 0
            if event.key == pygame.K_a:
                direction_command = 1
            if event.key == pygame.K_w:
                direction_command = 2
            if event.key == pygame.K_s:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_win):
                powerup = False
                power_count = 0
                startup_counter = 0
                moving = False
                player.x_position = start_x
                player.y_postion = start_y
                red.x_position = red_x
                red.y_postion = red_y
                red.direction = 0
                blue.x_position = else_x - 15
                blue.y_postion = else_y
                blue.direction = else_direction
                pink.x_position = else_x + 15
                pink.y_postion = else_y
                pink.direction = else_direction
                orange.x_position = else_x
                orange.y_postion = else_y - 15
                orange.direction = else_direction
                orange.eaten = False
                orange.scared = False
                orange.touch = False
                pink.eaten = False
                pink.scared = False
                pink.touch = False
                blue.eaten = False
                blue.scared = False
                blue.touch = False
                red.eaten = False
                red.scared = False
                red.touch = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_win = False
        for i in range(4):
            if direction_command == i and allowed[i]:
                player.direction = i

    if player.x_position > 650:
        player.x_position = 0
    elif player.x_position < 0:
        player.x_position = 650

    pygame.display.flip()

pygame.quit()

