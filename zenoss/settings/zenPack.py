""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: migrate.py
Fecha: 26/11/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

--------------------------------------------------------------------------------------------------- """

from tools.parser import Html
from zenoss.api import API

# ----------------------------------------------------------------- #
# --- ███████╗███████╗███╗  ██╗██████╗  █████╗  █████╗ ██╗  ██╗ --- #
# --- ╚════██║██╔════╝████╗ ██║██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝ --- #
# ---   ███╔═╝█████╗  ██╔██╗██║██████╔╝███████║██║  ╚═╝█████═╝  --- #
# --- ██╔══╝  ██╔══╝  ██║╚████║██╔═══╝ ██╔══██║██║  ██╗██╔═██╗  --- #
# --- ███████╗███████╗██║ ╚███║██║     ██║  ██║╚█████╔╝██║ ╚██╗ --- #
# --- ╚══════╝╚══════╝╚═╝  ╚══╝╚═╝     ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ --- #
# ----------------------------------------------------------------- #

class ZenPack:
    

    def checkZenpack(self, api_login: API) -> list:
        """
        Obtiene y procesa la lista de ZenPacks instalados en Zenoss.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.

        Retorna:
        - parser_view_zenPacks (list): Una lista de ZenPacks instalados, procesados desde la respuesta HTML.
        """

        # Extraer los ZenPacks instalados en Zenoss utilizando la API
        view_zenPacks = api_login.viewZenPacks()

        # Convertir la respuesta HTML en un formato JSON utilizando la clase Html
        parser_view_zenPacks = Html().html_to_json(view_zenPacks, "LoadedZenPacks")

        # Retornar la lista de ZenPacks procesados
        return parser_view_zenPacks


    def find_missing_packs(self, export_zenpack: list, missing_zenPacks: list[dict]) -> list:
        """
        Encuentra los ZenPacks en `export_zenpack` que no están presentes en `missing_zenPacks`.

        Parámetros:
        - export_zenpack (list): Lista de ZenPacks obtenidos desde el sistema de exportación.
        - missing_zenPacks (list[dict]): Lista de diccionarios que contienen información de ZenPacks,
          donde cada diccionario tiene una clave 'Pack' que representa el nombre del ZenPack.

        Retorna:
        - missing_packs (list): Lista de ZenPacks que están en `export_zenpack` pero no en `missing_zenPacks`.
        """

        # Crear un conjunto de nombres de ZenPacks presentes en `missing_zenPacks`
        existing_packs = {item['Pack'] for item in missing_zenPacks}

        # Filtrar los ZenPacks en `export_zenpack` que no están en `existing_packs`
        missing_packs = [pack for pack in export_zenpack if pack not in existing_packs]

        # Retornar la lista de ZenPacks faltantes
        return missing_packs