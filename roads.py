import os
import argparse
import json
import secrets
from dataclasses import asdict, dataclass

import modeler
import logger
from util import prompt_forever, read_text, read_float, read_choices


_logger = logger.get_logger('roads')
DEFAULT_FILE = 'roads.json'


@dataclass
class RoadAttributes:
    road_name: str
    trafficable: float
    condition: float
    pitstop_condition: float
    weight: float = None

    default_weights = {
        'trafficable': 20,
        'condition': 10,
        'pitstop_condition': 5
    }

    def __post_init__(self):
        first_op = 0
        for param in self.default_weights.keys():
            value = getattr(self, param)
            first_op += value * self.default_weights[param]
        self.weight = first_op / sum(self.default_weights.values())


def read_road(io_wrapper):
    content = json.load(io_wrapper)
    io_wrapper.close()

    road_attrs = []
    for road in content:
        road_attrs.append(RoadAttributes(**road))
    return road_attrs


def roads_to_dict(roads):
    new_list = []
    for road in roads:
        new_list.append(asdict(road))
    return new_list 


def mount_road():
    kwargs = dict()
    road_name = read_text('Road name', 
                            max_attempts=1,
                            throlling_message='Creating a random name')
    if not road_name:
        road_name = secrets.token_hex(6)
    kwargs['road_name'] = road_name

    kwargs['trafficable'] = read_float('Road is trafficable',
                            max_attempts=1,
                            default=1.0,
                            throlling_message='Assuming road is trafficable')
    kwargs['condition'] = read_float('Road condition',
                            max_attempts=1,
                            default=1.0,
                            throlling_message='Assuming road condition is good')
    kwargs['pitstop_condition'] = read_float('Road pitstop',
                                max_attempts=1,
                                default=1.0,
                                throlling_message='Assuming road condition has a good pitstop')
    return RoadAttributes(**kwargs)


def create_roads():
    road_attrs = []
    try:
        while True:
            road = prompt_forever('This info sounds good?', mount_road)
            _logger.debug('recv road: %s', road)
            road_attrs.append(road)
    except KeyboardInterrupt as exc:
        print('[+] User interrrupted!')
        if read_choices('Continue and save', ['yes', 'no']) == 1:
            raise exc
    return road_attrs


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', help='Be moderatly verbose.',
                        default=False, action='store_true')

    return parser.parse_args()


def load_from_file():
    if os.path.exists(DEFAULT_FILE):
        return read_road(open(DEFAULT_FILE))


def dump_roads(roads):
    modeler.dump_class(DEFAULT_FILE, roads, dict_impl=roads_to_dict)


def main():
    args = parse_arguments()
    
    logger.setup(debug=args.verbose)
    
    road_attrs = load_from_file()

    if road_attrs is None:
        road_attrs = create_roads()
    else:
        _logger.debug('loaded road from file: %s', road_attrs)
        new_roads = create_roads()
        road_attrs.extend(new_roads)
    dump_roads(road_attrs)


if __name__ == '__main__':
    main()
