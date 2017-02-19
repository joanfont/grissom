import yaml
from crawler import filters

from urllib.parse import urlencode


class Base:
    SITE = None
    FILTER_CLASS = None

    def __init__(self):
        self.config = self.get_site_config()
        self.check_config()

    def generate(self):
        raise NotImplementedError()

    def check_config(self):
        assert self.config.get('url', {}).get('base') is not None

    def append_to_base(self, path):
        base = self.base_url
        return f'{base}{path}'

    def get_site_config(self):
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config

    @property
    def config_file(self):
        return f'config/{self.SITE}.yml'

    @property
    def base_url(self):
        return self.config.get('url').get('base')

    @property
    def template_url(self):
        path = self.config.get('url').get('path')
        return self.append_to_base(path)


class Fotocasa(Base):
    SITE = 'fotocasa'
    FILTER_CLASS = filters.Fotocasa

    def generate(self):
        zones = self.config.get('zones')
        for zone in zones:
            yield self._generate_zone_url(zone)

    def _generate_zone_url(self, zone):
        base_url = self.template_url
        zone_slug = self.config.get('zones', {}).get(zone)
        url = base_url.format(zone=zone_slug)

        zone_filters = self.config.get('filters', {}).get(zone)
        if zone_filters:
            url = self._add_filters_to_url(url, zone_filters)

        return url

    def _add_filters_to_url(self, url, zone_filters):
        filter_instance = self.FILTER_CLASS.from_yml(**zone_filters)
        filters_dict = filter_instance.to_dict()
        query_string = urlencode(filters_dict)
        return f'{url}?{query_string}'


class Factory:
    SITES = {
        Fotocasa.SITE: Fotocasa,
    }

    @classmethod
    def build(cls, site):
        builder_class = cls.SITES.get(site)
        if not builder_class:
            return None

        return builder_class()
