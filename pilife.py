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

import time

import minecraft
import block


class LifeGrid(object):
    """Helper class to handle the grid that the game of life is played on"""

    def __init__(self, size=32):
        self.size = size
        # The grid is represented as a single list.  You can imagine this as
        # taking every row and concatenating them together.
        self.grid = [0] * (self.size**2)

    def neighbors(self, x, y):
        """Get the number of neighbors that surround the location x, y"""
        count = 0
        # Note: the min and max functions are to prevent looking for
        # neighbors beyond the grid boundaries.
        for x1 in range(max(x - 1, 0), min(x + 2, self.size)):
            for y1 in range(max(y - 1, 0), min(y + 2, self.size)):
                if x1 == x and y1 == y:
                    # Don't count the original x, y.
                    continue
                if self.grid[x1 * self.size + y1]:
                    count += 1
        return count

    def get(self, x, y):
        """Returns the brick number at location x, y."""
        return self.grid[x * self.size + y]

    def set(self, x, y, val):
        """Set the brick number at location x, y."""
        self.grid[x * self.size + y] = val


class PiLife(object):
    """Conway's game of life in Minecraft"""

    def __init__(self, size=32):
        """Initialize Life"""
        # Set up the minecraft connection
        self.conn = minecraft.Minecraft.create('127.0.0.1')
        self.size = size
        self.grid = LifeGrid(size)

    def create_board(self):
        """Create the board centered around the player's current position"""
        pos = self.conn.player.getTilePos()
        self.x = pos.x-self.size/2
        self.y = pos.y
        self.z = pos.z-self.size/2
        # Create the board
        self.conn.setBlocks(self.x, self.y - 1, self.z, self.x + self.size - 1,
                            self.y - 1, self.z + self.size - 1, block.OBSIDIAN)
        # Clear the area above a bit just to be sure
        self.conn.setBlocks(self.x, self.y, self.z, self.x + self.size - 1,
                            self.y + 20, self.z + self.size - 1, block.AIR)

    def step(self, grid):
        """Calculate the next generation.  Returns the next generation grid"""
        new_grid = LifeGrid(grid.size)
        for x in range(grid.size):
            for y in range(grid.size):
                count = grid.neighbors(x, y)
                block = grid.get(x, y)
                if block == 0 and count == 3:
                    # If a cell is empty and has 3 neighbors,
                    # a new block is born
                    new_grid.set(x, y, 4)
                elif block != 0 and (count < 2 or count > 3):
                    # If a cell has a block, and has less than 2 or
                    # greater than 3 neighbors, remove the block
                    new_grid.set(x, y, 0)
                else:
                    # Otherwise, leave the block as is
                    new_grid.set(x, y, grid.get(x, y))
        return new_grid

    def run(self):
        self.conn.postToChat("Gathering blocks")
        # Note: There currently isn't a bulk get blocks opperation, so for
        # now, we have to loop over the entire grid, getting each block
        # one at a time.
        for x in range(self.size):
            for z in range(self.size):
                self.grid.set(x, z, self.conn.getBlock(
                    self.x + x, self.y, self.z + z))
        self.conn.postToChat("Running simulation")
        print "Starting similation, hit CTRL-C to stop"
        try:
            while True:
                new_grid = self.step(self.grid)
                for x in range(self.size):
                    for z in range(self.size):
                        if (new_grid.get(x, z) != self.grid.get(x, z)):
                            # Only update if things have changed
                            self.conn.setBlock(self.x + x, self.y, self.z + z,
                                               new_grid.get(x, z))
                self.grid = new_grid
        except KeyboardInterrupt:
            self.conn.postToChat("Stopping simulation")
