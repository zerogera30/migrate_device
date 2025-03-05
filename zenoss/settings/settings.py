""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: settings.py
Fecha: 29/11/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

--------------------------------------------------------------------------------------------------- """

import os
import json
import urllib.parse
from tools.parser import Html
from zenoss.api import API

# ----------------------------------------------------------------------- # 
# ---  ██████╗███████╗████████╗████████╗██╗███╗  ██╗ ██████╗  ██████╗ --- #
# --- ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗ ██║██╔════╝ ██╔════╝ --- #
# --- ╚█████╗ █████╗     ██║      ██║   ██║██╔██╗██║██║  ██╗ ╚█████╗  --- #
# ---  ╚═══██╗██╔══╝     ██║      ██║   ██║██║╚████║██║  ╚██╗ ╚═══██╗ --- #
# --- ██████╔╝███████╗   ██║      ██║   ██║██║ ╚███║╚██████╔╝██████╔╝ --- #
# --- ╚═════╝ ╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚══╝ ╚═════╝ ╚═════╝  --- #
# ----------------------------------------------------------------------- #

class Settings:


    def viewSettings(self, api_export, api_import):
        """
        Obtiene y procesa la configuración de la instancia de exportación, reemplazando campos y valores
        según la configuración definida en el archivo JSON. Además, genera parámetros de URL para su uso
        en la instancia de importación.

        Parámetros:
            api_export: Objeto API para interactuar con la instancia de exportación.
            api_import: Objeto API para interactuar con la instancia de importación.

        Retorna:
            Un diccionario con los campos reemplazados y los parámetros de URL generados.
        """
        # Obtener los datos de configuración de la instancia de exportación
        code, json_settings = self.parserSettings(api_export)
        # Reemplazar campos y valores según la configuración
        replaceFildSettings = self.replaceFildSettings(json_settings)
        # Generar parámetros de URL a partir de los campos reemplazados
        params = self.generate_url_params(replaceFildSettings)
        # Crear un diccionario de salida con los campos y parámetros generados
        output_export = {
            "filds": replaceFildSettings,
            "params": params
        }
        return output_export


    def parserSettings(self, api_login: API):
        """
        Extrae y parsea la configuración de la instancia de Zenoss.

        Parámetros:
            api_login: Objeto API para interactuar con la instancia de Zenoss.

        Retorna:
            Un código de estado y un diccionario con la configuración parseada.
        """
        # Obtener la configuración de la instancia de Zenoss
        code, view_settings = api_login.viewSettings()
        # Parsear la configuración HTML a un formato JSON
        parser_view_settings = Html().html_to_json_2(view_settings, "Stateattime")
        return code, parser_view_settings


    def replaceFildSettings(self, json_settings):
        """
        Reemplaza campos y valores en la configuración según las reglas definidas en el archivo de
        configuración JSON.

        Parámetros:
            json_settings: Diccionario con la configuración original.

        Retorna:
            Un diccionario con los campos y valores reemplazados.
        """
        # Obtener la configuración desde el archivo JSON
        config = getConfig()
        # Obtener las reglas de reemplazo para campos y valores
        field_replacements = config.get('settings', {}).get('fild', {})
        value_replacements = config.get('settings', {}).get('replace', {})
        # Crear un nuevo diccionario para almacenar la configuración actualizada
        updated_json = {}
        # Reemplazar las claves según el diccionario 'fild'
        for key, value in json_settings.items():
            new_key = field_replacements.get(key, key)  # Mantener la clave original si no hay reemplazo
            updated_json[new_key] = value
        # Reemplazar o agregar valores según el diccionario 'replace'
        for replace_key, replace_value in value_replacements.items():
            if replace_key in updated_json:
                updated_json[replace_key] = replace_value  # Reemplazar el valor si la clave existe
            else:
                updated_json[replace_key] = replace_value  # Agregar la clave y valor si no existe
        return updated_json


    def saveSettings(self, api_login: API, params):
        """
        Guarda la configuración en la instancia de Zenoss utilizando los parámetros proporcionados.

        Parámetros:
            api_login: Objeto API para interactuar con la instancia de Zenoss.
            params: Parámetros de configuración a guardar.

        Retorna:
            Un código de estado y la respuesta de la API.
        """
        # Guardar la configuración en la instancia de Zenoss
        code, save_settings = api_login.saveSettings(params)
        return code, save_settings


    def generate_url_params(self, params_dict):
        """
        Genera una cadena de parámetros de URL a partir de un diccionario.

        Parámetros:
            params_dict: Diccionario con los parámetros a codificar.

        Retorna:
            Una cadena de parámetros de URL codificada.
        """
        # Codificar los valores y construir la cadena de parámetros
        return '&'.join(f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in params_dict.items())


def getConfig():
    """
    Lee y carga la configuración desde un archivo JSON.

    Retorna:
        Un diccionario con la configuración cargada desde el archivo JSON.
    """
    # Obtener el directorio del archivo JSON
    with open(os.getcwd() + '/tools/config.json') as file:
        data = json.load(file)
    return data