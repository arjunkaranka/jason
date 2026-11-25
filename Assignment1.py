
import heapq

# Goal state
goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

N = 3

# Calculate Manhattan Distance
def heuristic(state):
    distance = 0

    for i in range(N * N):
        if state[i] != 0:
            goal_pos = state[i] - 1

            x1, y1 = i // N, i % N
            x2, y2 = goal_pos // N, goal_pos % N

            distance += abs(x1 - x2) + abs(y1 - y2)

    return distance


# Generate possible moves
def get_neighbors(state):
    neighbors = []

    zero = state.index(0)
    x, y = zero // N, zero % N

    moves = [(-1, 0), (1, 0),
             (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        if 0 <= nx < N and 0 <= ny < N:
            new_pos = nx * N + ny

            new_state = list(state)
            new_state[zero], new_state[new_pos] = (
                new_state[new_pos], new_state[zero]
            )

            neighbors.append(tuple(new_state))

    return neighbors


# A* Search Algorithm
def solve(start):
    pq = []
    heapq.heappush(pq, (heuristic(start), 0, start))

    visited = {start: 0}
    parent = {start: None}

    while pq:
        f, g, current = heapq.heappop(pq)

        if current == goal:
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        if g != visited[current]:
            continue

        for neighbor in get_neighbors(current):
            new_g = g + 1

            if neighbor not in visited or new_g < visited[neighbor]:
                visited[neighbor] = new_g
                parent[neighbor] = current

                new_f = new_g + heuristic(neighbor)
                heapq.heappush(pq, (new_f, new_g, neighbor))

    return None


# Take initial state from user
print("Enter the initial state (0 represents blank space):")

start = tuple(map(int, input().split()))

# Validate input
if len(start) != 9 or set(start) != set(range(9)):
    print("Invalid input! Enter numbers from 0 to 8 exactly once.")

else:
    # Solve puzzle
    solution = solve(start)

    # Display solution
    if solution:
        print("\nSolution found!")
        print("Total moves:", len(solution) - 1)

        for step in solution:
            for i in range(N):
                print(step[i*N:(i+1)*N])
            print()
    else:
        print("No solution exists")
