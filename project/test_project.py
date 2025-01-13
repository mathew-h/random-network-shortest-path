import pytest
import math
from project.project import generate_coordinates, calculate_distance

def test_generate_coordinates_n_zero():
    with pytest.raises(ValueError, match="n cannot be 0"):
        generate_coordinates(0, 5)  # n=0 should raise an error

def test_calculate_distance():
    assert calculate_distance((0,0), (0,0)) == 0
    assert calculate_distance((0,0), (0,5)) == 5

def test_calculate_distance_edge_case():
    # Very large coordinates
    coord1 = (1e10, 1e10)
    coord2 = (1e10 + 1, 1e10 + 1)

    result = calculate_distance(coord1, coord2)

    expected_distance = math.dist(coord1, coord2)  # Calculate expected distance using math.dist
    assert result == expected_distance, f"Expected distance {expected_distance}, but got {result}"

def test_calculate_distance_same_coordinates():
    coord1 = (0.0, 0.0)
    coord2 = (0.0, 0.0)

    result = calculate_distance(coord1, coord2)

    assert result == 0.0, f"Expected distance to be 0.0, but got {result}"

# def test_function_n():
#     ...
