from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from OFS.SimpleItem import SimpleItem
from OFS.History import Historical
from datetime import datetime
from .Gestor import Gestor


class AppPalestra(SimpleItem, Historical):
    """'Raiz."""

    meta_type = 'App - Palestra'
    zmi_icon = 'fas fa-file-upload'
    security = ClassSecurityInfo()
    __ac_permissions__ = (
        (
            'Change configuration',
            ['manage', 'edit',
             'editForm', 'manage_config']),)
    manage_options = (
        {'label': 'Editar',
         'action': 'manage'},) + Historical.manage_options
    editForm = PageTemplateFile(
        'zpt/edit.zpt', (globals()), __name__='editForm')
    editForm._owner = None
    manage = manage_config = editForm

    def __init__(self, id, url_assinebem, token=None, secret=None):
        """Construtor."""
        self.id = id
        self.url_assinebem = url_assinebem
        self.token = token
        self.secret = secret
        self.lista_uploads = {}
        self.callbacks_api = []
        self.gestor = Gestor('Gestor')

    def add_upload(self, dados):
        """Adc upload na lista."""
        self.lista_uploads[dados['documento']
                           ['id_externo']] = dados['documento']

    def get_lista_uploads(self, desc=None):
        """Retorna lista de uploads."""
        if desc:
            return list(self.lista_uploads.values())[::-1]
        else:
            return self.lista_uploads.values()

    def add_callback(self, desc_callback, payload, security_token=None):
        """Persiste payload."""
        if not getattr(self, 'callbacks_api', None):
            setattr(self, 'callbacks_api', [])
        self.callbacks_api.append({
            'security_token': security_token,
            'desc_callback': desc_callback,
            'payload': payload,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')})

    def get_callbacks(self, desc=None):
        """Retorna lista de callbacks."""
        if not getattr(self, 'callbacks_api', None):
            setattr(self, 'callbacks_api', [])
        if desc:
            return self.callbacks_api[::-1]
        else:
            return self.callbacks_api

    def define_doc_assinado(self, id_externo):
        """Define documento como assinado."""
        if id_externo in list(self.lista_uploads.keys()):
            self.lista_uploads[id_externo]['assinado'] = True
            self.lista_uploads[id_externo]['id_documento_status'] = 2
            self.lista_uploads[id_externo]['descricao_documento_status'] = \
                'Assinado'

    def manage_edit(self, RESPONSE=None, url_assinebem=None, token=None,
                    secret=None, lista_uploads=None, REQUEST=None):
        """."""
        self.url_assinebem = url_assinebem
        self.token = token
        self.secret = secret
        if lista_uploads is None:
            lista_uploads = {}
        self.lista_uploads = lista_uploads
        self._p_changed = 1
        RESPONSE.redirect('manage_config')

    def teste(self):
        """Pagina de teste usado pelo script de deploy."""
        return 'Ok'


def add_action(self, id, url_assinebem=None, token=None, secret=None,
               REQUEST=None):
    """."""
    app = AppPalestra(id=id,
                      url_assinebem=url_assinebem,
                      token=token,
                      secret=secret)
    self._setObject(id, app)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)


addForm = PageTemplateFile('zpt/add.zpt', globals())
InitializeClass(AppPalestra)
