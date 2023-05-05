from geopy import distance


def get_distance(point_a: tuple, point_b: tuple):
    dist = round(distance.great_circle(point_a, point_b).km, 2)
    return dist


if __name__ == "__main__":
    print(get_distance((51, 34), (-5, 100)))