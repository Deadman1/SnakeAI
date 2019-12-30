from enum import Enum
from Snake import Snake, ACTION
from random import randint
import numpy as np
from PIL import Image
import cv2

class BlobEnv:
    SIZE = 12
    MOVE_PENALTY = -1
    ENEMY_PENALTY = -5
    FOOD_REWARD = 10
    OBSERVATION_SPACE_VALUES = (SIZE, SIZE, 3)  # 4
    ACTION_SPACE_SIZE = len(ACTION.keys())
    SNAKE_N = 1  # snake key in dict
    FOOD_N = 2  # food key in dict
    WALL_N = 3  # wall key in dict
    SNAKE_HEAD_N = 4  # wall key in dict
    # the dict! (colors)
    d = {1: (255, 175, 0),
         2: (0, 255, 0),
         3: (0, 0, 255),
         4: (0, 255, 255)}

    def spawn_new_food(self):
        x = randint(1, self.SIZE-2)
        y = randint(1, self.SIZE-2)
        if (x, y) not in self.snake.body:
            return (x, y)
        else:
            return self.spawn_new_food()


    def reset(self):
        self.episode_step = 0
        self.snake = Snake((int(0.45 * BlobEnv.SIZE), int(0.5 * BlobEnv.SIZE)))
        self.food = self.spawn_new_food()
        self.walls = []
        for i in range(BlobEnv.SIZE):
            self.walls.append((i,0))
            self.walls.append((i, BlobEnv.SIZE-1))
            self.walls.append((BlobEnv.SIZE-1, i))
            self.walls.append((0, i))

        return np.array(self.get_image())

    def step(self, action):
        self.episode_step += 1
        ate_food = self.snake.perform_action(action, self.food)
        if ate_food:
            self.food = self.spawn_new_food()

        done = False
        new_observation = np.array(self.get_image())
        if self.snake.head in self.walls:
            reward = self.ENEMY_PENALTY
            done = True
        elif len([pos for pos in self.snake.body if pos == self.snake.head]) ==2:
            # Ran into the snake
            reward = self.ENEMY_PENALTY
            done = True
        elif self.snake.head == self.food:
            reward = BlobEnv.FOOD_REWARD
        else:
            reward = self.MOVE_PENALTY

        # done = False
        # if reward == self.ENEMY_PENALTY:# or self.episode_step >= 200:
        #     done = True

        return new_observation, reward, done

    def render(self):
        img = self.get_image()
        img = img.resize((300, 300))  # resizing so we can see our agent in all its glory.
        cv2.imshow("image", np.array(img))  # show it!
        cv2.waitKey(200)

    # FOR CNN #
    def get_image(self):
        env = np.full((self.SIZE, self.SIZE, 3), 255, dtype=np.uint8)
        # env = np.zeros((self.SIZE, self.SIZE, 3), dtype=np.uint8)  # starts an rbg of our size
        env[self.food[0]][self.food[1]] = self.d[BlobEnv.FOOD_N]  # sets the food location tile to green color
        for w_x, w_y in self.walls:
            env[w_x][w_y] = self.d[BlobEnv.WALL_N]  # sets the wall location to red
        for s_x, s_y in self.snake.body:
            env[s_x][s_y] = self.d[BlobEnv.SNAKE_N]  # sets the snake tiles to blue
        env[self.snake.head[0]][self.snake.head[1]] = self.d[BlobEnv.SNAKE_HEAD_N]
        img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
        return img