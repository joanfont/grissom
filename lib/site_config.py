import yaml


class SiteConfig(dict):

    @classmethod
    def from_yml(cls, path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        return cls(**config)
