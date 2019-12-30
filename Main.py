from DQN import DQNAgent, MODEL_NAME
from tqdm import tqdm
import numpy as np
import random
import tensorflow as tf
from Game2 import BlobEnv
from Snake import ACTION
import time
import os

# Environment settings
EPISODES = 20_000

# For stats
ep_rewards = [-200]

#  Stats settings
AGGREGATE_STATS_EVERY = 50  # episodes
SHOW_PREVIEW = True

# Exploration settings
# epsilon = 1  # not a constant, going to be decayed
epsilon = 0.00
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001

# For more repetitive results
random.seed(1)
np.random.seed(1)
tf.random.set_seed(1)

MIN_REWARD = -200  # For model save
MEMORY_FRACTION = 0.20

agent = DQNAgent()
env = BlobEnv()

# Create models folder
if not os.path.isdir('models'):
    os.makedirs('models')

# Iterate over episodes
for episode in tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):

    # Update tensorboard step every episode
    agent.tensorboard.step = episode

    # Restarting episode - reset episode reward and step number
    episode_reward = 0
    step = 1

    # Reset environment and get initial state
    current_state = env.reset()

    # Reset flag and start iterating until episode ends
    done = False
    while not done:

        # This part stays mostly the same, the change is to query a model for Q values
        if np.random.random() > epsilon:
            # Get action from Q table
            action = np.argmax(agent.get_qs(current_state))
        else:
            # Get random action
            action = np.random.randint(0, env.ACTION_SPACE_SIZE)

        new_state, reward, done = env.step(action)

        # Transform new continous state to new discrete state and count reward
        episode_reward += reward

        if SHOW_PREVIEW:# and not episode % AGGREGATE_STATS_EVERY:
            env.render()

        # Every step we update replay memory and train main network
        agent.update_replay_memory((current_state, action, reward, new_state, done))
        agent.train(done, step)

        current_state = new_state
        step += 1

    # Append episode reward to a list and log stats (every given number of episodes)
    ep_rewards.append(episode_reward)
    if not episode % AGGREGATE_STATS_EVERY or episode == 1:
        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:])/len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, epsilon=epsilon)

    # Save model, but only when min reward is greater or equal a set value
    if episode % 50 == 0:
        agent.model.save(f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

    if len(env.snake.body) > 2:    
        print("   Episode: {0}      Score: {1}".format(episode, len(env.snake.body)))
    # Decay epsilon
    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)