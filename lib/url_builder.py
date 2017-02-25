
from lib.filters import Factory as FilterFactory
from lib import config
from lib.site_config import SiteConfig


class Base:
    SITE = None

    def __init__(self):
        self.config = self.get_site_config()
        self.filter_builder = FilterFactory.build(self.SITE)
        self.check_config()

    def generate(self):
        zones = self.config.get('zones')
        if not zones:
            return self.generate_simple_url()

        return self.generate_zone_urls(zones)

    def generate_simple_url(self):
        yield self.template_url

    def generate_zone_urls(self, zones):
        for zone in zones:
            yield self.generate_zone_url(zone)

    def generate_zone_url(self, zone):
        base_url = self.template_url
        zone_slug = self.config.get('zones', {}).get(zone)
        url = base_url.format(zone=zone_slug)

        zone_filters = self.config.get('filters', {}).get(zone)
        if zone_filters:
            url = self.combine_with_filters(url, zone_filters)

        return url

    def combine_with_filters(self, url, zone_filters):
        raise NotImplementedError()

    def check_config(self):
        assert self.config.get('url', {}).get('base') is not None

    def append_to_base(self, path):
        base = self.base_url
        return f'{base}{path}'

    def get_site_config(self):
        return SiteConfig.from_yml(self.config_file)

    @property
    def config_file(self):
        config_dir = config.CONFIG_DIR
        return f'{config_dir}/{self.SITE}.yml'

    @property
    def base_url(self):
        return self.config.get('url').get('base')

    @property
    def template_url(self):
        path = self.config.get('url').get('path')
        return self.append_to_base(path)


class PonsOliver(Base):
    SITE = 'pons_oliver'


class Fotocasa(Base):
    SITE = 'fotocasa'

    def combine_with_filters(self, url, zone_filters):
        query_string = self.filter_builder.build(**zone_filters)

        if query_string:
            url = f'{url}?{query_string}'

        return url


class Idealista(Base):
    SITE = 'idealista'

    def generate_zone_url(self, zone):
        # Idealista site will return 404 if url does not end with trailing slash
        zone_url = super().generate_zone_url(zone)
        if not zone_url.endswith('/'):
            zone_url = f'{zone_url}/'

        return zone_url

    def combine_with_filters(self, url, zone_filters):
        filter_path = self.filter_builder.build(**zone_filters)

        if filter_path:
            url = f'{url}/{filter_path}'

        return url


class Factory:
    SITES = {
        PonsOliver.SITE: PonsOliver,
        Fotocasa.SITE: Fotocasa,
        Idealista.SITE: Idealista,
    }

    @classmethod
    def build(cls, site):
        builder_class = cls.SITES.get(site)
        if not builder_class:
            return None

        return builder_class()
