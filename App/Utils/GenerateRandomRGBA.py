import random

def generate_random_rgba() -> str:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = round(random.uniform(0.5, 1), 2)
    return f"rgba({r}, {g}, {b}, {a})"
