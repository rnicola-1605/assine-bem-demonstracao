from Products.SQLAlchemyDA.da import SAWrapper
from Products.ZPagamentos.zpagamentos import ZPagamentos

from Products.ZSQLMethods.SQL import SQLConnectionIDs

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
    """Instala os produtos do Docker de Pagamentos."""

    # sqlalchemyda
    _config_sqlalchemyda = CONFIG_PATHS.get('sqlalchemyda', {})
    if _config_sqlalchemyda and not hasattr(self, 'SQLAlchemy'):

        sqlalchemyda = SAWrapper(
            'SQLAlchemy',
            _config_sqlalchemyda.get('title', ''))

        sqlalchemyda.dsn = _config_sqlalchemyda.get('dns', '')
        sqlalchemyda.encoding = _config_sqlalchemyda.get('encoding', '')
        sqlalchemyda.convert_unicode = 0
        # this will call manage_afterAdd
        self._setObject('SQLAlchemy', sqlalchemyda)

    # MailHost
    # _config_mailhost = CONFIG_PATHS.get('mailhost', {})
    # if _config_mailhost and not hasattr(self, 'MailHost'):
    #     mailhost = MaildropHost(
    #         _config_mailhost.get('id', ''),
    #         _config_mailhost.get('title', ''))

    #     self._setObject(
    #         _config_mailhost.get('id', ''), mailhost)

    # ZPagamentos
    _config_api_pagamentos = CONFIG_PATHS.get('api_pagamentos', {})
    if _config_api_pagamentos and not hasattr(self, 'api_pagamentos'):
        connect = SQLConnectionIDs(self)[0][1]
        conn = getattr(self, connect)
        # mailsrv = getattr(self, _config_mailhost.get('id'))

        api_pagamentos = ZPagamentos(
            _config_api_pagamentos.get('id', ''), conn, None,
            _config_api_pagamentos.get('urldb', '')
        )

        self._setObject(_config_api_pagamentos.get('id', ''), api_pagamentos)
