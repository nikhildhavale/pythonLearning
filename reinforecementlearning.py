import pygame
import random
import os
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from enum import Enum
from collections import namedtuple, deque
import matplotlib.pyplot as plt

# COMMENTED OUT TO PREVENT ERROR ON WINDOWS
# from IPython import display

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)

# ==========================================
# 1. SETTINGS & CONSTANTS
# ==========================================
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# Game Settings
BLOCK_SIZE = 20
SPEED = 80  # Speed of the game

# ==========================================
# 2. THE GAME ENGINE
# ==========================================
class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI - Deep Q Learning')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.episode = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # DISTANCE CALCULATION (Before Move)
        head = self.snake[0]
        dist_before = math.sqrt((head.x - self.food.x)**2 + (head.y - self.food.y)**2)

        # MOVE
        self._move(action) 
        self.snake.insert(0, self.head)
        
        # DISTANCE CALCULATION (After Move)
        head_new = self.snake[0]
        dist_after = math.sqrt((head_new.x - self.food.x)**2 + (head_new.y - self.food.y)**2)

        # CHECK GAME OVER
        reward = 0
        game_over = False
        
        # Starvation Logic: Die if haven't eaten in 100 frames
        if self.is_collision() or self.frame_iteration > 100:
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # CHECK FOOD
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            self.frame_iteration = 0 # Reset Starvation Timer
        else:
            self.snake.pop()
            # Reward Shaping: Give small hint for moving closer
            if dist_after < dist_before:
                reward = 0.1 
            else:
                reward = -0.1 
        
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render(f"Episode: {self.episode}  Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else: 
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

# ==========================================
# 3. THE BRAIN (3-Layer Neural Net)
# ==========================================
class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, int(hidden_size / 2)) # Extra hidden layer
        self.linear3 = nn.Linear(int(hidden_size / 2), output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

# ==========================================
# 4. THE AGENT (Flood Fill + Logic)
# ==========================================
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9 
        self.memory = deque(maxlen=MAX_MEMORY) 
        
        # 14 Inputs: 11 Standard + 3 Trap Detectors
        self.model = Linear_QNet(14, 256, 3) 
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # --- FLOOD FILL ALGORITHM (Trap Detection) ---
    def is_trap(self, game, point):
        obstacles = set()
        for p in game.snake:
            obstacles.add((int(p.x), int(p.y)))
            
        start_node = (int(point.x), int(point.y))
        
        # Collision check
        if (start_node in obstacles or 
            point.x < 0 or point.x >= game.w or 
            point.y < 0 or point.y >= game.h):
            return True 
            
        queue = deque([start_node])
        visited = {start_node}
        count = 0
        limit = len(game.snake) # We only care if free space > snake length
        
        while queue:
            cx, cy = queue.popleft()
            count += 1
            if count > limit: 
                return False # Safe: Accessible area is larger than snake
            
            neighbors = [
                (cx + BLOCK_SIZE, cy), (cx - BLOCK_SIZE, cy),
                (cx, cy + BLOCK_SIZE), (cx, cy - BLOCK_SIZE)
            ]
            
            for nx, ny in neighbors:
                if (nx, ny) not in visited and (nx, ny) not in obstacles:
                    if 0 <= nx < game.w and 0 <= ny < game.h:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        
        return True # Trap detected

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # Trap Logic
        pt_straight, pt_right, pt_left = Point(0,0), Point(0,0), Point(0,0)
        
        if dir_r:
            pt_straight, pt_right, pt_left = point_r, point_d, point_u
        elif dir_l:
            pt_straight, pt_right, pt_left = point_l, point_u, point_d
        elif dir_u:
            pt_straight, pt_right, pt_left = point_u, point_r, point_l
        elif dir_d:
            pt_straight, pt_right, pt_left = point_d, point_l, point_r

        is_trap_straight = self.is_trap(game, pt_straight)
        is_trap_right = self.is_trap(game, pt_right)
        is_trap_left = self.is_trap(game, pt_left)

        state = [
            # Danger Straight, Right, Left
            (dir_r and game.is_collision(point_r)) or (dir_l and game.is_collision(point_l)) or (dir_u and game.is_collision(point_u)) or (dir_d and game.is_collision(point_d)),
            (dir_u and game.is_collision(point_r)) or (dir_d and game.is_collision(point_l)) or (dir_l and game.is_collision(point_u)) or (dir_r and game.is_collision(point_d)),
            (dir_d and game.is_collision(point_r)) or (dir_u and game.is_collision(point_l)) or (dir_r and game.is_collision(point_u)) or (dir_l and game.is_collision(point_d)),
            
            # Directions
            dir_l, dir_r, dir_u, dir_d,
            
            # Food Location
            game.food.x < game.head.x, 
            game.food.x > game.head.x, 
            game.food.y < game.head.y, 
            game.food.y > game.head.y,

            # NEW: Trap Inputs
            is_trap_straight,
            is_trap_right,
            is_trap_left
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Min Epsilon 1% to prevent getting stuck
        self.epsilon = 80 - self.n_games
        if self.epsilon < 1: self.epsilon = 1
        
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

# ==========================================
# 5. PLOTTING & MAIN
# ==========================================
def plot(scores, mean_scores):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.pause(0.1)

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    
    print("DEBUG: Training started! Game window should appear now...")

    # DISABLE GRAPHING (Ghost Window Fix)
    # plt.ion()
    
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        
        reward, done, score = game.play_step(final_move)
        
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            game.episode = agent.n_games
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(f'Game {agent.n_games}, Score {score}, Record {record}')

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            
            # DISABLE PLOTTING (Ghost Window Fix)
            # plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()