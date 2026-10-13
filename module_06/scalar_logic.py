row = 0
col = 3

on_top = row == 0
on_left = col == 0

print(on_top or on_left)
print(on_top and on_left)

row = 2
on_top = row == 0

print(on_top)
print(not on_top)

has_key = False
knows_code = True
alarm_on = False

can_unlock = has_key or knows_code
can_open = can_unlock and not alarm_on

print(can_open)

can_open = (has_key or knows_code) and not alarm_on
print(can_open)
