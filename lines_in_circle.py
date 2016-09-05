# -*- coding: utf-8 -*-

import sys
import pytest
import matplotlib.pyplot as plt

from math import sqrt


def get_new_vectors(radius, vector_one, vector_two, distance, operation):
    """Get vectors that form parallel line inside a circle

    1. Getting orthogonal distance vector (unitary orthogonal vector*distance)
    2. Adding or subtracting the orthogonal distance vector to original vector
    3. Intersecting new vectors with circle
    """
    #
    # TODOs:
    # - There should be a check so that the desired distance is
    #   not larger than maximum distance from the line to the circle
    #
    if distance > radius:
        raise ValueError(
            ("Incompatible radius ({}) and distance ({}); " +
             "the new lines would be outside the circle.").format(
                 radius, distance
             )
        )
    orthogonal_distance_vector = get_orthogonal_distance_vector(
        vector_one,
        vector_two,
        distance
    )
    new_vector_one = (
        operation(vector_one[0], orthogonal_distance_vector[0]),
        operation(vector_one[1], orthogonal_distance_vector[1])
    )
    new_vector_two = (
        operation(vector_two[0], orthogonal_distance_vector[0]),
        operation(vector_two[1], orthogonal_distance_vector[1])
    )
    new_vectors = get_vector_intersection_with_circle(
        radius,
        new_vector_one,
        new_vector_two
    )
    return(new_vectors)


def get_orthogonal_distance_vector(vector_one, vector_two, distance):
    """Get orthogonal distance vector given two vectors that specify a line

    To do so we:
    1. Get the an orthogonal vector
    2. Make the orthogonal vector unitary
    3. Multiply orthogonal vector by distance
    """
    orthogonal_vector = get_orthogonal_vector(vector_one, vector_two)
    unitary_orthogonal_vector = make_unitary_vector(orthogonal_vector)
    distance_vector = (
        unitary_orthogonal_vector[0]*distance,
        unitary_orthogonal_vector[1]*distance,
    )
    return(distance_vector)


def get_orthogonal_vector(vector_one, vector_two):
    """Get orthogonal vector by simple method for R^2"""
    aux_vector = (
        vector_two[0] - vector_one[0],
        vector_two[1] - vector_one[1]
    )
    orthogonal_vector = [0, 0]
    orthogonal_vector[0] = -aux_vector[1]
    orthogonal_vector[1] = aux_vector[0]
    return(tuple(orthogonal_vector))


def make_unitary_vector(vector):
    """Divide a vector by its norm to make it unitary"""
    euclidian_norm = sqrt(
        vector[0]*vector[0] +
        vector[1]*vector[1]
    )
    normalized_vector = (
        vector[0]/euclidian_norm,
        vector[1]/euclidian_norm
    )
    return(normalized_vector)


def get_vector_intersection_with_circle(r, vector_one, vector_two):
    """Solve quadratic equation to find line-circle intersections

    x = (-ab +- sqrt(a^2*b^2 - 4*(a^2 - r^2)*b^2))/(2*(a^2 - r^2))

    where a (intercept) and b (slope) come from `y = a + xb`
    (the line equation), and r (radius) comes from
    `r^2 = x^2 + y^2` (the circle equation).
    """
    if infinite_slope(vector_one, vector_two):
        x_one = vector_one[0]
        x_two = vector_two[0]

        y_one = sqrt(r*r - x_one*x_one)
        y_two = -sqrt(r*r - x_two*x_two)
    else:
        (a, b) = get_line_parameters(vector_one, vector_two)

        A = a*a - r*r
        B = 2*a*b
        C = b*b + 1

        x_one = (-B + sqrt(B*B - 4*A*C))/(2*(b*b + 1))
        x_two = (-B - sqrt(B*B - 4*A*C))/(2*(b*b + 1))

        y_one = a + x_one*b
        y_two = a + x_two*b

    new_vector_one = (x_one, y_one)
    new_vector_two = (x_two, y_two)
    return((new_vector_one, new_vector_two))


def get_line_parameters(vector_one, vector_two):
    """Get (a, b) from `y = a + xb` given two vectors for the line"""
    b = get_slope(vector_one, vector_two)
    a = vector_one[1] - vector_one[0]*b
    return((a, b))


def get_slope(vector_one, vector_two):
    """Get the slope of a line specified by two vectors"""
    return(vector_two[1] - vector_one[1])/(vector_two[0] - vector_one[0])


def infinite_slope(vector_one, vector_two):
    """Check if provided vectors for line imply an infinite slope"""
    return(vector_one[0] == vector_two[0])


def add(one, two):
    """Helper function for adding"""
    return(one + two)


def subtract(one, two):
    """Helper function for subtracting"""
    return(one - two)


def print_circle_PNG(radius,
                     vector_one,
                     vector_two,
                     lower_vectors,
                     higher_vectors):
    """Helper function for graphing"""
    space = 1
    fig, ax = plt.subplots()
    ax.set_xlim((-(radius + space), radius + space))
    ax.set_ylim((-(radius + space), radius + space))

    circle_1 = plt.Circle((0, 0), radius, edgecolor='black', facecolor='none')
    ax.add_artist(circle_1)

    plt.plot(
        [vector_one[0], vector_two[0]],
        [vector_one[1], vector_two[1]],
        color="red"
    )
    plt.plot(
        [lower_vectors[0][0], lower_vectors[1][0]],
        [lower_vectors[0][1], lower_vectors[1][1]],
        color="blue"
    )
    plt.plot(
        [higher_vectors[0][0], higher_vectors[1][0]],
        [higher_vectors[0][1], higher_vectors[1][1]],
        color="green"
    )

    plt.grid(True)

    fig.savefig('plot.png')


def main(arguments):

    radius = float(arguments[0])
    point_one = float(arguments[1])
    point_two = float(arguments[2])
    point_three = float(arguments[3])
    point_four = float(arguments[4])
    distance = float(arguments[5])

    vector_one = (point_one, point_two)
    vector_two = (point_three, point_four)

    lower_vectors = get_new_vectors(
        radius,
        vector_one,
        vector_two,
        distance,
        subtract
    )
    higher_vectors = get_new_vectors(
        radius,
        vector_one,
        vector_two,
        distance,
        add
    )

    print("Lower  vector one: ({}, {})".format(
        lower_vectors[0][0], lower_vectors[0][1]
    ))
    print("Lower  vector two: ({}, {})".format(
        lower_vectors[1][0], lower_vectors[1][1]
    ))
    print("Higher vector one: ({}, {})".format(
        higher_vectors[0][0], higher_vectors[0][1]
    ))
    print("Higher vector two: ({}, {})".format(
        higher_vectors[1][0], higher_vectors[1][1]
    ))

    print_circle_PNG(
        radius,
        vector_one,
        vector_two,
        lower_vectors,
        higher_vectors
    )


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


def close_enough(vector_one, vector_two):
    """Check that the values for vectors are close enough (< 0.1)"""
    for i in range(len(vector_one)):
        for j in range(len(vector_one[i])):
            if vector_one[i][j] - vector_two[i][j] > 0.1:
                return(False)
    return(True)


@pytest.mark.parametrize(
    "radius, vector_one, vector_two, distance, lower_vectors",
    [
        (2, (1, 1.73), (-2, 0), 0.5, ((0.39, 1.96), (-1.89, 0.63))),
        (2, (1, 1.73), (-2, 0), 1,   ((-0.94, 1.76), (-1.05, 1.70))),
        (2, (0, -2), (0, 2), 1, ((1, 1.73), (1, -1.73))),
        (2, (0, -2), (0, 2), 0.1, ((0.1, 1.99), (0.1, -1.99)))
    ]
)
def test_get_lower_vectors(radius,
                           vector_one,
                           vector_two,
                           distance,
                           lower_vectors):
    our_lower_vectors = get_new_vectors(
        radius,
        vector_one,
        vector_two,
        distance,
        subtract
    )
    assert close_enough(our_lower_vectors, lower_vectors)
