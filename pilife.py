# Copyright (C) 2013 by Chuck Thier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import minecraft
import block
import time

class PiLife(object):
    def __init__(self):
        self.mc = minecraft.Minecraft.create('127.0.0.1')

    def create_board(self):
        pos = self.mc.player.getTilePos()
        self.size = 32
        self.x = pos.x-self.size/2
        self.y = pos.y
        self.z = pos.z-self.size/2
        # create the board
        self.mc.setBlocks(self.x, self.y-1, self.z, self.x+self.size-1, self.y-1,
                self.z+self.size-1, block.OBSIDIAN)
        # clear the area above a bit just to be sure
        self.mc.setBlocks(self.x, self.y, self.z, self.x+self.size-1, self.y+10,
                self.z+self.size-1, block.AIR)

    def run(self):
        self.mc.postToChat("Gathering blocks")
        grid = []
        for x in range(self.size):
            for z in range(self.size):
                grid.append(self.mc.getBlock(self.x+x, self.y, self.z+z))
        self.grid = grid
        self.mc.postToChat("Running simulation...")
        rev = 1
        while True:
            new_grid = self.step()
            for x in range(self.size):
                for z in range(self.size):
                    if new_grid[self.size*x+z] != self.grid[self.size*x+z]:
                        self.mc.setBlock(self.x+x, self.y, self.z+z,
                                new_grid[self.size*x+z])
            self.grid = new_grid
            rev += 1

    def step(self):
        def neighbors(x, z):
            count = 0
            for x1 in range(max(x-1, 0), min(x+2, self.size)):
                for z1 in range(max(z-1, 0), min(z+2, self.size)):
                    if x1 == x and z1 == z:
                        continue
                    if self.grid[x1*self.size+z1]:
                        count += 1
            return count

        new_grid = []
        for x in range(self.size):
            for z in range(self.size):
                count = neighbors(x, z)
                if self.grid[x*self.size+z] == 0 and count == 3:
                    new_grid.append(4)
                elif self.grid[x*self.size+z] and (count < 2 or count > 3):
                    new_grid.append(0)
                else:
                    new_grid.append(self.grid[x*self.size+z])
        return new_grid

