import os
import glob

from lib import config
from lib.site_config import SiteConfig


def get_config():
    beat_config = {}
    sites = fetch_sites()
    for site in sites:
        beat_config[site] = build_site_config(site)

    return beat_config


def get_site_path():
    config_dir = config.CONFIG_DIR
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../',
            config_dir,
        )
    )


def fetch_sites():
    config_path = get_site_path()
    glob_regex = os.path.join(config_path, '*.yml')
    config_files = glob.glob(glob_regex)
    return map(get_site_name, config_files)


def get_site_name(site_path):
    site_name = os.path.basename(site_path)
    return site_name.split('.')[0]


def build_site_config(site_name):
    config_path = get_site_path()
    site_config_path = os.path.join(config_path, f'{site_name}.yml')

    site_config = SiteConfig.from_yml(site_config_path)
    periodicity = float(site_config.get('periodicity', 30))
    return {
        'task': 'async.crawlers.crawl',
        'schedule': periodicity,
        'args': (site_name,)
    }
