""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: location.py
Fecha: 10/12/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

--------------------------------------------------------------------------------------------------- """

from zenoss.api import API

class Location:

    # ██╗      █████╗  █████╗  █████╗ ████████╗██╗ █████╗ ███╗  ██╗
    # ██║     ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗ ██║
    # ██║     ██║  ██║██║  ╚═╝███████║   ██║   ██║██║  ██║██╔██╗██║
    # ██║     ██║  ██║██║  ██╗██╔══██║   ██║   ██║██║  ██║██║╚████║
    # ███████╗╚█████╔╝╚█████╔╝██║  ██║   ██║   ██║╚█████╔╝██║ ╚███║
    # ╚══════╝ ╚════╝  ╚════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚════╝ ╚═╝  ╚══╝

    def getGroupLocationSystem(self, devices: list) -> dict:
        """
        Extrae y organiza los grupos, ubicaciones y sistemas asociados a una lista de dispositivos.

        Parámetros:
        - devices (list): Lista de diccionarios que representan dispositivos. Cada diccionario debe contener
          información sobre 'location', 'groups' y 'systems'.

        Retorna:
        - dict: Un diccionario con tres claves: 'groups', 'location' y 'systems', cada una con una lista
          ordenada de valores únicos.
        """

        # Inicializar un diccionario para almacenar los resultados
        result = {'groups': set(), 'location': set(), 'systems': set()}

        # Iterar sobre cada dispositivo en la lista
        for item in devices:
            # Verificar si 'location' existe y no es None antes de intentar obtener 'uid'
            location = item.get('location')
            if location and isinstance(location, dict):
                location_name = location.get('uid')
                if location_name:
                    result['location'].add(location_name)

            # Agregar los grupos si están disponibles
            result['groups'].update(
                group.get('uid') for group in item.get('groups', []) if group.get('name')
            )

            # Agregar los sistemas si están disponibles
            for system in item.get('systems', []):
                system_name = system.get('uid')
                if system_name:
                    result['systems'].add(system_name)

        # Convertir los sets a listas ordenadas antes de devolver
        origin = {key: sorted(value) for key, value in result.items()}

        # Retornar el diccionario procesado por self.parserOptions
        return self.parserOptions(origin)


    def parserOptions(self, data: dict) -> dict:
        """
        Procesa y organiza las rutas de grupos, ubicaciones y sistemas en una estructura jerárquica.

        Parámetros:
        - data (dict): Un diccionario que contiene listas de rutas para 'groups', 'location' y 'systems'.

        Retorna:
        - dict: Un diccionario con tres claves ('groups', 'location', 'systems'), cada una con una lista
          de rutas organizadas jerárquicamente.
        """

        # Inicializar el diccionario de resultados
        result = {'groups': [], 'location': [], 'systems': []}

        # Definir las categorías y sus rutas base
        categories = [
            ('groups', '/zport/dmd/Groups'),
            ('location', '/zport/dmd/Locations'),
            ('systems', '/zport/dmd/Systems')
        ]

        # Procesar cada categoría
        for category, base_path in categories:
            # Obtener la lista de elementos para la categoría actual
            items = data.get(category, [])

            # Procesar cada elemento en la lista
            for item in items:
                # Extraer las partes de la ruta, omitiendo la ruta base
                parts = item[len(base_path):].strip('/').split('/')

                # Reconstruir la ruta jerárquicamente
                current_path = base_path
                for part in parts:
                    # Construir la entrada actual
                    entry = f"{current_path}/{part}"

                    # Agregar la entrada al resultado si no está ya presente
                    if entry not in result[category]:
                        result[category].append(entry)

                    # Actualizar la ruta actual para la siguiente iteración
                    current_path = entry

        # Retornar el diccionario con las rutas organizadas
        return result


    def getLocationDetail(self, api_login: API, locations: dict) -> dict:
        """
        Obtiene y transforma los detalles de las ubicaciones (locations) utilizando la API de Zenoss.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - locations (dict): Un diccionario que contiene listas de rutas de ubicaciones organizadas por categoría.

        Retorna:
        - dict: Un diccionario que contiene los detalles de las ubicaciones, transformados y organizados por categoría.
        """

        # Inicializar el diccionario de resultados transformados
        transformed = {}

        # Iterar sobre cada categoría y sus elementos en el diccionario de ubicaciones
        for category, items in locations.items():
            transformed[category] = {}  # Inicializar el diccionario para la categoría actual

            # Procesar cada ubicación en la lista de elementos
            for item in items:
                # Obtener la información de la ubicación utilizando la API
                info = api_login.getInfo(item)

                # Modificar el valor de 'uid' si existe en los datos
                data = info.get('data')
                if data and 'uid' in data:
                    # Eliminar el último segmento del valor de 'uid'
                    data['uid'] = '/'.join(data['uid'].rstrip('/').split('/')[:-1])

                # Agregar los datos transformados al resultado final
                transformed[category][item] = data

        # Retornar el diccionario con los detalles transformados
        return transformed
    

    def addLocationDetail(self, api_login: API, locations: dict) -> dict:
        """
        Agrega detalles de ubicaciones, grupos o sistemas en Zenoss utilizando la API.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - locations (dict): Un diccionario que contiene los detalles de las ubicaciones, grupos o sistemas
          organizados por categoría.

        Retorna:
        - dict: El diccionario de ubicaciones modificado, con los resultados de las operaciones de agregado.
        """
        
        # Iterar sobre cada categoría y sus elementos en el diccionario de ubicaciones
        for main_key, items in locations.items():
            # Iterar sobre cada elemento en la categoría actual
            for key, data in items.items():
                # Reemplazar 'uid' por 'contextUid' y agregar 'type' al diccionario de datos
                if 'uid' in data:
                    data['contextUid'] = data.pop('uid')
                data['type'] = 'organizer'

                # Ejecutar la función correspondiente según la categoría
                if main_key == 'groups' or main_key == 'systems':
                    result = api_login.addNode(data)
                elif main_key == 'location':
                    result = api_login.addLocationNode(data)
                else:
                    result = None  # En caso de no ser una categoría válida

                # Agregar el resultado de la operación al diccionario de datos
                data['result'] = result['success'] if result and result.get('success') else result

        # Retornar el diccionario de ubicaciones modificado
        return locations