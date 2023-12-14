import os
import pygame
import random
import math
import time

try:
    xrange
except NameError:
    xrange = range


width = 48
height = 27
size = width * height
fps = 10
    
class GameOfLife:
    def __init__(self):
        self.board = [int(7 * random.getrandbits(1)) for _ in xrange(size)]
        self.old_board = [False] * size
        self.older_board = [False] * size
        self.color = [[154, 154, 174], [0, 0, 255], [0, 0, 200], [0, 0, 160], [0, 0, 140], [0, 0, 90], [0, 0, 60], [0, 0, 0]]

    def value(self, x, y):
        index = ((x % width) * height) + (y % height)
        return self.board[index]

    def neighbors(self, x, y):
        sum = 0
        for i in xrange(3):
            for j in xrange(3):
                if i == 1 and j == 1:
                    continue
                if self.value(x + i - 1, y + j - 1) == 0:
                    sum = sum + 1
        return sum

    def next_generation(self):
        new_board = [False] * size
        for i in xrange(width):
            for j in xrange(height):
                neigh = self.neighbors(i, j)
                lvl = self.value(i, j)
                if lvl == 0:
                    if neigh < 2:
                        new_board[i * height + j] = min(7, lvl + 1)
                    elif 2 <= neigh <= 3:
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
                else:
                    if neigh == 3:
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
        self.older_board = self.old_board
        self.old_board = self.board
        self.board = new_board


    def all_dead(self):
        for i in xrange(size):
            if self.board[i] != 7:
                return False
        return True

    def set_cell(self,i, j, R, G, B):
        x = i * cell_width + cell_pad
        y = j * cell_height + cell_pad
        dx = cell_width - 2 * cell_pad
        dy = cell_height - 2 * cell_pad
        cell = pygame.Rect(x, y, dx, dy)
        background.fill((R,G,B), cell)

    def show_board(self):
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.value(i, j)]
                self.set_cell(i, j, rgb[0], rgb[1], rgb[2])
        screen.blit(background, (0,0))
        pygame.display.flip()

pygame.init()

life = GameOfLife()
canvas_width = 1920
canvas_height = 1080
cell_width=math.floor(canvas_width / width)
cell_height=math.floor(canvas_height / height)
cell_pad = 2
clock = pygame.time.Clock()
screen = pygame.display.set_mode((canvas_width, canvas_height), pygame.NOFRAME | pygame.FULLSCREEN | pygame.SCALED)
# , pygame.SCALED
pygame.display.set_caption("No Man's Sky")
pygame.mouse.set_visible(True)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((20,20,20))

#if pygame.font:
#    font = pygame.font.Font(None, 24)
#    text = font.render("Cellular Automaton First Prototype", True, (180,180,255))
#    textpos = text.get_rect(centerx=background.get_width() / 2, centery=background.get_height() / 2)
#    background.blit(text,textpos)
    
screen.blit(background, (0,0))
pygame.display.flip()

try:
    while True:
        life = GameOfLife()
        wait = 100
        fade = wait
        timestamp = 0
        timestamp_old = 0
        restart_secs= 600
        while not (life.all_dead() or (timestamp < timestamp_old)):
            timestamp_old = timestamp
            timestamp = time.monotonic() % restart_secs
            if (life.old_board == life.board):
                fade -= 4
            if (life.older_board == life.board):
                fade -= 2
                time.sleep(0.04)
            if (fade < 0):
                break
            life.next_generation()
            life.show_board()
        
#            life.color -= 5
            #unicornhathd.brightness(start_brightness / wait * fade)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                life = GameOfLife()
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
            pygame.event.pump()
            clock.tick(fps)

except KeyboardInterrupt:
    pygame.quit()
