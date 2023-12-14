#!/usr/bin/env python

import random
import time

import unicornhathd


print("""Unicorn HAT HD: Game Of Life

Runs Conway's Game Of Life on your Unicorn HAT HD, this
starts with a random spread of life, so results may vary!

Press Ctrl+C to exit!
""")

try:
    xrange
except NameError:
    xrange = range

unicornhathd.rotation(0)

start_brightness = 0.2
unicornhathd.brightness(start_brightness)
width, height = unicornhathd.get_shape()

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

    def show_board(self):
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.value(i, j)]
                unicornhathd.set_pixel(i, j, rgb[0], rgb[1], rgb[2])
        unicornhathd.show()



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
            unicornhathd.brightness(start_brightness / wait * fade)
            time.sleep(0.08)

except KeyboardInterrupt:
    unicornhathd.clear()
    unicornhathd.off()

unicornhathd.clear()
unicornhathd.off()
