# This experiment intentionally raises ValueError before the loop body runs.
# Change the step from 0 to 1, then run the file again.
for number in range(0, 5, 0):
    print(number)
