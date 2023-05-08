import OFS.SimpleItem as SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

import requests as req
import json
import base64

from copy import copy

from .AuthAD import AuthAD
from .Callbacks import Callbacks


class Gestor(SimpleItem.SimpleItem):
    """Classe para Testar a Integracao."""

    callbacks = Callbacks()

    NEW_PARTE = {
        "id_validacao_bloco": 2,
        "identificacao_parte": "Tester",
        "nome": None,
        "pessoa_preenche_dados": 1,
        "email": None,
        "ddd": None,
        "telefone": None,
        "id_tipo_telefone": 2,
    }

    NEW_PARTE_AUTENTICADO = {
        "id_validacao_bloco": 1,
        "identificacao_parte": "Tester",
        "nome": None,
        "pessoa_preenche_dados": 1,
        "email": None,
        "ddd": None,
        "telefone": None,
        "id_tipo_telefone": 2,
    }

    _caracteres_especiais = [
        ' ', ',', '.', '-', '(', ')', '_', '*', '/', '[', ']', '\\']

    TIPOS_CAMPOS = {
        1: 'Texto',
        2: 'Constante',
        3: 'Única opção (vulgo RADIO)',
        4: 'Caixa de seleção (vulgo SELECT)',
        5: 'Múltiplas opções (vulgo CHECKBOX)',
        6: 'Número',
        7: 'Data',
        8: 'E-mail',
        9: 'CPF',
        10: 'CNPJ',
        11: 'DDD + Fone',
        12: 'Texto grande',
        13: 'RG',
        14: 'Valor (Real R$)'
    }

    def __init__(self, zid='gestor'):
        """Construtor."""
        self.id = zid

    def extrair_caracteres_especiais(self, string):
        """Extra caracteres especiais da string."""
        if string:
            for c in self._caracteres_especiais:
                string = string.replace(c, '')
        return string

    def id_tipo_campo_tostring(self, id_tipo_campo):
        """Retorna tipo do campo formatado para texto."""
        return self.TIPOS_CAMPOS[id_tipo_campo]

    def _retorna_msg_js(self, msg):
        """."""
        return """
        <script>
        alert('{}')
        history.back(-1);
        </script>
        """.format(msg)

    def _formatar_query_string(self, data):
        """Transforma dicionario em query string de GET."""
        return '&'.join("%s=%s" % i for i in data.items())

    def _obter_auth(self, url, query=''):
        """."""
        return AuthAD(
            url=url, query=query,
            token=self.token,
            secret=self.secret)

    def index_html(self):
        """Tela inicial do sistema demonstracao."""

        url_modelos = (
            self.url_assinebem + "modelo/obter_modelos")
        r = req.get(
            url=url_modelos,
            auth=self._obter_auth(url=url_modelos, query='')
        )

        _modelos = []

        if r.status_code == 200:
            _modelos = r.json()['modelos']

        _lista_uploads = copy(self.lista_uploads)

        return self._index_html(
            lista_uploads=_lista_uploads,
            modelos=_modelos
        )

    def processar(self, index=None, **kwargs):
        """Processa dados do form."""

        #
        # BLOCO PARA OBTER IDENTIFICADOR
        #

        if not index:
            return self._retorna_msg_js(
                msg="Nenhum assinante definido.")

        arquivo = self.REQUEST.get('arquivo')

        if not arquivo:
            return self._retorna_msg_js(
                msg="Nenhum arquivo definido.")

        url_identifier = (
            self.url_assinebem + "documento/get_identifier_to_upload")

        r = req.get(
            url=url_identifier,
            auth=self._obter_auth(url=url_identifier, query='')
        )

        r_1 = r.json()

        if r_1["status"] != 200:
            raise Exception("Erro: " + json.dumps(r_1))

        identificador = r_1["identifier"]

        #
        # BLOCO DE UPLOAD DO DOCUMENTO
        #

        filename = arquivo.filename
        arquivo = base64.b64encode(arquivo.read()).decode()

        lista_partes = []
        for i in index:
            _identificacao = self.REQUEST.get('identificacao_%s' % i, None)
            _nome = self.REQUEST.get('nome_%s' % i)
            _email = self.REQUEST.get('email_%s' % i)
            _celular = self.REQUEST.get('celular_%s' % i)

            if _celular:
                _celular = self.extrair_caracteres_especiais(_celular)

            _obj_parte = copy(self.NEW_PARTE)
            _obj_parte.update({
                "identificacao_parte": _identificacao,
                "nome": _nome,
                "email": _email,
                "ddd": _celular[:2] if _celular else None,
                "telefone": _celular[2:] if _celular else None
            })

            lista_partes.append(_obj_parte)

        data = {
            "id_identifier": identificador,
            "lista_partes": lista_partes,
            "arquivo": arquivo,
            "sufixo_arquivo": "pdf",
            "identificacao_arquivo": filename,
            "quadro_assinaturas": 1
        }

        url_upload = self.url_assinebem + "documento"

        r_2 = req.post(
            url=url_upload, json=data,
            auth=self._obter_auth(
                url=url_upload, query=json.dumps(data))
        )

        r_2 = r_2.json()
        if r_2["status"] == 200:
            self.add_upload(r_2)
        else:
            raise Exception(r_2)

        return self.REQUEST.RESPONSE.redirect("index_html")

    def processar_modelo(self, id_modelo, index=None, **kwargs):
        """Processa dados do form de Modelo."""
        if not index:
            return self._retorna_msg_js(
                msg="Nenhum assinante definido.")

        lista_partes = []
        for i in index:
            _id_modelo_parte = self.REQUEST.get('id_modelo_parte_%s' % i, None)
            _identificacao = self.REQUEST.get('identificacao_%s' % i, None)
            _nome = self.REQUEST.get('nome_%s' % i)
            _email = self.REQUEST.get('email_%s' % i)
            _celular = self.REQUEST.get('celular_%s' % i)

            if _celular:
                _celular = self.extrair_caracteres_especiais(_celular)

            _obj_parte = copy(self.NEW_PARTE)
            _obj_parte["id_modelo_parte"] = int(_id_modelo_parte)

            _obj_parte.update({
                "identificacao_parte": _identificacao,
                "nome": _nome,
                "email": _email,
                "ddd": _celular[:2] if _celular else None,
                "telefone": _celular[2:] if _celular else None
            })

            lista_partes.append(_obj_parte)

        id_modelo = int(id_modelo)

        data = {
            "id_externo": id_modelo,
            "lista_partes": lista_partes,
            "sufixo_arquivo": "pdf",
            "identificacao_arquivo": 'modelo_%d.pdf' % id_modelo,
            "quadro_assinaturas": 1
        }

        url_upload = self.url_assinebem + "modelo"

        r_2 = req.post(
            url=url_upload, json=data,
            auth=self._obter_auth(
                url=url_upload, query=json.dumps(data))
        )

        r_2 = r_2.json()
        if r_2["status"] == 200:
            r_2["documento"]["id_modelo"] = id_modelo

            self.add_upload(r_2)
        else:
            raise Exception(r_2)

        return self.REQUEST.RESPONSE.redirect("index_html")

    def get(self, id_externo):
        """Faz um GET para obter infos do documento."""

        url_get = self.url_assinebem + "documento"

        data = {"id_externo": id_externo}

        r = req.get(
            url=url_get,
            params=data,
            auth=self._obter_auth(
                url=url_get, query=self._formatar_query_string(data))
        )

        return json.dumps({
            "url_entrada": "GET: %s" % url_get,
            "entrada": data,
            "saida": r.json()
        })

    def invalidar(self, id_externo):
        """Invalida documento na API."""
        url_invalidar = self.url_assinebem + "documento/invalidar"

        data = {
            "id_externo": id_externo
        }

        r_inval = req.post(
            url=url_invalidar, json=data,
            auth=self._obter_auth(
                url=url_invalidar, query=json.dumps(data))
        )

        r_inval = r_inval.json()

        _retorno = {
            "url_entrada": "POST: %s" % url_invalidar,
            "entrada": data,
            "saida": r_inval
        }

        if r_inval["status"] == 200:
            _retorno["invalidou"] = 1

            self.lista_uploads[id_externo]["invalido"] = True
            self.lista_uploads[id_externo]["id_documento_status"] = 3
            self.lista_uploads[id_externo]["descricao_documento_status"] =\
                "Inválido."

            return json.dumps(_retorno)

        _retorno["invalidou"] = 0
        return json.dumps(_retorno)

    def assinantes(self, id_externo):
        """Obtem assinantes do documento."""
        dados_documento = self.lista_uploads.get(id_externo)

        if dados_documento:

            _lista_partes = dados_documento["lista_partes"]

            return self._assinantes(
                id_externo_documento=id_externo,
                lista_partes=_lista_partes
            )

        return self._retorna_msg_js(
            msg="Nenhum assinante encontrado.")

    def campos_preenchidos(self, id_externo):
        """View com campos preenchidos pelos assinantes."""

        def filtrar_por_id(item):
            if ((isinstance(id, (list, tuple)) and
                 item['id'] in id) or item['id'] == id):
                return True
            return False

        dados_documento = self.lista_uploads.get(id_externo)

        if dados_documento:

            json_retorno = self.get_modelo_dados_preenchidos(
                id_externo_documento=id_externo,
                flag_tipo_retorno=2)

            a = []
            if json_retorno.get("dados"):
                for id_parte, campos in json_retorno["dados"].items():
                    r = {"parte": {"id_externo": id_parte}, "campos": []}

                    for i, j in campos.items():
                        j["nome_campo"] = i
                        r["campos"].append(j)
                    a.append(r)

            return self._campos_preenchidos(
                id_externo_documento=id_externo,
                data=a
            )

        return self._retorna_msg_js(
            msg="Nenhum documento encontrado.")

    def assinatura(self, id_externo_documento, id_externo_parte):
        """Retorna dados da Assinatura."""

        url_assinatura = self.url_assinebem + "documento/assinatura/status"

        data = {
            "id_externo_documento": id_externo_documento,
            "id_externo_parte": id_externo_parte
        }

        r_assinatura = req.get(
            url=url_assinatura,
            params=data,
            auth=self._obter_auth(
                url=url_assinatura, query=self._formatar_query_string(data))
        )

        r_assinatura = r_assinatura.json()

        if r_assinatura["status"] == 200:

            if r_assinatura.get("dt_assinatura"):
                _status = "Assinado em: %s" % r_assinatura.get("dt_assinatura")
            elif r_assinatura.get("assinatura_delegada"):
                _status = "Assinatura delegada para: %s" %\
                    r_assinatura.get("nome_delegado")
            elif r_assinatura.get("assinatura_substituida"):
                _status = "Assinatura substituida por: %s" %\
                    r_assinatura.get("nome_substituto")

            return json.dumps({
                "status": _status,
                "assinado": 1
            })
        elif r_assinatura["status"] == 204:
            return json.dumps({
                "status": "Não assinado",
                "assinado": 0
            })

        return json.dumps({
            "status": "Indisponível",
            "assinado": 0
        })

    def download(self, id_externo):
        """Faz download do arquivo."""

        url_download = self.url_assinebem + "documento/download"

        data = {
            "id_externo": id_externo,
            "assinado": 1
        }

        r = req.post(
            url=url_download, json=data,
            auth=self._obter_auth(
                url=url_download, query=json.dumps(data))
        )

        r = r.json()

        if r["status"] == 200:
            arquivo = base64.b64decode(r["arquivo"])

            self.REQUEST.RESPONSE.setHeader(
                'Content-Transfer-Encoding', 'binary')
            self.REQUEST.RESPONSE.setHeader(
                'Content-Type', r["file_type"])
            self.REQUEST.RESPONSE.setHeader(
                'Content-Length', r["file_length"])

            self.REQUEST.RESPONSE.setHeader(
                'Content-Disposition', 'attachment; filename="' +
                r["identificacao_arquivo"] + '"')

            return arquivo

        return self._retorna_msg_js(msg="Download indisponivel")

    def assinaturas_pendentes(self):
        """Busca assinaturas pendentes do Cliente."""

        url_get = self.url_assinebem + "documento/assinatura/pendentes"

        r_get = req.get(
            url=url_get,
            auth=self._obter_auth(url=url_get, query='')
        )

        return json.dumps({
            "url_entrada": "GET: %s" % url_get,
            "entrada": {},
            "saida": r_get.json()
        })

    def novo_acesso(self, id_externo_documento):
        """Envia novo acesso para todos assinantes do Documento."""

        url_novo_acesso = self.url_assinebem + "parte/novo_acesso"

        _l_entradas = []
        _l_saidas = []

        if id_externo_documento in list(self.lista_uploads.keys()):
            for parte in self.lista_uploads[
                    id_externo_documento]["lista_partes"]:

                data = {"id_externo": parte["id_externo"]}

                r = req.post(
                    url=url_novo_acesso, json=data,
                    auth=self._obter_auth(
                        url=url_novo_acesso, query=json.dumps(data))
                )

                _l_entradas.append(data)
                _l_saidas.append(r.json())

        return json.dumps({
            "url_entrada": "POST: %s" % url_novo_acesso,
            "entrada": _l_entradas,
            "saida": _l_saidas
        })

    def get_modelo_config(self, id_modelo):
        """Retorna dados de configuracao do Modelo."""

        url_get = self.url_assinebem + "modelo/obter_modelo_dados"

        data = {
            "id_externo": id_modelo
        }

        r_get = req.get(
            url=url_get,
            params=data,
            auth=self._obter_auth(
                url=url_get, query=self._formatar_query_string(data))
        )

        return json.dumps(r_get.json())

    def get_modelo_dados_preenchidos(
            self, id_externo_documento, flag_tipo_retorno=None):
        """Recupera dados preenchidos pelo assinante no Modelo."""

        url_get = self.url_assinebem + "modelo/documentos/campos/preenchidos"

        if flag_tipo_retorno is None:
            flag_tipo_retorno = 1

        data = {
            "id_externo_documento": id_externo_documento,
            "flag_tipo_retorno": flag_tipo_retorno
        }

        r_get = req.get(
            url=url_get,
            params=data,
            auth=self._obter_auth(
                url=url_get, query=self._formatar_query_string(data))
        )

        return r_get.json()

    def standard_error_message(self, **kwargs):
        """Metodo para personalizar a pagina de exception."""
        dados = {}

        error_header = None
        # error_header = self.session.obter_session_key("error_header")

        # self.session.deleta_session_key("error_header")

        dados["error_header"] = error_header if error_header else ""
        dados["error_message"] = kwargs.get("error_message", "")
        dados["error_type"] = kwargs.get("error_type", "")
        dados["error_value"] = kwargs.get("error_value", "")
        dados["server_port"] = self.REQUEST.get("SERVER_PORT", "")

        return self._standard_error_message(dados=dados)

    _standard_error_message = PageTemplateFile(
        'zpt/standard_error_message.zpt', globals())

    _index_html = PageTemplateFile('zpt/index_html.zpt', globals())

    _assinantes = PageTemplateFile('zpt/assinantes.zpt', globals())

    _campos_preenchidos = PageTemplateFile(
        'zpt/campos_preenchidos.zpt', globals())
