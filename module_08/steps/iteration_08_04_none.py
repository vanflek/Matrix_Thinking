# An action and a returned value are different things.
def show_rules(target_count):
    print(f"Collect {target_count} targets.")
    print("Use the arrow keys to change direction.")
    print("Visit every target to win.")

result = show_rules(3)
print(result)
