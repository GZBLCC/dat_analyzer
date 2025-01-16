with open('modified.dat', 'rb') as f:
    f.seek(2)
    byte = f.read(1)
    print(f"Offset 2 value: 0x{byte.hex().upper()}")