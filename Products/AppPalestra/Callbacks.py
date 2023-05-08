import OFS.SimpleItem as SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

import json


class Callbacks(SimpleItem.SimpleItem):
    """Classe para gerenciar os Callbacks recebidos."""

    def __init__(self, zid='callbacks'):
        """Construtor."""
        self.id = zid

    def index_html(self):
        """View com um log de todas as requisicoes de Callback recebidas."""
        return self._callbacks()

    def _obter_security_token(self):
        try:
            if ('HTTP-ASSINEBEM-SECURITY-TOKEN' in
                    list(self.REQUEST.environ.keys())):
                return self.REQUEST.environ['HTTP-ASSINEBEM-SECURITY-TOKEN']

            if ('HTTP_ASSINEBEM_SECURITY_TOKEN' in
                    list(self.REQUEST.environ.keys())):
                return self.REQUEST.environ['HTTP_ASSINEBEM_SECURITY_TOKEN']
        except:
            pass

        return ''

    def obter_callbacks(self, json=None):
        """Retorna lista de callbacks formatados para renderizar.

        var json = True: retorna string formatado em json.
        """
        _lista = []
        for log in self.get_callbacks(desc=True):
            if log['payload']:
                _lista.append(
                    '[{data} - {callback}]:\n{payload}\n{sec_token}\n\n'.
                    format(
                        data=log['data'],
                        callback=log['desc_callback'],
                        payload=log['payload'],
                        sec_token=(
                            ('ASSINEBEM-SECURITY-TOKEN: %s\n' %
                             log['security_token'])
                            if log['security_token'] else ''
                        )
                    )
                )

        if _lista:
            return ''.join(_lista)

        return ''

    def status_parte(self, **kwargs):
        """Parte status foi alterado."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Status da Parte",
            _payload,
            self._obter_security_token())

    def parte_visualizou(self, **kwargs):
        """Parte visualizou."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Parte Visualizou Documento",
            _payload,
            self._obter_security_token())

    def parte_preencheu_dados(self, **kwargs):
        """Parte Preencheu Dados na plataforma."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Parte Preencheu Dados na Plataforma",
            _payload,
            self._obter_security_token())

    def parte_assinou(self, **kwargs):
        """Parte assinou."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Assinatura da Parte",
            _payload,
            self._obter_security_token())

    def parte_recusou(self, **kwargs):
        """Parte recusou."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Recusa da Parte:",
            _payload,
            self._obter_security_token())

    def documento_assinado(self, **kwargs):
        """Documento assinado por completo."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Documento Assinado",
            _payload,
            self._obter_security_token())

        self.define_doc_assinado(
            id_externo=_payload["dados"]["documento"]["id_externo"])

    def documento_invalidado(self, **kwargs):
        """Documento invalidado."""
        _payload = self.REQUEST.get('BODY', '')
        if _payload:
            _payload = json.loads(_payload)

        self.add_callback(
            "Documento Invalidado",
            _payload,
            self._obter_security_token())

    _callbacks = PageTemplateFile('zpt/callbacks.zpt', globals())
