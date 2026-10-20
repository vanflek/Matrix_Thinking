numbers = [10, 20, 30, 40]
removed = {20, 40}
remaining = []
for number in numbers:
    if number not in removed:
        remaining.append(number)
print(remaining)
remaining = [number for number in numbers if number not in removed]
print(remaining)
