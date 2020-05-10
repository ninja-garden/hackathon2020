import click
import json

from util import RegistryRequester

@click.command()
@click.option('--lat', required=True, type=float)
@click.option('--lon', required=True, type=float)
@click.option('--headless', default=False, is_flag=True)
@click.option('--driver', default='', type=str)
def main(lat, lon, headless, driver):
    if not driver:
        registry = RegistryRequester(headless=headless)
    else:
        registry = RegistryRequester(driver, headless=headless)

    result = registry.is_home(lat, lon)

    print(json.dumps(result).encode('utf-8').decode('utf-8'))

if __name__ == '__main__':
    main()
