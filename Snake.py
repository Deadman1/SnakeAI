from enum import Enum
import numpy as np
from collections import deque

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

ACTION = {
    'CONTINUE': 0,
    'LEFT': 1,
    'RIGHT': 2
}

class Snake(object):
    
    def __init__(self, initial_head):
        self.head = initial_head
        self.body = deque([(self.head[0], self.head[1]+1), self.head])
        self.curr_dir = Direction.UP 

    def update_position(self, new_head):
        if new_head == self.body[-1]:
            return
        self.body.popleft()
        self.body.append(new_head)
        self.head = new_head

    def perform_action(self, action, food):
        # Move body accordingly.
        if self.curr_dir == Direction.UP or self.curr_dir == Direction.DOWN:
            dx, dy = (-1, 0) if action == ACTION['LEFT'] else (1, 0) if action == ACTION['RIGHT'] else (0, -1)
            dx = dx * 1 if self.curr_dir == Direction.UP else dx * -1
            dy = dy * 1 if self.curr_dir == Direction.UP else dy * -1
            if self.curr_dir == Direction.UP:
                self.curr_dir = Direction.LEFT if action == ACTION['LEFT'] else  Direction.RIGHT
            else:
                self.curr_dir = Direction.RIGHT if action == ACTION['LEFT'] else  Direction.LEFT
        else:
            dx, dy = (0, -1) if action == ACTION['LEFT'] else (0, 1) if action == ACTION['RIGHT'] else (1,0)
            dx = dx * 1 if self.curr_dir == Direction.RIGHT else dx * -1
            dy = dy * 1 if self.curr_dir == Direction.RIGHT else dy * -1
            if self.curr_dir == Direction.LEFT:
                self.curr_dir = Direction.DOWN if action == ACTION['LEFT'] else  Direction.UP
            else:
                self.curr_dir = Direction.UP if action == ACTION['LEFT'] else  Direction.DOWN

        x = self.head[0] + dx
        y = self.head[1] + dy
        if food == (x, y):
            self.body.append(food)
            self.head = food
            return True
        else:
            self.update_position((x, y))
            return False