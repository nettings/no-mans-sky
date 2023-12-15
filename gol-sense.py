#!/usr/bin/env python

import random
import time
import math
from sense_hat import SenseHat

print("""AstroPi Sense-HAT: Game Of Life

Runs Conway's Game Of Life on your Sense HAT, this
starts with a random spread of life, so results may vary!

(code borrowed from Pimoroni's UnicornHATHD)

Press Ctrl+C to exit!
""")

try:
    xrange
except NameError:
    xrange = range

sense = SenseHat()
sense.set_rotation(0)

# sense.low_light = True
#sense.gamma = [0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,5,6,6,7,8]
sense.gamma = [0,1,1,2,2,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,8,8,8,8,9,9]

width = 8
height = 8

size = width * height


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

    def show_board(self,gain=1):
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.value(i, j)]
                sense.set_pixel(i, j, int(rgb[0]*gain), int(rgb[1]*gain), int(rgb[2]*gain))


try:
    while True:
        life = GameOfLife()
        gain = 1
        wait = 100
        fade = wait
        timestamp = 0
        timestamp_old = 0
        restart_secs= 450
        while not (life.all_dead() or (timestamp < timestamp_old)):
            timestamp_old = timestamp
            timestamp = time.monotonic() % restart_secs
            if (life.old_board == life.board):
                fade -= 4
            if (life.older_board == life.board):
                fade -= 2
                time.sleep(0.05)
            if (fade < 0):
                break
            life.next_generation()
            life.show_board(gain*fade/wait)
            time.sleep(0.1)

except KeyboardInterrupt:
    sense.clear()

sense.clear()
