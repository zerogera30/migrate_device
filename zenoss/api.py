""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: zenoss.py
Fecha: 26/11/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

--------------------------------------------------------------------------------------------------- """

import re
import json
import requests
import urllib3
from requests.adapters import HTTPAdapter
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception, retry_if_result

urllib3.disable_warnings()

# -------------------------------------------------------------------------------- #
# ---  █████╗ ██████╗ ██╗    ███████╗███████╗███╗  ██╗ █████╗  ██████╗ ██████╗ --- #
# --- ██╔══██╗██╔══██╗██║    ╚════██║██╔════╝████╗ ██║██╔══██╗██╔════╝██╔════╝ --- #
# --- ███████║██████╔╝██║      ███╔═╝█████╗  ██╔██╗██║██║  ██║╚█████╗ ╚█████╗  --- #
# --- ██╔══██║██╔═══╝ ██║    ██╔══╝  ██╔══╝  ██║╚████║██║  ██║ ╚═══██╗ ╚═══██╗ --- #
# --- ██║  ██║██║     ██║    ███████╗███████╗██║ ╚███║╚█████╔╝██████╔╝██████╔╝ --- #
# --- ╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚══════╝╚═╝  ╚══╝ ╚════╝ ╚═════╝ ╚═════╝  --- #
# -------------------------------------------------------------------------------- #

class API:

    def __init__(self, options: dict):
        """
        Inicializa la clase configurando la sesión de conexión y estableciendo los parámetros de autenticación
        y conexión necesarios para interactuar con la API.

        Parámetros:
            options: Un diccionario que contiene las opciones de configuración, incluyendo:
                - authority: La URL base de la API.
                - user: El nombre de usuario para la autenticación.
                - password: La contraseña para la autenticación.
                - scheme: El esquema de conexión (http o https).

        Configura:
            - Una sesión de `requests` con adaptadores para manejar conexiones HTTP/HTTPS.
            - Parámetros de autenticación y conexión.
        """
        # Configurar una sesión de requests para manejar conexiones HTTP/HTTPS
        self.session = requests.Session()

        # Configurar un adaptador para la sesión con parámetros de conexión optimizados
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=5)
        self.session.mount("http://", adapter)  # Montar el adaptador para conexiones HTTP
        self.session.mount("https://", adapter)  # Montar el adaptador para conexiones HTTPS

        # Establecer los parámetros de conexión y autenticación
        self.authority = options['authority']  # URL base de la API
        self.user = options['user']  # Nombre de usuario para la autenticación
        self.password = options['password']  # Contraseña para la autenticación
        self.scheme = options['scheme']  # Esquema de conexión (http o https)

        
    #  ██████╗ ███████╗████████╗
    # ██╔════╝ ██╔════╝╚══██╔══╝
    # ██║  ██╗ █████╗     ██║   
    # ██║  ╚██╗██╔══╝     ██║   
    # ╚██████╔╝███████╗   ██║   
    #  ╚═════╝ ╚══════╝   ╚═╝   

    def logout(self):
        """
        Realiza el proceso de cierre de sesión (logout) en el servidor.

        Esta función envía una solicitud GET al servidor para cerrar la sesión del usuario
        y limpia las cookies de la sesión actual.
        """
        # Ruta relativa para el endpoint de cierre de sesión
        path = "zport/dmd/logoutUser"

        # Construye la URL completa utilizando el esquema (http/https), la autoridad (dominio) y la ruta
        baseURL = f"{self.scheme}://{self.authority}/{path}"

        # Establece el encabezado de la solicitud para indicar que el contenido es JSON
        self.session.headers["Content-Type"] = "application/json; charset=utf-8"

        # Realiza una solicitud GET al servidor para cerrar la sesión
        response = self.session.get(baseURL, verify=False)

        # Limpia las cookies de la sesión actual
        self.session.cookies.clear()

        # Opcional: Limpiar las cookies de la respuesta (si es necesario)
        # response.cookies.clear()

        # Opcional: Imprimir las cookies de la sesión para depuración
        # print(self.session.cookies)


    def viewZenPacks(self):
        """
        Obtiene el listado de ZenPacks instalados en el servidor.

        Esta función realiza una solicitud GET al endpoint correspondiente para obtener
        la lista de ZenPacks instalados.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint que lista los ZenPacks instalados
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/ZenPackManager/viewZenPacks'

        # Realiza una solicitud GET al servidor utilizando el método `getResponseGet`
        return self.getResponseGet(api_endpoint)


    def viewSettings(self):
        """
        Obtiene los datos de configuración actuales del servidor.

        Esta función realiza una solicitud GET al endpoint `editSettings` para obtener
        la configuración actual del servidor.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint que devuelve la configuración actual
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/editSettings'

        # Realiza una solicitud GET al servidor utilizando el método `getResponseGet`
        return self.getResponseGet(api_endpoint)


    def saveSettings(self, params: dict):
        """
        Guarda los datos de configuración en el servidor.

        Esta función realiza una solicitud POST al endpoint `editSettings` para guardar
        la configuración proporcionada en el servidor.

        Args:
            params (dict): Un diccionario con los parámetros de configuración que se desean guardar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint que guarda la configuración
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd'

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, params)


    def dataRootManage(self):
        """
        Obtiene información relacionada con la gestión de la raíz de datos (dataRoot).

        Esta función realiza una solicitud GET al endpoint `dataRootManage` para obtener
        información sobre la raíz de datos del servidor.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint que gestiona la raíz de datos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/dataRootManage'

        # Realiza una solicitud GET al servidor utilizando el método `getResponseGet`
        return self.getResponseGet(api_endpoint)


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def getResponseGet(self, baseURL: str) -> str:
        """
        Ejecuta una solicitud GET y retorna el resultado si la solicitud es exitosa.

        Esta función llama a `responseGet` para realizar la solicitud GET y verifica si la respuesta
        tiene un código de estado HTTP 200 (éxito). Si es exitosa, retorna el contenido de la respuesta;
        de lo contrario, imprime un mensaje de error y retorna `None`.

        Args:
            baseURL (str): La URL completa a la que se realizará la solicitud GET.

        Returns:
            str or None: El contenido de la respuesta si la solicitud es exitosa, o `None` si falla.
        """
        # Ejecutar la solicitud GET
        response = self.responseGet(baseURL)
        
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            results = response.text  # Obtener el contenido de la respuesta
            return results
        else:
            # Imprimir un mensaje de error si la solicitud falla
            print(f"No se puede completar el estado HTTP: {response.status_code}")
            return ""


    def responseGet(self, baseURL: str) -> requests.Response:
        """
        Realiza una solicitud GET a la URL proporcionada.

        Esta función configura los encabezados de la solicitud y realiza una solicitud GET
        utilizando la sesión actual. También verifica si la respuesta contiene un formulario
        de autenticación, lo que indica que las credenciales son incorrectas.

        Args:
            baseURL (str): La URL completa a la que se realizará la solicitud GET.

        Returns:
            requests.Response: El objeto de respuesta de la solicitud GET.
        """
        # Configurar el encabezado de la solicitud
        self.session.headers["Content-Type"] = "application/json; charset=utf-8"
        
        # Realizar la solicitud GET
        response = self.session.get(baseURL, verify=False)
        
        # Verificar si la respuesta contiene un formulario de autenticación
        if re.search('name="__ac_name"', response.content.decode("utf-8")):
            print("Solicitud fallida. Nombre de usuario / contraseña incorrectos.")
        
        return response


    # ██████╗  █████╗  ██████╗████████╗
    # ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
    # ██████╔╝██║  ██║╚█████╗    ██║   
    # ██╔═══╝ ██║  ██║ ╚═══██╗   ██║   
    # ██║     ╚█████╔╝██████╔╝   ██║   
    # ╚═╝      ╚════╝ ╚═════╝    ╚═╝   


    def login(self):
        """
        Realiza el proceso de autenticación (login) en un servidor utilizando credenciales de usuario.

        Returns:
            dict: Un diccionario con las cookies de sesión si el login es exitoso.
            None: Si ocurre un error durante el proceso de autenticación.
        """
        # Ruta relativa para el endpoint de autenticación
        path = "zport/acl_users/cookieAuthHelper/login"

        # Construye la URL completa utilizando el esquema (http/https), la autoridad (dominio) y la ruta
        baseURL = f"{self.scheme}://{self.authority}/{path}"

        # Configura la autenticación básica (usuario y contraseña) en la sesión
        self.session.auth = (self.user, self.password)

        # Establece el encabezado de la solicitud para indicar que el contenido es JSON
        self.session.headers["Content-Type"] = "application/json; charset=utf-8"

        try:
            # Realiza una solicitud POST al servidor para autenticarse y obtener las cookies de sesión
            response = self.session.post(baseURL, verify=False)

            # Retorna las cookies de sesión en formato de diccionario
            return response.cookies.get_dict()
        except Exception as error:
            # Si ocurre un error, imprime un mensaje y retorna None
            print(f"Error in login: {error}")
            return None
    

    def getDevices(self, collector: str) -> dict:
        """
        Obtiene la lista de dispositivos (devices) asociados a un colector específico.

        Esta función realiza una solicitud POST al endpoint `device_router` para obtener
        información detallada de los dispositivos gestionados por un colector.

        Args:
            collector (str): El nombre del colector del cual se desean obtener los dispositivos.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            'action': 'DeviceRouter',  # Acción del enrutador
            'method': 'getDevices',    # Método específico para obtener dispositivos
            'data': [
                {
                    "params": {
                        "productionState": [1000, 500, 300, -1],  # Estados de producción de los dispositivos
                        "collector": collector  # Nombre del colector
                    },
                    "uid": "/zport/dmd/Devices",  # Identificador único del recurso
                    "keys": [  # Campos que se desean obtener para cada dispositivo
                        "name",
                        "snmpSysName",
                        "ipAddress",
                        "uid",
                        "status",
                        "productionState",
                        "serialNumber",
                        "tagNumber",
                        "hwManufacturer",
                        "hwModel",
                        "osManufacturer",
                        "osModel",
                        "collector",
                        "priority",
                        "systems",
                        "groups",
                        "location",
                        "ipAddressString",
                        "pythonClass"
                    ],
                    "start": 0,  # Índice inicial para la paginación
                    "limit": 10000,  # Número máximo de dispositivos a devolver
                    "sort": "name",  # Campo por el cual ordenar los resultados
                    "dir": "DESC"  # Dirección del orden (descendente)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addDeviceClassNode(self, data: dict) -> dict:
        """
        Agrega un nuevo nodo de clase de dispositivo (Device Class Node) en la jerarquía de dispositivos.

        Esta función realiza una solicitud POST al endpoint `device_router` para agregar un nuevo
        nodo de clase de dispositivo con la información proporcionada.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para crear el nodo.
                        Debe incluir:
                        - id (str): El identificador del nuevo nodo.
                        - description (str): La descripción del nodo (opcional).
                        - connectionInfo (str): Información de conexión del nodo (opcional).
                        - uid (str): El UID del contexto en el que se agregará el nodo.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción del enrutador
            "method": "addDeviceClassNode",  # Método específico para agregar un nodo de clase de dispositivo
            "data": [
                {
                    "id": data.get('id'),  # Identificador del nuevo nodo
                    "description": data.get('description', ''),  # Descripción del nodo (opcional)
                    "connectionInfo": data.get('connectionInfo', ''),  # Información de conexión (opcional)
                    "type": "organizer",  # Tipo de nodo (organizador)
                    "contextUid": data.get('uid')  # UID del contexto en el que se agregará el nodo
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
        

    def getInfo(self, device_class: str) -> dict:
        """
        Obtiene información detallada de una clase de dispositivo específica.

        Esta función realiza una solicitud POST al endpoint `device_router` para obtener
        información detallada de una clase de dispositivo, como su ID, descripción,
        dirección e información de conexión.

        Args:
            device_class (str): El UID (Identificador Único) de la clase de dispositivo
                                de la cual se desea obtener la información.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = '%s://%s/zport/dmd/device_router' % (self.scheme, self.authority)

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción del enrutador
            "method": "getInfo",       # Método específico para obtener información de la clase de dispositivo
            "data": [
                {
                    "uid": device_class,  # UID de la clase de dispositivo
                    "keys": [             # Campos que se desean obtener
                        "id",            # Identificador de la clase de dispositivo
                        "description",   # Descripción de la clase de dispositivo
                        "address",       # Dirección asociada a la clase de dispositivo
                        "connectionInfo" # Información de conexión de la clase de dispositivo
                    ]
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def getPropertiesRouter(self, device: dict) -> dict:
        """
        Obtiene las propiedades de un dispositivo específico utilizando el enrutador de propiedades.

        Esta función realiza una solicitud POST al endpoint `properties_router` para obtener
        las propiedades asociadas a un dispositivo, como configuraciones, etiquetas, etc.

        Args:
            device (dict): Un diccionario que contiene información del dispositivo, incluyendo
                        su UID (Identificador Único).

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}{device.get("uid")}/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "query",             # Método específico para consultar propiedades
            "data": [
                {
                    "constraints": {
                        "idPrefix": "c"  # Filtra propiedades cuyo ID comience con "c"
                    },
                    "uid": device.get('uid'),  # UID del dispositivo
                    "start": 0,                # Índice inicial para la paginación
                    "limit": 1000,             # Número máximo de propiedades a devolver
                    "sort": "label",            # Campo por el cual ordenar los resultados
                    "dir": "DESC"               # Dirección del orden (descendente)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def getPropertiesRouterGeneral(self):
        """
        Obtiene las propiedades generales de los dispositivos utilizando el enrutador de propiedades.

        Esta función realiza una solicitud POST al endpoint `properties_router` para obtener
        propiedades generales asociadas a los dispositivos, como configuraciones, etiquetas, etc.,
        bajo el contexto de "/zport/dmd/Devices".

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "query",             # Método específico para consultar propiedades
            "data": [
                {
                    "constraints": {
                        "idPrefix": "c"  # Filtra propiedades cuyo ID comience con "c"
                    },
                    "uid": "/zport/dmd/Devices",  # UID del contexto general de dispositivos
                    "start": 0,                   # Índice inicial para la paginación
                    "limit": 1000,               # Número máximo de propiedades a devolver
                    "sort": "label",              # Campo por el cual ordenar los resultados
                    "dir": "DESC"                 # Dirección del orden (descendente)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)        


    def getZenProperties(self, device: dict) -> dict:
        """
        Obtiene las propiedades Zen (ZenProperties) de un dispositivo específico.

        Esta función realiza una solicitud POST al endpoint `properties_router` para obtener
        las propiedades Zen asociadas a un dispositivo, como configuraciones, etiquetas, etc.

        Args:
            device (dict): Un diccionario que contiene información del dispositivo, incluyendo
                        su UID (Identificador Único).

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}{device.get("uid")}/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "getZenProperties", # Método específico para obtener propiedades Zen
            "data": [
                {
                    "params": {},         # Parámetros adicionales (vacío en este caso)
                    "uid": device.get('uid'),  # UID del dispositivo
                    "start": 0,           # Índice inicial para la paginación
                    "limit": 1000,        # Número máximo de propiedades a devolver
                    "sort": "id",         # Campo por el cual ordenar los resultados
                    "dir": "DESC"         # Dirección del orden (descendente)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getZenPropertiesGeneral(self):
        """
        Obtiene las propiedades Zen (ZenProperties) generales de todos los dispositivos.

        Esta función realiza una solicitud POST al endpoint `properties_router` para obtener
        las propiedades Zen asociadas a todos los dispositivos bajo el contexto general
        "/zport/dmd/Devices".

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "getZenProperties", # Método específico para obtener propiedades Zen
            "data": [
                {
                    "params": {},         # Parámetros adicionales (vacío en este caso)
                    "uid": "/zport/dmd/Devices",  # UID del contexto general de dispositivos
                    "start": 0,            # Índice inicial para la paginación
                    "limit": 10000,        # Número máximo de propiedades a devolver
                    "sort": "id",          # Campo por el cual ordenar los resultados
                    "dir": "ASC"           # Dirección del orden (ascendente)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getZenProperty(self, uid: str) -> dict:
        """
        Obtiene una propiedad Zen (ZenProperty) específica de un dispositivo o recurso.

        Esta función realiza una solicitud POST al endpoint `properties_router` para obtener
        una propiedad Zen específica (en este caso, "zCollectorPlugins") asociada a un
        dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso del cual se
                    desea obtener la propiedad Zen.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "getZenProperty",   # Método específico para obtener una propiedad Zen
            "data": [
                {
                    "uid": uid,           # UID del dispositivo o recurso
                    "zProperty": "zCollectorPlugins"  # Nombre de la propiedad Zen a obtener
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    
        
    def setZenPropertyModel(self, data: dict) -> dict:
        """
        Establece o actualiza una propiedad Zen (ZenProperty) para un dispositivo o recurso.

        Esta función realiza una solicitud POST al endpoint `properties_router` para establecer
        o actualizar una propiedad Zen específica utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para establecer
                        la propiedad Zen. Debe incluir:
                        - uid (str): El UID del dispositivo o recurso.
                        - zProperty (str): El nombre de la propiedad Zen a establecer.
                        - value: El valor que se desea asignar a la propiedad Zen.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "setZenProperty",  # Método específico para establecer una propiedad Zen
            "data": [data],              # Datos proporcionados para establecer la propiedad Zen
            'type': 'rpc',               # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def setZenProperty(self, uid: str, value: dict) -> dict:
        """
        Establece o actualiza una propiedad Zen (ZenProperty) para un dispositivo o recurso.

        Esta función realiza una solicitud POST al endpoint `properties_router` para establecer
        o actualizar una propiedad Zen específica utilizando el UID del recurso y el valor proporcionado.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se le asignará la propiedad.
            value (dict): Un diccionario que contiene:
                        - id (str): El nombre de la propiedad Zen a establecer.
                        - value: El valor que se desea asignar a la propiedad Zen.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "setZenProperty",   # Método específico para establecer una propiedad Zen
            "data": [
                {
                    "uid": uid,           # UID del dispositivo o recurso
                    "zProperty": value.get('id'),  # Nombre de la propiedad Zen a establecer
                    "value": value.get('value')    # Valor que se desea asignar a la propiedad Zen
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def setZenPropertyGeneral(self, zProperty: str, value: str) -> dict:
        """
        Establece o actualiza una propiedad Zen (ZenProperty) general para todos los dispositivos.

        Esta función realiza una solicitud POST al endpoint `properties_router` para establecer
        o actualizar una propiedad Zen específica en el contexto general de dispositivos ("/zport/dmd/Devices").

        Args:
            zProperty (str): El nombre de la propiedad Zen a establecer.
            value (str): El valor que se desea asignar a la propiedad Zen.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "setZenProperty",   # Método específico para establecer una propiedad Zen
            "data": [
                {
                    "uid": "/zport/dmd/Devices",  # UID del contexto general de dispositivos
                    "zProperty": zProperty,       # Nombre de la propiedad Zen a establecer
                    "value": value                # Valor que se desea asignar a la propiedad Zen
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def updatePropertiesRouterGeneral(self, id: str, value: str) -> dict:
        """
        Actualiza una propiedad personalizada (custom property) en el contexto general de dispositivos.

        Esta función realiza una solicitud POST al endpoint `properties_router` para actualizar
        una propiedad personalizada en el contexto general de dispositivos ("/zport/dmd/Devices").

        Args:
            id (str): El identificador de la propiedad personalizada que se desea actualizar.
            value (str): El nuevo valor que se desea asignar a la propiedad personalizada.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "update",           # Método específico para actualizar una propiedad
            "data": [
                {
                    "id": id,             # Identificador de la propiedad personalizada
                    "value": value,      # Nuevo valor que se desea asignar a la propiedad
                    "uid": "/zport/dmd/Devices"  # UID del contexto general de dispositivos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addPropertiesRouterGeneral(self, data: dict) -> dict:
        """
        Agrega una nueva propiedad personalizada (custom property) en el contexto general de dispositivos.

        Esta función realiza una solicitud POST al endpoint `properties_router` para agregar
        una nueva propiedad personalizada en el contexto general de dispositivos ("/zport/dmd/Devices").

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para agregar la propiedad.
                        Debe incluir:
                        - id (str): El identificador de la propiedad personalizada.
                        - value (str): El valor de la propiedad personalizada.
                        - uid (str): El UID del contexto general de dispositivos ("/zport/dmd/Devices").

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "add",              # Método específico para agregar una propiedad
            "data": [data],               # Datos proporcionados para agregar la propiedad
            'type': 'rpc',                # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                   # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addNode(self, data: dict) -> dict:
        """
        Agrega un nuevo nodo (grupo o sistema) en la jerarquía de dispositivos.

        Esta función realiza una solicitud POST al endpoint `device_router` para agregar
        un nuevo nodo (grupo o sistema) utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para agregar el nodo.
                        Debe incluir:
                        - id (str): El identificador del nuevo nodo.
                        - description (str): La descripción del nodo (opcional).
                        - type (str): El tipo de nodo (por ejemplo, "organizer").
                        - contextUid (str): El UID del contexto en el que se agregará el nodo.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción del enrutador de dispositivos
            "method": "addNode",       # Método específico para agregar un nodo
            "data": [data],            # Datos proporcionados para agregar el nodo
            'type': 'rpc',             # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def addLocationNode(self, data: dict) -> dict:
        """
        Agrega un nuevo nodo de localidad en la jerarquía de dispositivos.

        Esta función realiza una solicitud POST al endpoint `device_router` para agregar
        un nuevo nodo de localidad utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para agregar la localidad.
                        Debe incluir:
                        - id (str): El identificador de la nueva localidad.
                        - description (str): La descripción de la localidad (opcional).
                        - type (str): El tipo de nodo (por ejemplo, "organizer").
                        - contextUid (str): El UID del contexto en el que se agregará la localidad.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",      # Acción del enrutador de dispositivos
            "method": "addLocationNode",  # Método específico para agregar un nodo de localidad
            "data": [data],               # Datos proporcionados para agregar la localidad
            'type': 'rpc',                # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                   # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addDevice(self, data: dict) -> dict:
        """
        Agrega un nuevo dispositivo (Device) en la jerarquía de dispositivos.

        Esta función realiza una solicitud POST al endpoint `device_router` para agregar
        un nuevo dispositivo utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para agregar el dispositivo.
                        Debe incluir:
                        - deviceName (str): El nombre del dispositivo.
                        - deviceClass (str): La clase del dispositivo.
                        - collector (str): El colector asignado al dispositivo.
                        - productionState (int): El estado de producción del dispositivo.
                        - comments (str): Comentarios adicionales sobre el dispositivo (opcional).
                        - hwManufacturer (str): El fabricante del hardware (opcional).
                        - hwProductName (str): El nombre del producto de hardware (opcional).
                        - osManufacturer (str): El fabricante del sistema operativo (opcional).
                        - osProductName (str): El nombre del producto del sistema operativo (opcional).

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción del enrutador de dispositivos
            "method": "addDevice",     # Método específico para agregar un dispositivo
            "data": [data],            # Datos proporcionados para agregar el dispositivo
            'type': 'rpc',             # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
        

    def updatePropertiesRouter(self, uid: str, value: dict) -> dict:
        """
        Actualiza una propiedad personalizada (custom property) para un dispositivo o recurso específico.

        Esta función realiza una solicitud POST al endpoint `properties_router` para actualizar
        una propiedad personalizada asociada a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso.
            value (dict): Un diccionario que contiene:
                        - id (str): El identificador de la propiedad personalizada.
                        - value: El nuevo valor que se desea asignar a la propiedad.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "update",           # Método específico para actualizar una propiedad
            "data": [
                {
                    "id": value.get('id'),  # Identificador de la propiedad personalizada
                    "value": value.get('value'),  # Nuevo valor que se desea asignar a la propiedad
                    "uid": uid  # UID del dispositivo o recurso
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addPropertiesRouter(self, uid: str, value: dict) -> dict:
        """
        Agrega una nueva propiedad personalizada (custom property) para un dispositivo o recurso específico.

        Esta función realiza una solicitud POST al endpoint `properties_router` para agregar
        una nueva propiedad personalizada asociada a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso.
            value (dict): Un diccionario que contiene:
                        - id (str): El identificador de la propiedad personalizada.
                        - label (str): La etiqueta de la propiedad (opcional).
                        - description (str): La descripción de la propiedad (opcional).
                        - type (str): El tipo de la propiedad.
                        - value: El valor que se desea asignar a la propiedad.
                        - uid (str): El UID del contexto general de dispositivos ("/zport/dmd/Devices").

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de propiedades
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/properties_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "PropertiesRouter",  # Acción del enrutador de propiedades
            "method": "add",              # Método específico para agregar una propiedad
            "data": [
                {
                    "id": value.get('id'),          # Identificador de la propiedad personalizada
                    "label": value.get('label', ''),  # Etiqueta de la propiedad (opcional)
                    "description": value.get('description', ''),  # Descripción de la propiedad (opcional)
                    "type": value.get('type'),      # Tipo de la propiedad
                    "value": value.get('value'),    # Valor que se desea asignar a la propiedad
                    "uid": "/zport/dmd/Devices"     # UID del contexto general de dispositivos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
        

    def getAddTemplateTargets(self) -> dict:
        """
        Obtiene los objetivos (targets) disponibles para agregar una plantilla (template).

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        los objetivos (targets) disponibles a los que se puede asignar una nueva plantilla.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",          # Acción del enrutador de plantillas
            "method": "getAddTemplateTargets",  # Método específico para obtener los objetivos de plantilla
            "data": [{}],                       # Datos vacíos (no se requieren parámetros adicionales)
            'type': 'rpc',                      # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                         # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getTemplatesGeneral(self) -> dict:
        """
        Obtiene las plantillas (templates) disponibles en el contexto general de dispositivos.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        las plantillas asociadas al contexto general de dispositivos ("/zport/dmd/Devices").

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getTemplates",    # Método específico para obtener las plantillas
            "data": [
                "/zport/dmd/Devices"     # UID del contexto general de dispositivos
            ],
            'type': 'rpc',              # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                 # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getTemplates(self, uid: str) -> dict:
        """
        Obtiene las plantillas (templates) asociadas a un dispositivo o recurso específico.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        las plantillas asociadas a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso del cual
                    se desean obtener las plantillas.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getTemplates",    # Método específico para obtener las plantillas
            "data": [uid],               # UID del dispositivo o recurso
            'type': 'rpc',               # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
        

    def addTemplateGeneral(self, data: dict) -> dict:
        """
        Agrega una nueva plantilla (template) en el contexto general de dispositivos.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        una nueva plantilla utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para agregar la plantilla.
                        Debe incluir:
                        - id (str): El identificador de la plantilla.
                        - type (str): El tipo de plantilla.
                        - description (str): La descripción de la plantilla (opcional).
                        - target (str): El UID del objetivo (target) al que se asignará la plantilla.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addTemplate",     # Método específico para agregar una plantilla
            "data": [data],              # Datos proporcionados para agregar la plantilla
            'type': 'rpc',               # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def deleteTemplate(self, uid: str) -> dict:
        """
        Elimina una plantilla (template) específica identificada por su UID.

        Esta función realiza una solicitud POST al endpoint `template_router` para eliminar
        una plantilla asociada a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la plantilla que se desea eliminar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "deleteTemplate",  # Método específico para eliminar una plantilla
            "data": [
                {
                    "uid": uid  # UID de la plantilla que se desea eliminar
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def addTemplateLocal(self, uid: str, data: dict) -> dict:
        """
        Agrega una plantilla local (local template) a un dispositivo o recurso específico.

        Esta función realiza una solicitud POST al endpoint `device_router` para agregar
        una plantilla local a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se
                    agregará la plantilla local.
            data (dict): Un diccionario que contiene los datos necesarios para agregar
                        la plantilla local. Debe incluir:
                        - id (str): El identificador de la plantilla.
                        - type (str): El tipo de plantilla.
                        - description (str): La descripción de la plantilla (opcional).
                        - target (str): El UID del objetivo (target) al que se asignará la plantilla.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",      # Acción del enrutador de dispositivos
            "method": "addLocalTemplate",  # Método específico para agregar una plantilla local
            "data": [data],                # Datos proporcionados para agregar la plantilla local
            'type': 'rpc',                 # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                    # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def removeLocalTemplate(self, uid: str, data: dict) -> dict:
        """
        Elimina una plantilla local (local template) de un dispositivo o recurso específico.

        Esta función realiza una solicitud POST al endpoint `device_router` para eliminar
        una plantilla local asociada a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso del cual
                    se eliminará la plantilla local.
            data (dict): Un diccionario que contiene los datos necesarios para eliminar
                        la plantilla local. Debe incluir:
                        - id (str): El identificador de la plantilla local.
                        - type (str): El tipo de plantilla local.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de dispositivos
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/device_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "DeviceRouter",        # Acción del enrutador de dispositivos
            "method": "removeLocalTemplate", # Método específico para eliminar una plantilla local
            "data": [data],                  # Datos proporcionados para eliminar la plantilla local
            'type': 'rpc',                   # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                      # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def runCommand(self, uids: any, command: str) -> str:
        """
        Ejecuta un comando en uno o más dispositivos o recursos identificados por sus UIDs.

        Esta función realiza una solicitud POST al endpoint `run_command` para ejecutar
        un comando en los dispositivos o recursos especificados.

        Args:
            uids (str or list): El UID o una lista de UIDs de los dispositivos o recursos
                                en los que se ejecutará el comando.
            command (str): El comando que se desea ejecutar.

        Returns:
            str: La respuesta del servidor en formato de texto.
        """
        # Construye la URL completa para el endpoint de ejecución de comandos
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/run_command'

        # Prepara los datos de la solicitud
        data = {
            "uids": [uids] if isinstance(uids, str) else uids,  # Asegura que uids sea una lista
            "command": command  # Comando a ejecutar
        }

        # Codificar los parámetros y agregar al endpoint
        query_string = f'data={json.dumps(data)}'  # Convierte los datos a JSON y los codifica en la URL
        query_string = query_string.replace(" ", "")  # Elimina espacios en blanco

        # Formar la URL final
        api_url = f"{api_endpoint}?{query_string}"

        # Configurar los encabezados de la solicitud
        headers = {
            'Content-Type': ''  # No se requiere un tipo de contenido específico
        }

        # Realiza una solicitud POST al servidor
        response = self.session.post(api_url, headers=headers, verify=False)

        # Retorna la respuesta del servidor en formato de texto
        return response.text
    

    def getDataSources(self, uid: str) -> dict:
        """
        Obtiene las fuentes de datos (DataSources) asociadas a un dispositivo o recurso específico.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        las fuentes de datos asociadas a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso del cual
                    se desean obtener las fuentes de datos.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getDataSources",  # Método específico para obtener las fuentes de datos
            "data": [
                {
                    "uid": uid  # UID del dispositivo o recurso
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getDataSourceDetails(self, uid: str) -> dict:
        """
        Obtiene los detalles de una fuente de datos (DataSource) específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        los detalles de una fuente de datos asociada a un dispositivo o recurso identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la fuente de datos de la cual
                    se desean obtener los detalles.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",      # Acción del enrutador de plantillas
            "method": "getDataSourceDetails",  # Método específico para obtener los detalles de la fuente de datos
            "data": [
                {
                    "uid": uid  # UID de la fuente de datos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addDataSource(self, uid: str, data_source: dict) -> dict:
        """
        Agrega una nueva fuente de datos (DataSource) a una plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        una nueva fuente de datos a una plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la plantilla a la que se agregará
                    la fuente de datos.
            data_source (dict): Un diccionario que contiene los datos necesarios para agregar
                                la fuente de datos. Debe incluir:
                                - newId (str): El nombre de la nueva fuente de datos.
                                - type (str): El tipo de la fuente de datos.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addDataSource",   # Método específico para agregar una fuente de datos
            "data": [
                {
                    "name": data_source.get('newId'),  # Nombre de la nueva fuente de datos
                    "type": data_source.get('type'),   # Tipo de la fuente de datos
                    "templateUid": uid                # UID de la plantilla a la que se agregará la fuente de datos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def deleteDataSource(self, uid: str) -> dict:
        """
        Elimina una fuente de datos (DataSource) específica identificada por su UID.

        Esta función realiza una solicitud POST al endpoint `template_router` para eliminar
        una fuente de datos asociada a una plantilla o dispositivo identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la fuente de datos que se desea eliminar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "deleteDataSource",  # Método específico para eliminar una fuente de datos
            "data": [
                {
                    "uid": uid  # UID de la fuente de datos que se desea eliminar
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def addDataPoint(self, name: str, uid: str) -> dict:
        """
        Agrega un nuevo punto de datos (DataPoint) a una fuente de datos específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        un nuevo punto de datos a una fuente de datos identificada por su UID.

        Args:
            name (str): El nombre del nuevo punto de datos.
            uid (str): El UID (Identificador Único) de la fuente de datos a la que se
                    agregará el punto de datos.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addDataPoint",    # Método específico para agregar un punto de datos
            "data": [
                {
                    "name": name,          # Nombre del nuevo punto de datos
                    "dataSourceUid": uid   # UID de la fuente de datos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addDataPointLocal(self, uid: str, name: str, dataSourceUid: str) -> dict:
        """
        Agrega un nuevo punto de datos (DataPoint) local a una fuente de datos específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        un nuevo punto de datos local a una fuente de datos identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se
                    agregará el punto de datos local.
            name (str): El nombre del nuevo punto de datos.
            dataSourceUid (str): El UID de la fuente de datos a la que se agregará el punto de datos.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addDataPoint",    # Método específico para agregar un punto de datos
            "data": [
                {
                    "name": name,          # Nombre del nuevo punto de datos
                    "dataSourceUid": dataSourceUid  # UID de la fuente de datos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def getThresholds(self, uid: str) -> dict:
        """
        Obtiene los umbrales (thresholds) asociados a una fuente de datos o plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        los umbrales asociados a una fuente de datos o plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la fuente de datos o plantilla de la cual
                    se desean obtener los umbrales.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getThresholds",   # Método específico para obtener los umbrales
            "data": [
                {
                    "uid": uid  # UID de la fuente de datos o plantilla
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addThreshold(self, uid: str, threshold: dict) -> dict:
        """
        Agrega un nuevo umbral (threshold) a una fuente de datos o plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        un nuevo umbral a una fuente de datos o plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la fuente de datos o plantilla a la que
                    se agregará el umbral.
            threshold (dict): Un diccionario que contiene los datos necesarios para agregar
                            el umbral. Debe incluir:
                            - type (str): El tipo de umbral.
                            - name (str): El identificador del umbral.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addThreshold",    # Método específico para agregar un umbral
            "data": [
                {
                    "uid": uid,  # UID de la fuente de datos o plantilla
                    "thresholdType": threshold.get('type'),  # Tipo de umbral
                    "thresholdId": threshold.get('name'),    # Identificador del umbral
                    "dataPoints": []  # Lista de puntos de datos (vacía en este caso)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addThresholdLocal(self, uid: str, threshold: dict) -> dict:
        """
        Agrega un nuevo umbral (threshold) local a una fuente de datos o plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        un nuevo umbral local a una fuente de datos o plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se
                    agregará el umbral local.
            threshold (dict): Un diccionario que contiene los datos necesarios para agregar
                            el umbral. Debe incluir:
                            - uid (str): El UID de la fuente de datos o plantilla.
                            - type (str): El tipo de umbral.
                            - name (str): El identificador del umbral.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addThreshold",    # Método específico para agregar un umbral
            "data": [
                {
                    "uid": threshold.get('uid').split('/thresholds')[0],  # UID de la fuente de datos o plantilla (sin el sufijo '/thresholds')
                    "thresholdType": threshold.get('type'),  # Tipo de umbral
                    "thresholdId": threshold.get('name'),    # Identificador del umbral
                    "dataPoints": []  # Lista de puntos de datos (vacía en este caso)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)

    
    def setInfo(self, data: dict) -> dict:
        """
        Actualiza la información de una plantilla o fuente de datos específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para actualizar
        la información de una plantilla o fuente de datos utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para actualizar
                        la información. Debe incluir:
                        - uid (str): El UID de la plantilla o fuente de datos.
                        - Otros campos específicos que se deseen actualizar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "setInfo",         # Método específico para actualizar la información
            "data": [data],              # Datos proporcionados para actualizar la información
            'type': 'rpc',               # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def setInfolocal(self, uid: str, data: dict) -> dict:
        """
        Actualiza la información de una plantilla o fuente de datos específica en un contexto local.

        Esta función realiza una solicitud POST al endpoint `template_router` para actualizar
        la información de una plantilla o fuente de datos en un contexto local, utilizando los datos proporcionados.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se
                    actualizará la información.
            data (dict): Un diccionario que contiene los datos necesarios para actualizar
                        la información. Debe incluir:
                        - uid (str): El UID de la plantilla o fuente de datos.
                        - Otros campos específicos que se deseen actualizar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "setInfo",         # Método específico para actualizar la información
            "data": [data],              # Datos proporcionados para actualizar la información
            'type': 'rpc',               # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None                  # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
        

    def removeThreshold(self, uid: str) -> dict:
        """
        Elimina un umbral (threshold) específico identificado por su UID.

        Esta función realiza una solicitud POST al endpoint `template_router` para eliminar
        un umbral asociado a una fuente de datos o plantilla identificado por su UID.

        Args:
            uid (str): El UID (Identificador Único) del umbral que se desea eliminar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "removeThreshold", # Método específico para eliminar un umbral
            "data": [
                {
                    "uid": uid  # UID del umbral que se desea eliminar
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
            

    def getGraphs(self, uid: str) -> dict:
        """
        Obtiene los gráficos (graphs) asociados a una fuente de datos o plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        los gráficos asociados a una fuente de datos o plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la fuente de datos o plantilla de la cual
                    se desean obtener los gráficos.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getGraphs",       # Método específico para obtener los gráficos
            "data": [
                {
                    "uid": uid  # UID de la fuente de datos o plantilla
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addGraphDefinition(self, uid: str, graphs: dict) -> dict:
        """
        Agrega una nueva definición de gráfico (Graph Definition) a una plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        una nueva definición de gráfico a una plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la plantilla a la que se agregará
                    la definición de gráfico.
            graphs (dict): Un diccionario que contiene los datos necesarios para agregar
                        la definición de gráfico. Debe incluir:
                        - name (str): El nombre de la definición de gráfico.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addGraphDefinition",  # Método específico para agregar una definición de gráfico
            "data": [
                {
                    "templateUid": uid,  # UID de la plantilla
                    "graphDefinitionId": graphs.get('name')  # Nombre de la definición de gráfico
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def addGraphDefinitionLocal(self, uid: str, uid_template: str, name: str) -> dict:
        """
        Agrega una nueva definición de gráfico (Graph Definition) local a una plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para agregar
        una nueva definición de gráfico local a una plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se
                    agregará la definición de gráfico local.
            uid_template (str): El UID de la plantilla a la que se agregará la definición de gráfico.
            name (str): El nombre de la definición de gráfico.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "addGraphDefinition",  # Método específico para agregar una definición de gráfico
            "data": [
                {
                    "templateUid": uid_template,  # UID de la plantilla
                    "graphDefinitionId": name     # Nombre de la definición de gráfico
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def setGraphDefinition(self, data: dict) -> dict:
        """
        Actualiza la definición de un gráfico (Graph Definition) en una plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para actualizar
        la definición de un gráfico utilizando los datos proporcionados.

        Args:
            data (dict): Un diccionario que contiene los datos necesarios para actualizar
                        la definición del gráfico. Debe incluir:
                        - uid (str): El UID de la definición del gráfico.
                        - Otros campos específicos que se deseen actualizar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "setGraphDefinition",  # Método específico para actualizar la definición del gráfico
            "data": [data],  # Datos proporcionados para actualizar la definición del gráfico
            'type': 'rpc',   # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None      # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def setGraphDefinitionLocal(self, uid: str, data: dict) -> dict:
        """
        Actualiza la definición de un gráfico (Graph Definition) local en una plantilla específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para actualizar
        la definición de un gráfico local utilizando los datos proporcionados.

        Args:
            uid (str): El UID (Identificador Único) del dispositivo o recurso al que se
                    actualizará la definición del gráfico local.
            data (dict): Un diccionario que contiene los datos necesarios para actualizar
                        la definición del gráfico. Debe incluir:
                        - uid (str): El UID de la definición del gráfico.
                        - Otros campos específicos que se deseen actualizar.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "setGraphDefinition",  # Método específico para actualizar la definición del gráfico
            "data": [data],  # Datos proporcionados para actualizar la definición del gráfico
            'type': 'rpc',   # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None      # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
        

    def getGraphPoints(self, uid: str) -> dict:
        """
        Obtiene los puntos de gráfico (Graph Points) asociados a una definición de gráfico específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        los puntos de gráfico asociados a una definición de gráfico identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la definición de gráfico de la cual
                    se desean obtener los puntos de gráfico.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getGraphPoints",  # Método específico para obtener los puntos de gráfico
            "data": [
                {
                    "uid": uid  # UID de la definición de gráfico
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getInfoGraphPoints(self, uid: str) -> dict:
        """
        Obtiene la información detallada de los puntos de gráfico (Graph Points) asociados a una definición de gráfico específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        la información detallada de los puntos de gráfico asociados a una definición de gráfico identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la definición de gráfico de la cual
                    se desea obtener la información de los puntos de gráfico.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getInfo",         # Método específico para obtener la información
            "data": [
                {
                    "uid": uid  # UID de la definición de gráfico
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)


    def getInfoTemplate(self, uid: str) -> dict:
        """
        Obtiene la información detallada de una plantilla (template) específica.

        Esta función realiza una solicitud POST al endpoint `template_router` para obtener
        la información detallada de una plantilla identificada por su UID.

        Args:
            uid (str): El UID (Identificador Único) de la plantilla de la cual se desea
                    obtener la información.

        Returns:
            dict or None: La respuesta del servidor en formato JSON si la solicitud es exitosa,
                        o None si ocurre un error.
        """
        # Construye la URL completa para el endpoint del enrutador de plantillas
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload (carga útil) para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción del enrutador de plantillas
            "method": "getInfo",         # Método específico para obtener la información
            "data": [
                {
                    "uid": uid  # UID de la plantilla
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (llamada a procedimiento remoto)
            'tid': None     # Identificador de transacción (opcional)
        }

        # Realiza una solicitud POST al servidor utilizando el método `getResponsePost`
        return self.getResponsePost(api_endpoint, payload)
    

    def getInfoTemplate(self, uid: str) -> dict:
        """
        Obtiene la información de una plantilla específica utilizando su UID.

        Parámetros:
        - uid (str): El identificador único (UID) de la plantilla de la cual se desea obtener la información.

        Retorna:
        - dict: Un diccionario que contiene la información de la plantilla solicitada.
        """
        # Construye el endpoint de la API utilizando el esquema y la autoridad definidos en la clase
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",
            "method": "getInfo",
            "data": [{
                "uid": uid  # UID de la plantilla de la cual se desea obtener la información
            }],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta
        return self.getResponsePost(api_endpoint, payload)
    

    def addThresholdToGraph(self, thresholdUid: str, graphUid: str) -> dict:
        """
        Añade un umbral (threshold) a un gráfico específico utilizando sus UIDs.

        Parámetros:
        - thresholdUid (str): El identificador único (UID) del umbral que se desea añadir al gráfico.
        - graphUid (str): El identificador único (UID) del gráfico al cual se desea añadir el umbral.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor después de realizar la operación.
        """
        # Construye el endpoint de la API utilizando el esquema y la autoridad definidos en la clase
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "addThresholdToGraph",  # Método específico que se va a ejecutar
            "data": [
                {
                    "graphUid": graphUid,  # UID del gráfico al cual se añadirá el umbral
                    "thresholdUid": thresholdUid  # UID del umbral que se desea añadir
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    

    def deleteGraphDefinition(self, uid: str) -> dict:
        """
        Elimina una definición de gráfico utilizando su UID.

        Parámetros:
        - uid (str): El identificador único (UID) de la definición del gráfico que se desea eliminar.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor después de realizar la operación.
        """
        # Construye el endpoint de la API utilizando el esquema y la autoridad definidos en la clase
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "deleteGraphDefinition",  # Método específico que se va a ejecutar
            "data": [
                {
                    "uid": uid  # UID de la definición del gráfico que se desea eliminar
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)


    def deleteGraphDefinitionLocal(self, uid: str, uid_graph: str) -> dict:
        """
        Elimina una definición de gráfico local utilizando su UID y el UID del gráfico.

        Parámetros:
        - uid (str): El identificador único (UID) que se utiliza para construir el endpoint de la API.
        - uid_graph (str): El identificador único (UID) de la definición del gráfico que se desea eliminar.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor después de realizar la operación.
        """
        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "deleteGraphDefinition",  # Método específico que se va a ejecutar
            "data": [
                {
                    "uid": uid_graph  # UID de la definición del gráfico que se desea eliminar
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
        

    def getTemplatesDeviceLocal(self, uid: str) -> dict:
        """
        Obtiene las plantillas asociadas a un dispositivo específico utilizando su UID.

        Parámetros:
        - uid (str): El identificador único (UID) del dispositivo del cual se desean obtener las plantillas.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor con las plantillas asociadas al dispositivo.
        """
        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/device_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción que se desea realizar en el servidor
            "method": "getTemplates",  # Método específico que se va a ejecutar
            "data": [uid],  # UID del dispositivo del cual se desean obtener las plantillas
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)


    def getDeviceClassTemplates(self) -> dict:
        """
        Obtiene las plantillas asociadas a una clase de dispositivos en el sistema.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor con las plantillas asociadas a la clase de dispositivos.
        """
        # Construye el endpoint de la API utilizando el esquema y la autoridad definidos en la clase
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "getDeviceClassTemplates",  # Método específico que se va a ejecutar
            "data": [
                "/zport/dmd/Devices"  # Ruta de la clase de dispositivos de la cual se desean obtener las plantillas
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)


    def getDataSourceTypes(self) -> dict:
        """
        Obtiene los tipos de fuentes de datos (DataSourceTypes) disponibles en el sistema.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor con los tipos de fuentes de datos disponibles.
        """
        # Construye el endpoint de la API utilizando el esquema y la autoridad definidos en la clase
        api_endpoint = f'{self.scheme}://{self.authority}/zport/dmd/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "getDataSourceTypes",  # Método específico que se va a ejecutar
            "data": [
                {
                    "query": ""  # Consulta vacía para obtener todos los tipos de fuentes de datos
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    

    def setBoundTemplates(self, data: dict) -> dict:
        """
        Establece las plantillas vinculadas (bound templates) a un dispositivo específico.

        Parámetros:
        - data (dict): Un diccionario que contiene la información necesaria para vincular plantillas.
                    Debe incluir al menos el UID del dispositivo y las plantillas que se desean vincular.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor después de realizar la operación.
        """
        # Extrae el UID del dispositivo del diccionario `data`
        uid = data.get('uid')

        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/device_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción que se desea realizar en el servidor
            "method": "setBoundTemplates",  # Método específico que se va a ejecutar
            "data": [data],  # Datos que incluyen el UID del dispositivo y las plantillas a vincular
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    

    def getComponentTree(self, uid: str) -> dict:
        """
        Obtiene el árbol de componentes asociados a un dispositivo específico utilizando su UID.

        Parámetros:
        - uid (str): El identificador único (UID) del dispositivo del cual se desea obtener el árbol de componentes.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor con el árbol de componentes del dispositivo.
        """
        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/device_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción que se desea realizar en el servidor
            "method": "getComponentTree",  # Método específico que se va a ejecutar
            "data": [
                {
                    "uid": uid  # UID del dispositivo del cual se desea obtener el árbol de componentes
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    

    def getComponents(self, uid: str, meta_type: str) -> dict:
        """
        Obtiene una lista de componentes asociados a un dispositivo específico, filtrados por tipo de meta (meta_type).

        Parámetros:
        - uid (str): El identificador único (UID) del dispositivo del cual se desean obtener los componentes.
        - meta_type (str): El tipo de meta (meta_type) que se utiliza para filtrar los componentes.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor con la lista de componentes.
        """
        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/device_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "DeviceRouter",  # Acción que se desea realizar en el servidor
            "method": "getComponents",  # Método específico que se va a ejecutar
            "data": [
                {
                    "uid": uid,  # UID del dispositivo del cual se desean obtener los componentes
                    "keys": [  # Lista de campos que se desean obtener para cada componente
                        "uid",
                        "name",
                        "status",
                        "severity",
                        "usesMonitorAttribute",
                        "monitor",
                        "monitored",
                        "locking",
                        "mount",
                        "storageDevice",
                        "totalBytes",
                        "availableBytes",
                        "usedBytes",
                        "capacityBytes",
                        "netapp_server_filesystem",
                        "uuid",
                        "uid",
                        "meta_type",
                        "monitor"
                    ],
                    "meta_type": meta_type,  # Tipo de meta para filtrar los componentes
                    "start": 0,  # Índice de inicio para la paginación de resultados
                    "limit": 10000,  # Número máximo de resultados a devolver
                    "sort": "name",  # Campo por el cual se ordenarán los resultados
                    "dir": "ASC"  # Dirección del ordenamiento (ASC para ascendente)
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    

    def getObjTemplates(self, uid: str, uid_component: str) -> dict:
        """
        Obtiene las plantillas asociadas a un componente específico utilizando su UID.

        Parámetros:
        - uid (str): El identificador único (UID) del dispositivo o contexto al cual pertenece el componente.
        - uid_component (str): El identificador único (UID) del componente del cual se desean obtener las plantillas.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor con las plantillas asociadas al componente.
        """
        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "getObjTemplates",  # Método específico que se va a ejecutar
            "data": [
                {
                    "uid": uid_component  # UID del componente del cual se desean obtener las plantillas
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    

    def makeLocalRRDTemplate(self, uid: str, uid_component: str, uid_template: str) -> dict:
        """
        Crea una plantilla RRD local para un componente específico utilizando su UID y el UID de la plantilla.

        Parámetros:
        - uid (str): El identificador único (UID) del dispositivo o contexto al cual pertenece el componente.
        - uid_component (str): El identificador único (UID) del componente para el cual se creará la plantilla RRD local.
        - uid_template (str): El identificador único (UID) o nombre de la plantilla que se utilizará para crear la plantilla RRD local.

        Retorna:
        - dict: Un diccionario que contiene la respuesta del servidor después de realizar la operación.
        """
        # Construye el endpoint de la API utilizando el esquema, la autoridad y el UID proporcionado
        api_endpoint = f'{self.scheme}://{self.authority}{uid}/template_router'

        # Define el payload para la solicitud POST
        payload = {
            "action": "TemplateRouter",  # Acción que se desea realizar en el servidor
            "method": "makeLocalRRDTemplate",  # Método específico que se va a ejecutar
            "data": [
                {
                    "uid": uid_component,  # UID del componente para el cual se creará la plantilla RRD local
                    "templateName": uid_template  # UID o nombre de la plantilla que se utilizará
                }
            ],
            'type': 'rpc',  # Tipo de solicitud (Remote Procedure Call)
            'tid': None  # Transaction ID (puede ser None o un valor único para identificar la transacción)
        }

        # Ejecuta la solicitud POST y retorna la respuesta del servidor
        return self.getResponsePost(api_endpoint, payload)
    
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    @retry(stop=stop_after_attempt(5), wait=wait_fixed(5))  # 5 reintentos, 5 segundos de espera
    def getResponsePost(self, baseURL: str, req_data: dict) -> dict:
        """
        Realiza una solicitud POST a la API y retorna el resultado. Si la solicitud falla, se reintenta hasta 5 veces.

        Parámetros:
        - baseURL (str): La URL base a la cual se enviará la solicitud POST.
        - req_data (dict): Los datos que se enviarán en el cuerpo de la solicitud POST.

        Retorna:
        - dict: Un diccionario que contiene el resultado de la solicitud POST.

        Excepciones:
        - Exception: Si ocurre un error en la solicitud o si el código de estado HTTP no es 200.
        """
        try:
            # Realiza la solicitud POST utilizando la función responsePost
            response = self.responsePost(baseURL, req_data)

            # Verifica si el código de estado de la respuesta es 200 (éxito)
            if response.status_code == 200:
                # Decodifica el contenido de la respuesta y retorna el campo 'result'
                return json.loads(response.content.decode("utf-8")).get('result')
            
            # Si el código de estado es 404, 413, 500, 502 o 504, se lanza una excepción para reintentar
            elif response.status_code in [404, 413, 500, 502, 504]:
                raise Exception(f"HTTP {response.status_code}: Reintentando...")
            
            # Si el código de estado no es 200 ni uno de los códigos de reintento, se imprime un mensaje de error
            print(f"HTTP {response.status_code}: {response.reason}")
            return None

        # Captura excepciones relacionadas con la solicitud (por ejemplo, problemas de conexión)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la solicitud: {e}")


    def responsePost(self, baseURL: str, req_data: dict) -> requests.Response:
        """
        Ejecuta una solicitud POST a la URL especificada con los datos proporcionados.

        Parámetros:
        - baseURL (str): La URL base a la cual se enviará la solicitud POST.
        - req_data (dict): Los datos que se enviarán en el cuerpo de la solicitud POST.

        Retorna:
        - requests.Response: La respuesta de la solicitud POST.
        """
        # Configura el encabezado de la solicitud para indicar que el contenido es JSON
        self.session.headers["Content-Type"] = "application/json; charset=utf-8"

        # Realiza la solicitud POST utilizando la sesión actual, sin verificar certificados SSL
        response = self.session.post(baseURL, data=json.dumps(req_data), verify=False)

        # # Verifica si la respuesta contiene un formulario de inicio de sesión (indicando credenciales incorrectas)
        # if re.search('name="__ac_name"', response.content.decode("utf-8")):
        #     print("Solicitud fallida. Nombre de usuario / contraseña incorrectos.")

        # Retorna la respuesta
        return response
        
