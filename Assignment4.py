
import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 400
HEIGHT = 400
CELL = 20
SIZE = WIDTH // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake - Reinforcement Learning")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Directions: Up, Right, Down, Left
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Q-Learning parameters
alpha = 0.1
gamma = 0.9
epsilon = 1.0
episodes = 2000

# Q-table
Q = {}


# Snake game environment
class SnakeGame:

    def reset(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = 1
        self.food = self.create_food()
        self.score = 0
        self.done = False
        return self.get_state()

    def create_food(self):
        while True:
            food = (random.randint(0, SIZE-1),
                    random.randint(0, SIZE-1))
            if food not in self.snake:
                return food

    def collision(self, position):
        x, y = position

        return (x < 0 or x >= SIZE or
                y < 0 or y >= SIZE or
                position in self.snake[:-1])

    # Get current game state
    def get_state(self):

        head = self.snake[0]
        x, y = head

        straight = self.direction
        right = (self.direction + 1) % 4
        left = (self.direction - 1) % 4

        def danger(d):
            dx, dy = directions[d]
            return self.collision((x + dx, y + dy))

        food_x, food_y = self.food

        state = (
            danger(straight),
            danger(right),
            danger(left),

            self.direction == 0,
            self.direction == 1,
            self.direction == 2,
            self.direction == 3,

            food_x < x,
            food_x > x,
            food_y < y,
            food_y > y
        )

        return tuple(state)

    # Perform action
    def step(self, action):

        # 0 = Straight, 1 = Right, 2 = Left
        if action == 1:
            self.direction = (self.direction + 1) % 4

        elif action == 2:
            self.direction = (self.direction - 1) % 4

        dx, dy = directions[self.direction]

        head = self.snake[0]
        new_head = (head[0] + dx, head[1] + dy)

        if self.collision(new_head):
            self.done = True
            return self.get_state(), -10, True

        self.snake.insert(0, new_head)

        reward = -0.1

        if new_head == self.food:
            self.score += 1
            reward = 10
            self.food = self.create_food()
        else:
            self.snake.pop()

        return self.get_state(), reward, self.done


# Get Q values
def get_q(state):
    if state not in Q:
        Q[state] = np.zeros(3)
    return Q[state]


# Choose action
def choose_action(state, training=True):

    if training and random.random() < epsilon:
        return random.randint(0, 2)

    return int(np.argmax(get_q(state)))


# Train AI agent
game = SnakeGame()

print("Training AI Snake Agent...")

for episode in range(episodes):

    state = game.reset()

    for step in range(500):

        action = choose_action(state)

        next_state, reward, done = game.step(action)

        old_value = get_q(state)[action]
        next_max = np.max(get_q(next_state))

        # Q-Learning formula
        new_value = old_value + alpha * (
            reward + gamma * next_max - old_value
        )

        get_q(state)[action] = new_value

        state = next_state

        if done:
            break

    epsilon = max(0.05, epsilon * 0.995)

print("Training completed!")
print("Total states learned:", len(Q))


# Play using trained AI
state = game.reset()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = choose_action(state, training=False)

    state, reward, done = game.step(action)

    # Draw background
    screen.fill((25, 25, 25))

    # Draw food
    pygame.draw.rect(
        screen, (255, 0, 0),
        (game.food[0]*CELL, game.food[1]*CELL,
         CELL, CELL)
    )

    # Draw snake
    for segment in game.snake:
        pygame.draw.rect(
            screen, (0, 200, 0),
            (segment[0]*CELL, segment[1]*CELL,
             CELL-2, CELL-2)
        )

    # Display score
    score_text = font.render(
        "Score: " + str(game.score), True, (255, 255, 255)
    )

    screen.blit(score_text, (10, 10))

    pygame.display.update()

    clock.tick(10)

    if done:
        print("Game Over!")
        print("Final Score:", game.score)
        running = False

pygame.quit()
