# A list used as a stack: the last appended cell is processed first.
stack = []
stack.append((1, 1))
stack.append((1, 2))
stack.append((2, 2))

print(stack.pop())
print(stack)

while stack:
    print(stack.pop())

print(len(stack))

# A set stores each discovered coordinate only once.
visited = set()
visited.add((1, 2))
visited.add((1, 2))

print(len(visited))
print((1, 2) in visited)
print((2, 2) in visited)
print((2, 2) not in visited)

# Mark a coordinate as discovered when scheduling it for processing.
start = (1, 1)
stack = [start]
visited = {start}

for neighbor in [(1, 2), (1, 2), (2, 1)]:
    if neighbor not in visited:
        visited.add(neighbor)
        stack.append(neighbor)

print(stack)
print(len(visited))
