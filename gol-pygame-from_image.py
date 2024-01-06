import os
import pygame
import random
import math
import time
import numpy
from PIL import Image

try:
    xrange
except NameError:
    xrange = range


width = 48
height = 27
size = width * height
fps = 5
    
class GameOfLife:
    def __init__(self):
        image = Image.open("./start.bmp")
        img_array = numpy.array(image)
        img_array = numpy.swapaxes(img_array, 0, 1)
#        self.board = [int(7 * random.getrandbits(1)) for _ in xrange(size)]
        img_array = numpy.reshape(img_array, -1)
        a = img_array.tolist()
        self.board = [ (7 - (x * 7)) for x in a ] 
        self.old_board = [False] * size
        self.older_board = [False] * size
#        self.color = [[255, 0, 30], [255, 160, 33], [179, 113, 23], [130, 81, 17], [102, 64, 13], [51, 32, 7], [25, 16, 3], [0, 0, 0]]
        self.color = [[255, 0, 30], [130, 81, 17], [102, 64, 13], [51, 32, 7], [25, 16, 3], [12, 9, 2], [6, 4, 1], [0, 0, 0]]

    def one_bit_noise(self):
        cell = random.randint(0, size)
        self.board[cell] = 7 - self.board[cell]
        
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

    def set_rect_cell(self,i, j, R, G, B):
        x = i * cell_width + cell_pad
        y = j * cell_height + cell_pad
        dx = cell_width - 2 * cell_pad
        dy = cell_height - 2 * cell_pad
        cell = pygame.Rect(x, y, dx, dy)
        background.fill((R,G,B), cell)

    def set_circ_cell(self, i, j, R, G, B):
        x = (i * 2 + 1) * (cell_width / 2) + cell_pad
        y = (j * 2 + 1) * (cell_height / 2) + cell_pad
        r = min(cell_width - 2 * cell_pad, cell_height - 2 * cell_pad) / 2
        pygame.draw.circle(background, (R,G,B), (x,y), r)
        
    def show_board(self):
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.value(i, j)]
                self.set_circ_cell(i, j, rgb[0], rgb[1], rgb[2])
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
pygame.display.set_caption("No Man's Sky")
pygame.mouse.set_visible(False)

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
        wait = 100
        fade = wait
        timestamp = 0
        timestamp_old = 0
        restart_secs= 600
        life = GameOfLife()
        life.one_bit_noise()
        life.show_board()
        pygame.time.wait(4000)        
        clock.tick(fps)
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_SPACE:
                        life=GameOfLife()
                        life.show_board()
            pygame.event.pump()
            clock.tick(fps)
    

except KeyboardInterrupt:
    pygame.quit()
    quit()
