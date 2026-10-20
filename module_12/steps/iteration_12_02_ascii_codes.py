symbols = []
for code in range(32, 127):
    symbol = chr(code)
    symbols.append(symbol)
    print(code, repr(symbol))
print("Printable symbols:", len(symbols))
