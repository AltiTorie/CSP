import logging
import random
from collections import defaultdict

from shapely.geometry import LineString, Point

from utils.graph import Graph
from utils.region import Region


def generate_graph(num_of_regions, plane_size):
    logging.info(f"Generating graph of {num_of_regions} regions on a {plane_size}x{plane_size} plane")
    regions = random_regions(num_of_regions, plane_size, )
    graph = connect_regions_as_graph(regions)
    return graph


def random_regions(num_of_regions, plane_size):
    regions = []
    for _ in range(num_of_regions):
        x = random.randint(0, plane_size - 1)
        y = random.randint(0, plane_size - 1)
        region = Region(x, y)
        if region not in regions:
            regions.append(region)
    return regions


def get_existing_lines(graph):
    existing_lines = []
    for region in graph.neighbours:
        for neighbour in graph.neighbours[region]:
            existing_lines.append(LineString(
                [(region.x, region.y), (neighbour.x, neighbour.y)]))
    return existing_lines


def possible_connection_exists(regions, graph: Graph):
    if not graph.neighbours:
        return True
    existing_lines = get_existing_lines(graph)

    for region in regions:
        other_regions = regions.copy()
        other_regions.remove(region)
        for other_region in other_regions:
            if other_region not in graph.neighbours[region]:
                new_line = LineString(
                    [(region.x, region.y), (other_region.x, other_region.y)])

                if __not_intersecting(existing_lines, new_line, region, other_region):
                    return True
    return False


def __not_intersecting(existing_lines, line_to_check, region, other_region):
    not_intersecting = True
    for line in existing_lines:
        intersection = line_to_check.intersection(line)
        if type(intersection) is LineString:
            if intersection.length > 0:
                not_intersecting = False
                break
        if type(intersection) is Point:
            intersection_x = intersection.xy[0][0]
            intersection_y = intersection.xy[1][0]
            if not (intersection_x == region.x and intersection_y == region.y) and not (
                    intersection_x == other_region.x and intersection_y == other_region.y):
                not_intersecting = False
                break
    return not_intersecting


def connect_regions_as_graph(regions):
    graph = Graph(defaultdict(list))
    existing_lines = []
    regions_distance_sorted = get_regions_distances_sorted(regions)

    while possible_connection_exists(regions, graph):
        region_to_connect = random.choice(regions)

        for region in regions_distance_sorted[region_to_connect]:
            if region in graph.neighbours[region_to_connect]:
                continue
            new_line = LineString(
                [(region.x, region.y), (region_to_connect.x, region_to_connect.y)])

            if __not_intersecting(existing_lines, new_line, region, region_to_connect):
                graph.neighbours[region_to_connect].append(region)
                graph.neighbours[region].append(region_to_connect)
                existing_lines.append(new_line)
                break

    return graph


def get_regions_distances_sorted(regions):
    distances = {}
    for region in regions:
        other_regions = regions.copy()
        other_regions.remove(region)
        other_regions.sort(
            key=lambda r: (r.x - region.x) ** 2 + (r.y - region.y) ** 2)
        distances[region] = other_regions
    return distances
