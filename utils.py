# utils.py
def chunk_text(lines, size):
    for i in range(0, len(lines), size):
        yield lines[i:i+size]
