import json
import logging


class Graph:
    def __init__(self, neighbours):
        self.neighbours = neighbours

    def __str__(self):
        res = f"Graph: "
        for region in self.neighbours:
            res += f"\n{region}: "
            for neighbour in self.neighbours[region]:
                res += f"{neighbour}, "

        return res

    def __eq__(self, other):
        return self.neighbours == other.neighbours

    def __hash__(self):
        return hash(self.neighbours)

    def to_json(self, plane_size, save_filepath, colors=None):
        js = {
            "board": plane_size,
            "regions": [[region.x, region.y] for region in self.neighbours],
            "colors": colors if colors else [1] * len(self.neighbours),
            "connections": []
        }

        for region in self.neighbours:
            neighbours = []
            for neighbour in self.neighbours[region]:
                neighbours.append(list(self.neighbours.keys()).index(neighbour))
            js["connections"].append(neighbours)

        logging.info(f"Saving graph to {save_filepath}")
        with open(save_filepath, 'w') as file:
            json.dump(js, file)
