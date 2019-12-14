import math

def circumference(radius: float) -> float:
    return 2 * math.pi * radius

print(circumference(1.23))

print(circumference.__annotations__)