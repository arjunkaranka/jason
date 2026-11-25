
# Map Coloring using CSP and Backtracking

# Step 1: Take states as input
n = int(input("Enter number of states: "))

states = []

for i in range(n):
    state = input("Enter state name: ")
    states.append(state)


# Step 2: Take colors as input
c = int(input("\nEnter number of colors: "))

colors = []

for i in range(c):
    color = input("Enter color name: ")
    colors.append(color)


# Step 3: Create adjacency graph
graph = {}

print("\nEnter neighboring states:")

for state in states:
    graph[state] = []

    count = int(input("How many neighbors does " + state + " have? "))

    for j in range(count):
        neighbor = input("Enter neighbor name: ")

        if neighbor not in states:
            print("Invalid state! Enter again.")
            neighbor = input("Enter valid neighbor name: ")

        graph[state].append(neighbor)


# Step 4: Check whether color is safe
def is_safe(state, color, assignment):

    for neighbor in graph[state]:

        if neighbor in assignment:
            if assignment[neighbor] == color:
                return False

    return True


# Step 5: Backtracking algorithm
def backtracking(assignment):

    if len(assignment) == len(states):
        return True

    # Select unassigned state
    state = next(s for s in states if s not in assignment)

    for color in colors:

        if is_safe(state, color, assignment):

            assignment[state] = color

            if backtracking(assignment):
                return True

            # Backtrack
            del assignment[state]

    return False


# Step 6: Display result
assignment = {}

if backtracking(assignment):

    print("\nMap Coloring Solution:")

    for state in states:
        print(state, ":", assignment[state])

else:
    print("\nNo solution exists!")
