from App.config import getConfiguration
config = getattr(getConfiguration(), 'product_config', {})
CONFIG_PATHS = {}
for key, value in list(config.items()):
    CONFIG_PATHS[key] = value


def initialize(context):
    """."""
    app = context.getApplication()
    if app is not None:
        install_products(app)


def install_products(self):
    """Instala os produtos do Docker."""
