with open('direct_modified.dat', 'rb') as f:
    f.seek(2)
    byte = f.read(1)
    print(f"Offset 2 value in direct_modified.dat: 0x{byte.hex().upper()}")