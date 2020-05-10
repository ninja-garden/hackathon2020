import json
from PIL import Image

import click

from processor import Processor

@click.command()
@click.option('-c', '--config', 'config_path', required=True, type=click.Path(exists=True, readable=True))
@click.option('-i', '--image', 'image_path', required=True, type=click.Path(exists=True, readable=True))
@click.option('--north', required=True, type=float)
@click.option('--south', required=True, type=float)
@click.option('--west', required=True, type=float)
@click.option('--east', required=True, type=float)
def main(config_path, image_path, north, south, west, east):
    with open(config_path, 'rt') as f:
        config = json.load(f)
    with open(image_path, 'rb') as f:
        image = Image.open(image_path)

    proc = Processor(config)
    info = proc(image, north, south, west, east)
    print(info)

if __name__ == '__main__':
    main()
