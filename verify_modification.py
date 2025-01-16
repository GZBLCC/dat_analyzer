with open('modified.dat', 'rb') as f:
    data = f.read()
    print("Modified file content in hex:")
    print(' '.join(f'{b:02X}' for b in data))