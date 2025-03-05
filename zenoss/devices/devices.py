""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: device.py
Fecha: 29/11/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

--------------------------------------------------------------------------------------------------- """

import re
import logging
from typing import Union
from tools.parser import Html
from zenoss.api import API

class Devices:

    # ██████╗ ███████╗██╗   ██╗██╗ █████╗ ███████╗ ██████╗
    # ██╔══██╗██╔════╝██║   ██║██║██╔══██╗██╔════╝██╔════╝
    # ██║  ██║█████╗  ╚██╗ ██╔╝██║██║  ╚═╝█████╗  ╚█████╗ 
    # ██║  ██║██╔══╝   ╚████╔╝ ██║██║  ██╗██╔══╝   ╚═══██╗
    # ██████╔╝███████╗  ╚██╔╝  ██║╚█████╔╝███████╗██████╔╝
    # ╚═════╝ ╚══════╝   ╚═╝   ╚═╝ ╚════╝ ╚══════╝╚═════╝ 

    def getDataSourceTypes(self, api_login : API) -> list:
        """
        Obtiene los tipos válidos de datasources desde la API y extrae los valores de "type".

        Parámetros:
        - api_login (API): Una instancia de la clase API que contiene el método getDataSourceTypes.

        Retorna:
        - all_types (list): Una lista con todos los valores de "type" encontrados en los datasources.
        """

        # Obtener los tipos válidos de datasources desde la API
        data_source_types = api_login.getDataSourceTypes()

        # Extraer todos los valores de "type" del campo 'data' en la respuesta de la API
        # Si el campo 'data' no existe, se usa un diccionario vacío como valor predeterminado
        all_types = [item["type"] for item in data_source_types.get('data', {})]

        # Retornar la lista de tipos de datasources
        return all_types


    def getDevices(self, api_login: API, collector: str) -> list[dict]:
        """
        Obtiene la lista de dispositivos asociados a un colector específico desde la API.

        Parámetros:
        - api_login (API): Una instancia de la clase API que contiene el método getDevices.
        - collector (str): El identificador del colector del cual se desean obtener los dispositivos.

        Retorna:
        - get_devices: La respuesta de la API que contiene la lista de dispositivos asociados al colector.
        """

        # Llama al método getDevices de la API, pasando el identificador del colector como parámetro
        get_devices = api_login.getDevices(collector)

        # Retorna la respuesta de la API con la lista de dispositivos
        return get_devices


    def addFilterDevices(self, devices_export: list[dict], devices_import: list[dict]) -> list[dict]:
        """
        Añade una clave 'unique' a cada dispositivo en devices_export que indica si el dispositivo
        no está presente en devices_import.

        Parámetros:
        - devices_export (list[dict]): Lista de dispositivos a los que se les añadirá la clave 'unique'.
        - devices_import (list[dict]): Lista de dispositivos con los que se comparará devices_export.

        Retorna:
        - devices_export (list[dict]): Lista de dispositivos con la clave 'unique' añadida.
        """

        # Crear un conjunto de tuplas (ipAddressString, collector) de devices_import para facilitar la comparación
        device_keys_import = {(device['ipAddressString'], device['collector']) for device in devices_import}

        # Iterar sobre los dispositivos en devices_export y asignar la clave 'unique'
        for device in devices_export:
            # Asignar 'True' si el dispositivo no está en devices_import, 'False' si está presente
            device['unique'] = (device['ipAddressString'], device['collector']) not in device_keys_import

        # Retornar la lista devices_export con la nueva clave 'unique' asignada
        return devices_export


    def getPythonClass(self, pythonClass: list[dict]) -> list[str]:
        """
        Extrae y devuelve una lista de clases de Python únicas a partir de una lista de diccionarios.

        Parámetros:
        - pythonClass (list[dict]): Lista de diccionarios que pueden contener la clave 'pythonClass'.

        Retorna:
        - unique_classes (list[str]): Lista de clases de Python únicas, sin el último segmento después del punto.
        """

        python_classes = []  # Lista para almacenar las clases de Python procesadas

        # Iterar sobre cada elemento en la lista pythonClass
        for item in pythonClass:
            # Verificar si el diccionario contiene la clave 'pythonClass'
            if 'pythonClass' in item:
                # Obtener el valor de 'pythonClass'
                python_class = item['pythonClass']

                # Eliminar el último segmento después del último punto
                trimmed_class = ".".join(python_class.split(".")[:-1])

                # Agregar la clase procesada a la lista python_classes
                python_classes.append(trimmed_class)

        # Eliminar duplicados convirtiendo la lista a un conjunto y luego de vuelta a lista
        unique_classes = list(set(python_classes))

        # Retornar la lista de clases únicas
        return unique_classes


    def parserDevicesClass(self, devices: list[dict]) -> list[str]:
        """
        Extrae y procesa las clases de dispositivos a partir de una lista de dispositivos.

        Parámetros:
        - devices (list[dict]): Lista de diccionarios que contienen información de dispositivos.
          Cada diccionario debe tener una clave 'uid' que representa la ruta única del dispositivo.

        Retorna:
        - sorted_uids (list[str]): Lista ordenada de clases de dispositivos únicas.
        """

        # Extraer las clases de dispositivos de la clave 'uid' utilizando una expresión regular
        class_devices = [re.search(r'/zport/dmd/(.*?)/devices', item['uid']).group(1) for item in devices]

        # Obtener valores únicos de las clases de dispositivos
        unique_uids = list(set(class_devices))

        # Ordenar alfabéticamente las clases de dispositivos únicas
        sorted_uids = sorted(unique_uids)

        # Retornar la lista ordenada de clases de dispositivos únicas
        return sorted_uids


    def detailDevicesClass(self, api_login: API, detail_devices_class: list[str]) -> list[dict]:
        """
        Obtiene y procesa información detallada para una lista de clases de dispositivos.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - detail_devices_class (list[str]): Lista de rutas de clases de dispositivos.

        Retorna:
        - result (list[dict]): Lista de diccionarios que contienen información procesada de cada clase de dispositivo.
          Cada diccionario tiene como clave la ruta limpia de la clase y como valor la información obtenida.
          Si ocurre un error, el valor será un diccionario con la clave "error" y el mensaje de error correspondiente.
        """

        result = []  # Lista para almacenar los resultados procesados

        # Iterar sobre cada clase de dispositivo en la lista
        for device in detail_devices_class:
            try:
                # Obtener información detallada del dispositivo utilizando la API
                device_info = api_login.getInfo(f'/zport/dmd/{device}')

                # Limpiar la ruta de la clase de dispositivo eliminando el último segmento y la barra final
                cleaned_device = '/'.join(device.rstrip('/').split('/')[:-1])

                # Limpiar el campo 'uid' en la información del dispositivo
                id_value = device_info['data'].get('id', '')  # Obtener el valor de 'id'
                uid_value = device_info['data'].get('uid', '')  # Obtener el valor de 'uid'
                if id_value and uid_value and id_value in uid_value:
                    # Eliminar el segmento del 'id' del campo 'uid' si está presente
                    device_info['data']['uid'] = uid_value.replace(f'/{id_value}', '')

                # Agregar el resultado procesado a la lista
                result.append({cleaned_device: device_info.get('data', {})})

            except Exception as e:
                # Si ocurre un error, agregar un diccionario con el mensaje de error
                result.append({device: {"error": str(e)}})

        # Retornar la lista de resultados procesados
        return result


    def addDeviceClassNode(self, api_login: API, parser_detail_devices_class: list[dict]) -> list[dict]:
        """
        Agrega nodos de clases de dispositivos en Zenoss utilizando la información proporcionada.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - parser_detail_devices_class (list[dict]): Lista de diccionarios que contienen información detallada
          de las clases de dispositivos. Cada diccionario tiene una clave que representa la ruta completa
          de la clase y un valor que contiene los detalles de la clase.

        Retorna:
        - resultAddDevicesClass (list[dict]): Lista de diccionarios que contienen los datos enviados a la API
          y las respuestas obtenidas al agregar los nodos de clases de dispositivos.
        """

        resultAddDevicesClass = []  # Lista para almacenar los resultados de las operaciones

        # Iterar sobre cada entrada en la lista de clases de dispositivos
        for device_entry in parser_detail_devices_class:
            # Iterar sobre cada clave (ruta completa) y valor (detalles) en el diccionario
            for full_path, details in device_entry.items():
                # Procesar la ruta completa para construir los UIDs intermedios
                path_parts = full_path.split('/')[1:]  # Ignorar el primer elemento 'Devices'
                current_uid = "/zport/dmd/Devices"  # Iniciar con la ruta base

                # Construir y agregar nodos intermedios para cada segmento de la ruta
                for part in path_parts:
                    current_uid = f"{current_uid}/{part}"  # Construir el UID actual
                    data = {
                        "connectionInfo": [],  # Información de conexión (vacía para nodos intermedios)
                        "description": "",  # Descripción (vacía para nodos intermedios)
                        "id": part,  # ID del nodo actual
                        "uid": current_uid.rsplit('/', 1)[0]  # UID del nodo padre (sin el último segmento)
                    }
                    # Agregar el nodo utilizando la API
                    response = api_login.addDeviceClassNode(data)
                    # Actualizar los datos con la respuesta de la API
                    data.update({"addDeviceClass": response})
                    # Agregar los datos y la respuesta a la lista de resultados
                    resultAddDevicesClass.append(data)

                # Procesar el nodo final con los detalles completos
                data = {
                    "connectionInfo": details.get("connectionInfo", []),  # Información de conexión
                    "description": details.get("description", ""),  # Descripción
                    "id": details["id"],  # ID del nodo final
                    "uid": details["uid"]  # UID completo del nodo final
                }
                # Agregar el nodo final utilizando la API
                response = api_login.addDeviceClassNode(data)
                # Actualizar los datos con la respuesta de la API
                data.update({"addDeviceClass": response})
                # Agregar los datos y la respuesta a la lista de resultados
                resultAddDevicesClass.append(data)

        # Retornar la lista de resultados
        return resultAddDevicesClass
    

    def getZenProperty(self, api_login: API, device_or_uid: Union[dict, str]) -> dict:
        """
        Obtiene las propiedades Zen (ZenProperty) de un dispositivo o UID específico.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - device_or_uid (Union[dict, str]): Puede ser un diccionario que representa un dispositivo
          (debe contener la clave 'uid') o una cadena que representa directamente un UID.

        Retorna:
        - Union[dict, Any]: Si `device_or_uid` es un diccionario, retorna el mismo diccionario
          con una nueva clave 'modelerPlugin' que contiene las propiedades Zen.
          Si `device_or_uid` es una cadena, retorna directamente las propiedades Zen.
        """

        # Verificar si el parámetro es un diccionario (representa un dispositivo)
        if isinstance(device_or_uid, dict):
            # Obtener el UID del diccionario del dispositivo
            uid = device_or_uid.get('uid')
            # Obtener las propiedades Zen utilizando la API
            get_zen_property = api_login.getZenProperty(uid)
            # Agregar las propiedades Zen al diccionario del dispositivo
            device_or_uid['modelerPlugin'] = get_zen_property
            # Retornar el diccionario actualizado
            return device_or_uid
        else:
            # Si el parámetro es una cadena (UID), obtener las propiedades Zen directamente
            get_zen_property = api_login.getZenProperty(device_or_uid)
            # Retornar las propiedades Zen
            return get_zen_property


    def setZenPropertyModel(self, api_login: API, data: dict) -> dict:
        """
        Establece o actualiza las propiedades Zen (ZenProperty) en Zenoss utilizando los datos proporcionados.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - data (dict): Un diccionario que contiene los datos necesarios para establecer las propiedades Zen.
          Este diccionario debe incluir al menos las claves 'uid', 'zProperty' y 'value'.

        Retorna:
        - dict: Un diccionario que contiene la respuesta de la API después de intentar establecer las propiedades Zen.
        """

        # Llamar al método setZenPropertyModel de la API para establecer las propiedades Zen
        set_zenp_roperty = api_login.setZenPropertyModel(data)

        # Retornar la respuesta de la API
        return set_zenp_roperty


    def getZenPropertiesGeneral(self, api_login: API) -> dict:
        """
        Obtiene las propiedades Zen generales desde la API de Zenoss.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.

        Retorna:
        - dict: Un diccionario que contiene las propiedades Zen generales obtenidas desde la API.
        """

        # Obtener las propiedades Zen generales utilizando la API
        get_zen_properties_general = api_login.getZenPropertiesGeneral()

        # Retornar las propiedades Zen generales
        return get_zen_properties_general


    def setZenPropertyGeneral(self, api_login: API, zProperty: str, value: str) -> dict:
        """
        Establece o actualiza una propiedad Zen general en Zenoss.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - zProperty (str): El nombre de la propiedad Zen que se desea establecer o actualizar.
        - value (str): El valor que se asignará a la propiedad Zen.

        Retorna:
        - dict: Un diccionario que contiene la respuesta de la API después de intentar establecer la propiedad Zen.
        """

        # Llamar al método setZenPropertyGeneral de la API para establecer la propiedad Zen
        set_zenp_roperty = api_login.setZenPropertyGeneral(zProperty, value)

        # Retornar la respuesta de la API
        return set_zenp_roperty


    def getPropertiesRouterGeneral(self, api_login: API) -> dict:
        """
        Obtiene las propiedades personalizadas (custom properties) del enrutador general desde la API de Zenoss.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.

        Retorna:
        - dict: Un diccionario que contiene las propiedades personalizadas del enrutador general obtenidas desde la API.
        """

        # Obtener las propiedades personalizadas del enrutador general utilizando la API
        get_properties_router_general = api_login.getPropertiesRouterGeneral()

        # Retornar las propiedades personalizadas del enrutador general
        return get_properties_router_general


    def addPropertiesRouterGeneral(self, api_login: API, data: dict) -> dict:
        """
        Agrega una propiedad personalizada (custom property) del enrutador general en Zenoss.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - data (dict): Un diccionario que contiene los datos de la propiedad personalizada que se desea agregar.

        Retorna:
        - dict: Un diccionario que contiene la respuesta de la API después de intentar agregar la propiedad.
        """

        # Llamar al método addPropertiesRouterGeneral de la API para agregar la propiedad personalizada
        add_properties_route_general = api_login.addPropertiesRouterGeneral(data)

        # Retornar la respuesta de la API
        return add_properties_route_general


    def detailDevices(self, api_login: API, devices: list) -> list:
        """
        Obtiene y procesa detalles adicionales de una lista de dispositivos, incluyendo propiedades personalizadas,
        propiedades de configuración y credenciales.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - devices (list): Lista de diccionarios que representan dispositivos.

        Retorna:
        - list: La lista de dispositivos actualizada con propiedades personalizadas, propiedades de configuración
          y credenciales procesadas. Retorna `None` si ocurre un error.
        """
        
        try:
            # Recorrer cada dispositivo en la lista
            for device in devices:
                # Obtener las propiedades personalizadas del dispositivo
                custom_properties = api_login.getPropertiesRouter(device)

                # Obtener las propiedades de configuración del dispositivo
                configuration_properties = api_login.getZenProperties(device)

                # Filtrar propiedades personalizadas para incluir solo las locales (islocal == 1)
                filtered_custom_properties = [
                    prop for prop in custom_properties.get('data', []) if prop.get("islocal") == 1
                ]

                # Filtrar propiedades de configuración para incluir solo las locales (islocal == 1)
                filtered_configuration_properties = [
                    prop for prop in configuration_properties.get('data', []) if prop.get("islocal") == 1
                ]

                # Ejecutar un comando para obtener las contraseñas del dispositivo
                run_command = api_login.runCommand(device.get('uid'), 'password')

                # Parsear y extraer las credenciales desde la respuesta HTML
                dict_passwords = Html().extractBase64Html(run_command)

                # Agregar las propiedades filtradas como nuevas claves en el diccionario del dispositivo
                device["custom_properties"] = filtered_custom_properties
                device["configuration_properties"] = filtered_configuration_properties

                # Reemplazar valores de propiedades con las credenciales obtenidas
                replace_values_properties = self.replaceValuesProperties(device, dict_passwords)
                device["replace_values_properties"] = replace_values_properties

            # Retornar la lista de dispositivos actualizada
            return devices

        except Exception as error:
            # Capturar y mostrar cualquier excepción que ocurra durante el proceso
            print(f"Error en detailDevices: {error}")
            return None


    def replaceValuesProperties(self, original_dict: dict, replacement_values: dict) -> bool:
        """
        Reemplaza valores en las propiedades personalizadas y de configuración de un dispositivo
        utilizando un diccionario de valores de reemplazo.

        Parámetros:
        - original_dict (dict): Un diccionario que representa un dispositivo y contiene
          las claves 'custom_properties' y 'configuration_properties'.
        - replacement_values (dict): Un diccionario que contiene los valores de reemplazo,
          donde las claves son los IDs de las propiedades y los valores son los nuevos valores.

        Retorna:
        - bool: True si el reemplazo se realizó correctamente, False si no hay valores de reemplazo.
        """

        # Verificar si hay valores de reemplazo
        if replacement_values:
            # Reemplazar valores en 'custom_properties' y 'configuration_properties'
            for key in ('custom_properties', 'configuration_properties'):
                # Obtener la lista de propiedades usando el operador walrus (:=)
                if prop_list := original_dict.get(key):
                    # Iterar sobre cada propiedad en la lista
                    for prop in prop_list:
                        # Obtener el ID de la propiedad usando el operador walrus (:=)
                        if prop_id := prop.get('id'):
                            # Verificar si el ID está en los valores de reemplazo
                            if prop_id in replacement_values:
                                # Reemplazar el valor y su representación como cadena
                                prop['value'] = replacement_values[prop_id]
                                prop['valueAsString'] = replacement_values[prop_id]
        else:
            # Mostrar un mensaje de error si no hay valores de reemplazo
            print(f"Error in update custom: {original_dict.get('ipAddressString')}")
            return False

        # Retornar True si el reemplazo se realizó correctamente
        return True


    def parseDeviceData(self, devices: list) -> list:
        """
        Procesa y transforma una lista de dispositivos en un formato específico para su uso posterior.

        Parámetros:
        - devices (list): Lista de diccionarios que representan dispositivos con sus atributos.

        Retorna:
        - list: Una lista de diccionarios que representan los dispositivos en un formato procesado.
        """

        # Inicializar la lista de dispositivos procesados
        parsed_devices = []

        # Iterar sobre cada dispositivo en la lista
        for device in devices:
            # Crear un diccionario con los datos procesados del dispositivo
            parsed_device = {
                "deviceName": device["ipAddressString"],  # Usar 'ipAddressString' como nombre del dispositivo
                "deviceClass": re.search(r'Devices(/.+)/devices', device["uid"]).group(1),  # Extraer la clase del dispositivo desde 'uid'
                "collector": device["collector"],  # Asignar el colector del dispositivo
                "model": False,  # Valor por defecto para 'model'
                "title": device["name"],  # Usar 'name' como título del dispositivo
                "productionState": device["productionState"],  # Mantener el estado de producción
                "priority": device["priority"],  # Mantener la prioridad del dispositivo
                "snmpCommunity": "",  # Valor por defecto para la comunidad SNMP
                "snmpPort": "161",  # Valor por defecto para el puerto SNMP
                "tag": device["tagNumber"],  # Usar 'tagNumber' como etiqueta del dispositivo
                "rackSlot": "",  # Valor por defecto para la ranura del rack
                "serialNumber": device["serialNumber"],  # Mantener el número de serie del dispositivo
                "hwManufacturer": "",  # Valor por defecto para el fabricante del hardware
                "hwProductName": "",  # Valor por defecto para el nombre del producto de hardware
                "osManufacturer": "",  # Valor por defecto para el fabricante del sistema operativo
                "osProductName": "",  # Valor por defecto para el nombre del producto del sistema operativo
                "comments": "",  # Valor por defecto para comentarios
                "locationPath": device.get("location", {}).get("name", "") if device.get("location") else "",  # Extraer la ruta de ubicación si existe
                "groupPaths": [group["path"] for group in device["groups"]],  # Extraer las rutas de los grupos
                "systemPaths": [system["path"] for system in device["systems"]],  # Extraer las rutas de los sistemas
                "zProperties": {
                    "zWinRMUser": "",  # Valor por defecto para el usuario de WinRM
                    "zWinRMPassword": "",  # Valor por defecto para la contraseña de WinRM
                    "zWinKDC": "",  # Valor por defecto para el KDC de WinRM
                    "zWinScheme": "http",  # Valor por defecto para el esquema de WinRM
                    "zWinRMPort": "5985",  # Valor por defecto para el puerto de WinRM
                }
            }
            # Agregar el dispositivo procesado a la lista
            parsed_devices.append(parsed_device)

        # Retornar la lista de dispositivos procesados
        return parsed_devices


    def mergeDeviceData(self, parse_device_data: list, detail_devices: list) -> list:
        """
        Combina dos listas de dispositivos en una sola lista, fusionando la información de cada dispositivo
        basándose en su dirección IP o nombre.

        Parámetros:
        - parse_device_data (list): Lista de dispositivos procesados con información básica.
        - detail_devices (list): Lista de dispositivos con información detallada.

        Retorna:
        - list: Una lista de diccionarios que combina la información de ambas listas, donde cada diccionario
          contiene las claves 'deviceAdd' (información básica) y 'deviceDetail' (información detallada).
        """

        # Crear un mapa de los dispositivos de detail_devices usando 'ipAddressString' como clave
        detail_map = {device['ipAddressString']: device for device in detail_devices}

        # Inicializar la lista de dispositivos fusionados
        merged_devices = []

        # Iterar sobre los dispositivos en parse_device_data
        for device in parse_device_data:
            # Obtener la IP o nombre del dispositivo desde 'deviceName'
            device_ip = device.get('deviceName')

            # Verificar si el dispositivo existe en detail_map
            if device_ip in detail_map:
                # Obtener la información detallada del dispositivo desde detail_map
                detail = detail_map[device_ip]

                # Fusionar la información básica y detallada en un nuevo diccionario
                merged_devices.append({
                    'deviceAdd': device,      # Información básica del dispositivo
                    'deviceDetail': detail    # Información detallada del dispositivo
                })

        # Retornar la lista de dispositivos fusionados
        return merged_devices


    def addDevice(self, api_login: API, device: dict) -> dict:
        """
        Agrega un dispositivo y configura sus propiedades personalizadas y de configuración.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - device (dict): Un diccionario que contiene la información del dispositivo a agregar,
          incluyendo 'deviceAdd' (datos básicos) y 'deviceDetail' (datos detallados).

        Retorna:
        - dict: El diccionario del dispositivo actualizado con los resultados de la operación.
        """

        try:
            # Extraer los datos básicos y detallados del dispositivo
            deviceAdd = device.get('deviceAdd')
            deviceDetail = device.get('deviceDetail')

            # Verificar si el dispositivo tiene una IP válida
            if deviceDetail.get('ipAddressString') is None:
                device['resultDeviceAdd'] = {
                    "success": False,
                    "message": "El dispositivo no tiene una IP válida."
                }
                return device

            # Verificar si el dispositivo es único (no existe previamente)
            if deviceDetail.get('unique'):
                # Agregar el dispositivo utilizando la API
                add_device = api_login.addDevice(deviceAdd)
            else:
                # Si el dispositivo ya existe, no se agrega
                add_device = {
                    "success": True,
                    "message": "El dispositivo ya existe"
                }

            # Guardar el resultado de la operación en el diccionario del dispositivo
            device['resultDeviceAdd'] = add_device

            # Si el dispositivo se agregó correctamente, configurar sus propiedades
            if add_device.get('success'):
                # Configurar las propiedades de configuración
                for configuration_properties in deviceDetail.get('configuration_properties', []):
                    setZenProperty = api_login.setZenProperty(
                        deviceDetail.get('uid'),
                        self.processConfigurationProperties(configuration_properties)
                    )
                    configuration_properties['result_set_zenp_roperty'] = setZenProperty.get('success', False)

                # Configurar las propiedades personalizadas
                for custom_properties in deviceDetail.get('custom_properties', []):
                    result_add_properties_router = api_login.addPropertiesRouter(
                        deviceDetail.get('uid'),
                        custom_properties
                    )
                    if result_add_properties_router.get('success'):
                        custom_properties['result_add_properties_router'] = result_add_properties_router.get('success', False)
                    else:
                        # Si no se puede agregar, intentar actualizar la propiedad
                        result_update_properties_router = api_login.updatePropertiesRouter(
                            deviceDetail.get('uid'),
                            custom_properties
                        )
                        custom_properties['result_update_properties_router'] = result_update_properties_router.get('success', False)
            else:
                # Si no se pudo agregar el dispositivo, guardar un mensaje de error
                output = f"Error no se agregó el dispositivo. {deviceDetail.get('ipAddressString')} - {add_device.get('msg')}"
                device['resultDeviceAdd'] = output

        except Exception as error:
            # Capturar y manejar cualquier excepción que ocurra durante el proceso
            device['resultDeviceAdd'] = f"Error no se procesó: {error}"

        # Retornar el diccionario del dispositivo con los resultados
        return device


    def addTemplateGeneralNode(self, api_login: API, template_class: str) -> dict:
        """
        Agrega nodos de plantillas generales en Zenoss, construyendo rutas iterativamente.

        Parámetros:
        - api_login (API): Una instancia de la clase API que permite interactuar con Zenoss.
        - template_class (str): Una cadena que representa la ruta de la plantilla en formato de ruta (por ejemplo, "Devices/Server/Linux").

        Retorna:
        - dict: Un diccionario que contiene los resultados de la operación de agregado para cada ruta construida.
        """
        
        # Diccionario para almacenar los resultados de la operación
        add_templates = {}

        # Dividir la ruta de la plantilla en componentes
        components = template_class.split("/")

        # Ignorar el prefijo inicial "Devices" si está presente
        if components[0] == "Devices":
            components = components[1:]

        # Construir rutas iterativamente y agregar nodos de plantillas
        current_path = "/zport/dmd/Devices"  # Ruta base inicial
        for component in components:
            # Construir la ruta actual
            current_path += f"/{component}"

            # Crear el diccionario de la plantilla
            template = {
                "id": component,  # ID del nodo (nombre del componente)
                "targetUid": current_path  # Ruta completa del nodo
            }

            # Agregar el nodo de plantilla utilizando la API
            add_template_general_result = api_login.addTemplateGeneral(template)

            # Almacenar el resultado en el diccionario
            add_templates[current_path] = add_template_general_result.get("success", False)

        # Retornar un diccionario con la ruta original y los resultados
        return {template_class: add_templates}


    def updatePropertiesRouterGeneral(self, api_login: API, id: str, value: str) -> dict:
        """
        Actualiza las propiedades generales de un router utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la actualización.
        - id (str): Identificador de la propiedad que se desea actualizar.
        - value (str): Nuevo valor que se asignará a la propiedad.

        Retorna:
        - dict: Resultado de la operación de actualización.
        """
        # Llamar al método de la API para actualizar las propiedades generales del router
        update_properties_router_general = api_login.updatePropertiesRouterGeneral(id, value)
        
        # Retornar el resultado de la operación
        return update_properties_router_general

         
    def processConfigurationProperties(self, configuration_properties: dict) -> dict:
        """
        Procesa las propiedades de configuración, convirtiendo listas en cadenas concatenadas.

        Parámetros:
        - configuration_properties (dict): Un diccionario que contiene las propiedades de configuración.

        Retorna:
        - dict: Un diccionario con las propiedades procesadas, donde las listas se han convertido en cadenas.
        """
        # Iterar sobre cada clave y valor en el diccionario de propiedades de configuración
        for key, value in configuration_properties.items():
            # Verificar si el valor es una lista
            if isinstance(value, list):
                # Concatenar los elementos de la lista en una sola cadena, separados por saltos de línea
                configuration_properties[key] = '\n'.join(value)
        
        # Retornar el diccionario con las propiedades procesadas
        return configuration_properties

    
    def getTemplatesGeneralDetail(self, api_login: API, template: dict) -> list[dict]:
        """
        Obtiene los detalles generales de las plantillas asociadas a un dispositivo.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las consultas.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID.

        Retorna:
        - list[dict]: Una lista de diccionarios que contienen los detalles de cada plantilla.
        """
        # Obtener la lista de plantillas asociadas al dispositivo
        templates_device = api_login.getTemplates(template.get('uid'))
        
        # Lista para almacenar los detalles de cada plantilla
        templates_info = []
        
        # Iterar sobre cada plantilla obtenida
        for template_local in templates_device:
            # Obtener los detalles de la plantilla actual
            info_template_local = api_login.getInfoTemplate(template_local.get('uid'))
            info_template_local_data = info_template_local.get('data')
            
            # Agregar los detalles de la plantilla a la lista
            templates_info.append(info_template_local_data)
        
        # Retornar la lista con los detalles de las plantillas
        return templates_info


    def filterTemplateGeneral(self, templates: list) -> tuple[list, list]:
        """
        Filtra las plantillas generales en dos categorías: aquellas cuya definición contiene la ruta '/devices/' y aquellas que no.

        Parámetros:
        - templates (list): Una lista de diccionarios que contienen las plantillas generales.

        Retorna:
        - tuple[list, list]: Una tupla con dos listas:
            - without_devices: Plantillas cuya definición no contiene la ruta '/devices/'.
            - with_devices: Plantillas cuya definición contiene la ruta '/devices/'.
        """
        # Crear una lista de diccionarios con los campos necesarios
        filter_template_general = [
            {
                'definition': '/zport/dmd' + item['definition'],  # Agregar prefijo a la definición
                'id': item['id'],  # ID de la plantilla
                'description': item.get('description', ''),  # Descripción de la plantilla (opcional)
                'targetPythonClass': item.get('targetPythonClass', ''),  # Clase Python objetivo (opcional)
                'uid': item.get('uid', '')  # UID de la plantilla (opcional)
            }
            for item in templates
        ]
        
        # Filtrar las plantillas según si su definición contiene la ruta '/devices/'
        with_devices = [item for item in filter_template_general if re.search(r'/devices/', item['definition'])]
        without_devices = [item for item in filter_template_general if not re.search(r'/devices/', item['definition'])]
        
        # Retornar las dos listas filtradas
        return without_devices, with_devices
    

    def definitionUnique(self, templates: list) -> list:
        """
        Extrae las definiciones únicas de una lista de plantillas.

        Parámetros:
        - templates (list): Una lista de diccionarios que contienen las plantillas.

        Retorna:
        - list: Una lista de definiciones únicas.
        """
        # Usar un conjunto (set) para garantizar que los valores sean únicos
        unique_definitions = list({item['definition'] for item in templates})
        
        # Retornar la lista de definiciones únicas
        return unique_definitions

        
    def addTemplateGeneral(self, api_login: API, template: dict) -> dict:
        """
        Agrega una plantilla general utilizando la API proporcionada. Si la plantilla ya existe, se elimina antes de agregarla nuevamente.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID, nombre y definición.

        Retorna:
        - dict: El diccionario de la plantilla con un campo adicional que indica si la operación de agregado fue exitosa.
        """
        try:
            # Verificar si la plantilla ya existe
            get_template = api_login.getTemplates(template.get('uid'))
            
            # Si la plantilla existe, eliminarla
            if get_template:
                api_login.deleteTemplate(template.get('uid'))
            
            # Preparar los datos para agregar la plantilla
            add_template = {
                "id": template.get('name'),  # Nombre de la plantilla
                "targetUid": f"/zport/dmd{template.get('definition')}"  # Ruta completa de la plantilla
            }
            
            # Llamar a la API para agregar la plantilla
            add_template_general_result = api_login.addTemplateGeneral(add_template)
            
            # Agregar el resultado de la operación al diccionario de la plantilla
            template["templateGeneral_add"] = add_template_general_result.get("success", False)
        
        except Exception as error:
            # En caso de error, marcar la operación como fallida
            template["templateGeneral_add"] = False
        
        # Retornar el diccionario de la plantilla con el resultado de la operación
        return template


    def addTemplateLocal(self, api_login: API, template: dict) -> dict:
        """
        Agrega una plantilla local utilizando la API proporcionada. Si la plantilla ya existe, se elimina antes de agregarla nuevamente.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID, nombre y definición.

        Retorna:
        - dict: El diccionario de la plantilla con un campo adicional que indica si la operación de agregado fue exitosa.
        """
        add_template_general_result = None  # Inicializar la variable para almacenar el resultado de la operación
        try:
            # Construir el UID completo de la plantilla
            uid = f"/zport/dmd{template.get('definition')}"
            
            # Verificar si la plantilla ya existe
            get_template = api_login.getInfo(template.get('uid'))
            
            # Si la plantilla existe, eliminarla
            if get_template.get('success', False):
                remove_local_template = {
                    "deviceUid": uid,  # UID del dispositivo
                    "templateId": template.get('uid')  # ID de la plantilla
                }
                api_login.removeLocalTemplate(template.get('uid'), remove_local_template)
            
            # Preparar los datos para agregar la plantilla local
            add_template = {
                "deviceUid": uid,  # UID del dispositivo
                "templateId": template.get('name')  # Nombre de la plantilla
            }
            
            # Llamar a la API para agregar la plantilla local
            add_template_general_result = api_login.addTemplateLocal(uid, add_template)
            
            # Verificar si la operación fue exitosa o si la plantilla ya está en uso
            template["templateLocal_add"] = add_template_general_result.get('success', False) or ('it is already in use' in add_template_general_result.get('msg', ''))
        
        except Exception as error:
            # En caso de error, imprimir el mensaje de error y marcar la operación como fallida
            print(f"Error in addTemplateLocal {template.get('uid')} \n{error}")
            template["templateLocal_add"] = False
        
        # Retornar el diccionario de la plantilla con el resultado de la operación
        return template
    

    def getAddTemplateTargets(self, api_login: API) -> dict:
        """
        Obtiene los objetivos (targets) disponibles para agregar plantillas utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la consulta.

        Retorna:
        - dict: Un diccionario que contiene los objetivos disponibles para agregar plantillas.
        """
        # Llamar al método de la API para obtener los objetivos de agregado de plantillas
        get_add_template_targets = api_login.getAddTemplateTargets()
        
        # Retornar el resultado de la operación
        return get_add_template_targets
        

    def getDeviceClassTemplates(self, api_login: API) -> list:
        """
        Obtiene las plantillas asociadas a las clases de dispositivos utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la consulta.

        Retorna:
        - list: Una lista de plantillas asociadas a las clases de dispositivos.
        """
        # Llamar al método de la API para obtener las plantillas de clases de dispositivos
        get_device_class_templates = api_login.getDeviceClassTemplates()[0]
        
        # Retornar la lista de plantillas (children) o una lista vacía si no hay resultados
        return get_device_class_templates.get('children', [])
    

    def getInfoTemplate(self, api_login: API, template: dict) -> dict:
        """
        Obtiene los detalles de una plantilla específica utilizando la API proporcionada y los agrega al diccionario de la plantilla.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la consulta.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID.

        Retorna:
        - dict: El diccionario de la plantilla con un campo adicional que contiene los detalles de la plantilla.
        """
        # Llamar al método de la API para obtener los detalles de la plantilla
        get_info_template = api_login.getInfoTemplate(template.get('uid'))
        
        # Agregar los detalles de la plantilla al diccionario de la plantilla
        template['detailTemplate'] = get_info_template.get('data', {})
        
        # Retornar el diccionario de la plantilla con los detalles agregados
        return template


    def getInfoTemplateLocal(self, api_login: API, template: dict) -> dict:
        """
        Obtiene los detalles de una plantilla local específica utilizando la API proporcionada y los agrega al diccionario de la plantilla.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la consulta.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID.

        Retorna:
        - dict: El diccionario de la plantilla con un campo adicional que contiene los detalles de la plantilla local.
        """
        # Llamar al método de la API para obtener los detalles de la plantilla local
        get_info_template_local = api_login.getInfoTemplate(template.get('uid'))
        
        # Agregar los detalles de la plantilla local al diccionario de la plantilla
        template['templateLocal'] = get_info_template_local.get('data', {})
        
        # Retornar el diccionario de la plantilla con los detalles agregados
        return template
    

    def getTemplatesDeviceLocal(self, api_login: API, template: dict) -> dict:
        """
        Verifica si una plantilla es local para un dispositivo específico utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la consulta.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID y nombre.

        Retorna:
        - dict: El diccionario de la plantilla con un campo adicional que indica si la plantilla es local.
        """
        # Obtener la lista de plantillas locales asociadas al dispositivo
        get_info_template_local = api_login.getTemplatesDeviceLocal(template.get('uid').rpartition('/')[0])
        
        # Inicializar el campo que indica si la plantilla es local como False
        template['isTemplateLocal'] = False
        
        # Iterar sobre las plantillas locales para verificar si la plantilla actual es local
        for template_local in get_info_template_local:
            # Extraer el nombre de la plantilla local
            name = template_local.get('uid').rpartition('/')[2]
            
            # Verificar si el nombre y la ruta coinciden con la plantilla actual
            if template.get('name') == name and template_local.get('path') == "Locally Defined":
                template['isTemplateLocal'] = True  # Marcar la plantilla como local
                break  # Salir del bucle una vez que se encuentra la coincidencia
        
        # Retornar el diccionario de la plantilla con el campo actualizado
        return template


    def setInfoTemplate(self, api_login: API, template: dict) -> dict:
        """
        Configura la información de una plantilla utilizando la API proporcionada, si la plantilla fue agregada previamente.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar la operación.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su nombre, clase Python, descripción y UID.

        Retorna:
        - dict: El diccionario de la plantilla con un campo adicional que indica si la operación de configuración fue exitosa.
        """
        # Verificar si la plantilla fue agregada previamente (templateGeneral_add es True)
        if template.get('templateGeneral_add', False):
            # Preparar los datos para configurar la información de la plantilla
            data = {
                "newId": template.get('name'),  # Nuevo nombre de la plantilla
                "targetPythonClass": template.get('targetPythonClass'),  # Clase Python objetivo
                "description": template.get('description'),  # Descripción de la plantilla
                "uid": template.get('uid')  # UID de la plantilla
            }
            
            # Llamar al método de la API para configurar la información de la plantilla
            set_info_template = api_login.setInfo(data)
            
            # Agregar el resultado de la operación al diccionario de la plantilla
            template['infoTemplate_set'] = set_info_template.get('success', False)
        else:
            # Si la plantilla no fue agregada previamente, marcar la operación como fallida
            template['infoTemplate_set'] = False
        
        # Retornar el diccionario de la plantilla con el resultado de la operación
        return template
        

    def getDataSources(self, api_login: API, data_source_types: list, template: dict) -> dict:
        """
        Obtiene los data sources, thresholds y gráficos asociados a una plantilla utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las consultas.
        - data_source_types (list): Lista de tipos de data sources que se desean obtener.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo su UID.

        Retorna:
        - dict: Un diccionario que contiene los data sources, thresholds y gráficos asociados a la plantilla.
        """
        try:
            # Verificar si la plantilla fue agregada previamente
            if template.get('templateGeneral_add', template):
                uid = template.get("uid")
                
                # Si es un componente, ajustar el UID
                if "uid_template" in template:
                    parte_relevante = template.get('uid_template').split('/rrdTemplates/')[-1]
                    uid = f"{template.get('uid_component')}/{parte_relevante}" if "uid_template" in template else template.get("uid")
                
                # Obtener los data sources
                data_sources = api_login.getDataSources(uid)
                
                # Verificar que los data sources existan y contengan la clave "data"
                if data_sources and "data" in data_sources:
                    # Crear una lista para almacenar los datos de los data sources
                    get_dataapoint = []
                    
                    # Iterar sobre cada data source
                    for ds in data_sources.get("data"):
                        # Omitir si no está dentro de los tipos especificados
                        if ds.get('type', None) in data_source_types or data_source_types == []:
                            # Obtener detalles del data source
                            ds_details = api_login.getDataSourceDetails(ds.get("uid"))
                            
                            # Extraer el 'record' y eliminar las claves no deseadas
                            record_data = {key: value for key, value in ds_details.get("record", {}).items() if key not in {"availableParsers", "form"}}
                            
                            # Obtener los data points asociados al data source
                            dp_details = api_login.getDataSources(record_data.get("uid"))
                            record_data.update({'datapoints': dp_details.get('data', []), 'validType': True})
                            
                            # Agregar el data source con los datos del 'record' a la lista
                            get_dataapoint.append(record_data)
                        else:
                            get_dataapoint.append({'datapoints': [], 'validType': False})
                    
                    # Obtener los thresholds asociados a la plantilla
                    get_thresholds = api_login.getThresholds(uid)
                    get_thresholds = self.findThreshold(get_dataapoint, get_thresholds.get('data', []))
                    
                    # Eliminar espacios en blanco al final de la clave 'uid' en cada threshold
                    cleaned_thresholds = [{**item, 'uid': item['uid'].rstrip()} if 'uid' in item else item for item in get_thresholds]
                    
                    # Obtener los gráficos asociados a la plantilla
                    get_graphs = api_login.getGraphs(uid)
                    
                    # Obtener los data points que incluye cada gráfico
                    for graph_points in get_graphs:
                        points = api_login.getGraphPoints(graph_points.get("uid"))
                        
                        # Eliminar espacios en blanco al final de la clave 'uid' en cada punto
                        cleaned_points = [{**item, 'uid': item['uid'].rstrip()} if 'uid' in item else item for item in points.get('data', [])]
                        graph_points['getGraphPoints'] = cleaned_points
                    
                    # Crear la estructura final con los data sources, thresholds y gráficos
                    detail_template = {
                        'datasources': get_dataapoint or [],  # Data sources (o lista vacía si no hay)
                        'thresholds': cleaned_thresholds or [],  # Thresholds (o lista vacía si no hay)
                        'graphs': get_graphs or []  # Gráficos (o lista vacía si no hay)
                    }
                    
                    # Retornar la estructura final
                    return detail_template
        except Exception as error:
            # En caso de error, imprimir el mensaje de error
            print(f"Error in getDataSources: {error} \n{template.get('uid')}")
        
        # Retornar un diccionario vacío en caso de error o si no se cumple la condición inicial
        return {}


    def addDataSource(self, api_login: API, template: dict) -> dict:
        """
        Agrega y configura data sources a una plantilla utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo sus data sources.

        Retorna:
        - dict: El diccionario de la plantilla con campos adicionales que indican si las operaciones de agregado y configuración fueron exitosas.
        """
        try:
            # Iterar sobre cada data source en la plantilla
            for datasource in template.get('datasources', []):
                success_add, success_set = False, False  # Inicializar variables para almacenar el éxito de las operaciones
                
                # Verificar si el data source tiene un nombre y es de un tipo válido
                if datasource.get("name") and datasource.get('validType', False):
                    # Agregar el data source a la plantilla
                    add_result = api_login.addDataSource(template.get('uid'), datasource)
                    success_add = add_result.get('success', False) if add_result else False
                    
                    # Crear una copia del data source excluyendo ciertas claves
                    excluded_keys = {
                        'datapoints', 'validType', 'description', 'name', 'source', 'meta_type',
                        'testable', 'inspector_type', 'type', 'id'
                    }
                    datasource_copy = {key: value for key, value in datasource.items() if key not in excluded_keys}
                    
                    # Configurar la información del data source si la operación de agregado fue exitosa
                    set_result = api_login.setInfo(datasource_copy) if success_add else None
                    success_set = set_result.get('success', False) if set_result else False
                
                # Actualizar el data source con los resultados de las operaciones
                datasource.update({'dataSource_add': success_add, 'dataSource_set': success_set})
        
        except KeyError as key_error:
            # Registrar errores de clave faltante
            logging.error(f"KeyError in addDataSource: {key_error} \n{template.get('uid')}")
        except Exception as error:
            # Registrar errores inesperados
            logging.error(f"Unexpected error in addDataSource: {error} \n{template.get('uid')}")
        
        # Retornar el diccionario de la plantilla actualizado
        return template


    def addDataPoint(self, api_login: API, template: dict) -> dict:
        """
        Agrega puntos de datos (data points) a los data sources de una plantilla utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo sus data sources y data points.

        Retorna:
        - dict: El diccionario de la plantilla con campos adicionales que indican si las operaciones de agregado de data points fueron exitosas.
        """
        try:
            # Iterar sobre cada data source en la plantilla
            for datasource in template.get('datasources', []):
                # Verificar si el data source fue agregado previamente
                if datasource.get('dataSource_add', False):
                    # Iterar sobre cada data point en el data source
                    for datapoint in datasource.get('datapoints', []):
                        if datapoint:  # Verificar si el data point no es None o vacío
                            # Agregar el data point utilizando la API
                            add_data_point = api_login.addDataPoint(datapoint.get('newId'), datasource.get('uid'))
                            
                            # Actualizar el data point con el resultado de la operación
                            datapoint.update({'dataPoint_add': add_data_point.get('success', False)})
                        else:
                            # Si el data point es None o vacío, marcar la operación como fallida
                            datapoint.update({'dataPoint_add': False})
        except Exception as error:
            # En caso de error, imprimir un mensaje de error
            print(f"Error in addDataPoint: {template.get('uid')} - {error}")
        
        # Retornar el diccionario de la plantilla actualizado
        return template


    def setDataPoint(self, api_login: API, template: dict) -> dict:
        """
        Configura los puntos de datos (data points) de los data sources de una plantilla utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo sus data sources y data points.

        Retorna:
        - dict: El diccionario de la plantilla con campos adicionales que indican si las operaciones de configuración de data points fueron exitosas.
        """
        try:
            # Iterar sobre cada data source en la plantilla
            for datasource in template.get('datasources', []):
                # Verificar si el data source fue agregado previamente
                if datasource.get('dataSource_add', False):
                    # Iterar sobre cada data point en el data source
                    for datapoint in datasource.get('datapoints', []):
                        # Verificar si el data point existe y fue agregado previamente
                        if datapoint and datapoint.get('dataPoint_add', False):
                            # Crear una copia del data point excluyendo ciertas claves
                            excluded_keys = {'isrow', 'leaf', 'availableRRDTypes', 'name', 'rate', 'meta_type', 'inspector_type', 'type', 'id'}
                            datapoint_copy = {key: value for key, value in datapoint.items() if key not in excluded_keys}
                            
                            # Procesar los alias del data point
                            excluded_keys = {'description', 'meta_type', 'inspector_type', 'id', 'uid'}
                            datapoint_copy["aliases"] = [
                                {("id" if key == "name" else key): value for key, value in alias.items() if key not in excluded_keys}
                                for alias in datapoint_copy.get("aliases", [])
                            ]
                            
                            # Configurar la información del data point utilizando la API
                            set_data_point = api_login.setInfo(datapoint_copy)
                            
                            # Actualizar el data point con el resultado de la operación
                            datapoint.update({'dataPoint_set': set_data_point.get('success', False)})
                        else:
                            # Si el data point no existe o no fue agregado previamente, marcar la operación como fallida
                            datapoint.update({'dataPoint_set': False})
        except Exception as error:
            # En caso de error, imprimir un mensaje de error
            print(f"Error in setDataPoint: {template.get('uid')} - {error}")
        
        # Retornar el diccionario de la plantilla actualizado
        return template
        

    def addThreshold(self, api_login: API, template: dict) -> dict:
        """
        Agrega y configura umbrales (thresholds) a una plantilla utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo sus umbrales.

        Retorna:
        - dict: El diccionario de la plantilla con campos adicionales que indican si las operaciones de agregado y configuración de umbrales fueron exitosas.
        """
        try:
            # Iterar sobre cada umbral en la plantilla
            for threshold in template.get('thresholds', []):
                # Agregar el umbral utilizando la API
                add_threshold = api_login.addThreshold(template.get('uid'), threshold)
                
                # Actualizar el umbral con el resultado de la operación de agregado
                threshold.update({'threshold_add': add_threshold.get('success') if add_threshold else None})
                
                # Si el umbral fue agregado exitosamente, configurar su información
                if add_threshold and add_threshold.get('success'):
                    # Crear una copia del umbral excluyendo ciertas claves
                    excluded_keys = {'dataPoints', 'meta_type', 'newId', 'inspector_type', 'type', 'id'}
                    threshold_copy = {key: value for key, value in threshold.items() if key not in excluded_keys}
                    
                    # Configurar la información del umbral utilizando la API
                    set_info_threshold = api_login.setInfo(threshold_copy)
                    
                    # Actualizar el umbral con el resultado de la operación de configuración
                    threshold.update({'threshold_set': set_info_threshold.get('success') if set_info_threshold else None})
        except Exception as error:
            # En caso de error, imprimir un mensaje de error
            print(f"Error en addThreshold: \n{template}")
        
        # Retornar el diccionario de la plantilla actualizado
        return template
    

    def addGraphDefinition(self, api_login: API, template: dict) -> dict:
        """
        Agrega y configura definiciones de gráficos (graph definitions) a una plantilla utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Objeto de la API que permite realizar las operaciones.
        - template (dict): Un diccionario que contiene la información de la plantilla, incluyendo sus gráficos, data sources y thresholds.

        Retorna:
        - dict: El diccionario de la plantilla con campos adicionales que indican si las operaciones de agregado y configuración de gráficos fueron exitosas.
        """
        uid = template.get('uid')  # Obtener el UID de la plantilla
        try:
            # Iterar sobre cada gráfico en la plantilla
            for graphs in template.get('graphs', []):
                # Verificar si el gráfico ya existe y eliminarlo si es necesario
                get_graphs = api_login.getGraphs(graphs.get('uid'))
                if not 'success' in get_graphs:
                    api_login.deleteGraphDefinition(graphs.get('uid'))
                
                # Agregar la definición del gráfico utilizando la API
                add_graph_definition = api_login.addGraphDefinition(uid, graphs)
                
                # Actualizar el gráfico con el resultado de la operación de agregado
                graphs.update({'graphDefinition_add': add_graph_definition.get('success') if add_graph_definition else None})
                
                # Si el gráfico fue agregado exitosamente, configurar su información
                if add_graph_definition.get('success', False):
                    # Crear una copia del gráfico excluyendo ciertas claves
                    excluded_keys = {
                        'sequence', 'fakeGraphCommands', 'id', 'autoscale', 'custom', 'width', 
                        'graphPoints', 'ceiling', 'rrdVariables', 'name', 'meta_type', 'inspector_type'
                    }
                    graphs_copy = {key: value for key, value in graphs.items() if key not in excluded_keys}
                    
                    # Configurar la definición del gráfico utilizando la API
                    set_graph_definition = api_login.setGraphDefinition(graphs_copy)
                    
                    # Actualizar el gráfico con el resultado de la operación de configuración
                    graphs.update({'graphDefinition_set': set_graph_definition.get('success') if set_graph_definition else None})
                    
                    # Agregar los data points o thresholds al gráfico
                    datasources = template.get('datasources', {})
                    for point in graphs.get('getGraphPoints', []):
                        # Crear una copia del punto excluyendo ciertas claves
                        excluded_keys = {
                            'description', 'id', 'meta_type', 'rrdVariables', 'inspector_type', 
                            'cFunc', 'type', 'legend', 'dataPointUid'
                        }
                        
                        # Si el punto es de tipo DataPoint
                        if point.get('type') == 'DataPoint':
                            # Buscar coincidencias en los data sources
                            for item in datasources:
                                for datapoint in item.get('datapoints', []):
                                    # Reemplazar '.' por '_' en el nombre del data point
                                    modified_name = datapoint['name'].replace('.', '_')
                                    
                                    # Comparar con el nombre del punto en el gráfico
                                    if modified_name == point.get('dpName'):
                                        # Actualizar el UID del data point en el gráfico
                                        point.update({'dataPointUid': datapoint.get('uid')})
                                        
                                        # Agregar el data point al gráfico utilizando la API
                                        add_data_point_to_graph = api_login.addDataPointToGraph(datapoint.get('uid'), graphs.get('uid'))
                                        point.update({'dataPointToGraph_add': add_data_point_to_graph.get('success') if add_data_point_to_graph else False})
                                        
                                        # Si el data point fue agregado exitosamente, configurar su información
                                        if add_data_point_to_graph.get('success', False):
                                            point_copy = {key: value for key, value in point.items() if key not in excluded_keys}
                                            set_info_point_to_graph = api_login.setInfo(point_copy)
                                            point.update({'infoPointToGraph_set': set_info_point_to_graph.get('success') if set_info_point_to_graph else False})
                        
                        # Si el punto es de tipo Threshold
                        else:
                            thresholds = template.get('thresholds', [])
                            # Buscar coincidencias en los thresholds
                            for threshold in thresholds:
                                if threshold.get('name') == point.get('name'):
                                    # Actualizar el UID del threshold en el gráfico
                                    point.update({'dataPointUid': threshold.get('uid')})
                                    
                                    # Agregar el threshold al gráfico utilizando la API
                                    add_threshold_to_graph = api_login.addThresholdToGraph(threshold.get('uid'), graphs.get('uid'))
                                    point.update({'thresholdToGraph_add': add_threshold_to_graph.get('success') if add_threshold_to_graph else None})
                                    
                                    # Si el threshold fue agregado exitosamente, configurar su información
                                    if add_threshold_to_graph.get('success', False):
                                        point_copy = {key: value for key, value in point.items() if key not in excluded_keys}
                                        set_info_threshold_to_graph = api_login.setInfo(point_copy)
                                        point.update({'thresholdToGraph_set': set_info_threshold_to_graph.get('success') if set_info_threshold_to_graph else None})
        except Exception as error:
            # En caso de error, imprimir un mensaje de error
            print(f"Error en addGraphDefinition: {uid} \n{error}")
        
        # Retornar el diccionario de la plantilla actualizado
        return template
        

    def findThreshold(self, datasources: list, thresholds: list) -> list:
        """
        Filtra los umbrales (thresholds) basándose en los nombres de datapoints procesados
        que están presentes en las fuentes de datos (datasources).

        Parámetros:
        - datasources (list): Una lista de diccionarios que contienen las fuentes de datos y sus datapoints.
        - thresholds (list): Una lista de diccionarios que representan los umbrales a filtrar.

        Retorna:
        - filtered_thresholds (list): Una lista de umbrales filtrados que contienen solo los nombres de datapoints válidos.
        """
        # Crear un conjunto para almacenar los nombres de datapoints procesados
        datapoint_names: set = set()

        # Recorrer cada fuente de datos en la lista de datasources
        for datasource in datasources:
            # Obtener la lista de datapoints de la fuente de datos actual (si existe)
            datapoints: list = datasource.get('datapoints', [])
            
            # Recorrer cada datapoint en la lista de datapoints
            for datapoint in datapoints:
                # Reemplazar los puntos (.) por guiones bajos (_) en el nombre del datapoint
                processed_name: str = datapoint['name'].replace('.', '_')
                # Agregar el nombre procesado al conjunto de nombres de datapoints
                datapoint_names.add(processed_name)

        # Crear una lista para almacenar los umbrales filtrados
        filtered_thresholds: list = []

        # Recorrer cada umbral en la lista de thresholds
        for threshold in thresholds:
            # Obtener la lista de nombres de datapoints (dsnames) del umbral actual
            threshold_dsnames: list = threshold.get('dsnames', [])
            
            # Filtrar los nombres de datapoints que están presentes en el conjunto de datapoint_names
            valid_dsnames: list = [dsname for dsname in threshold_dsnames if dsname in datapoint_names]
            
            # Si hay nombres válidos, actualizar el umbral y agregarlo a la lista filtrada
            if valid_dsnames:
                threshold['dsnames'] = valid_dsnames
                filtered_thresholds.append(threshold)

        # Retornar la lista de umbrales filtrados
        return filtered_thresholds
    

    def findThreshold(self, datasources: list, thresholds: list) -> list:
        """
        Filtra los umbrales (thresholds) basándose en los nombres de datapoints procesados
        que están presentes en las fuentes de datos (datasources).

        Parámetros:
        - datasources (list): Una lista de diccionarios que contienen las fuentes de datos y sus datapoints.
        - thresholds (list): Una lista de diccionarios que representan los umbrales a filtrar.

        Retorna:
        - list: Una lista de umbrales filtrados que contienen solo los nombres de datapoints válidos.
        """
        # Crear un conjunto para almacenar los nombres de datapoints procesados
        datapoint_names = set()

        # Recorrer cada fuente de datos en la lista de datasources
        for datasource in datasources:
            # Obtener la lista de datapoints de la fuente de datos actual (si existe)
            datapoints = datasource.get('datapoints', [])
            
            # Recorrer cada datapoint en la lista de datapoints
            for datapoint in datapoints:
                # Reemplazar los puntos (.) por guiones bajos (_) en el nombre del datapoint
                processed_name = datapoint['name'].replace('.', '_')
                # Agregar el nombre procesado al conjunto de nombres de datapoints
                datapoint_names.add(processed_name)

        # Crear una lista para almacenar los umbrales filtrados
        filtered_thresholds = []

        # Recorrer cada umbral en la lista de thresholds
        for threshold in thresholds:
            # Obtener la lista de nombres de datapoints (dsnames) del umbral actual
            threshold_dsnames = threshold.get('dsnames', [])
            
            # Filtrar los nombres de datapoints que están presentes en el conjunto de datapoint_names
            valid_dsnames = [dsname for dsname in threshold_dsnames if dsname in datapoint_names]
            
            # Si hay nombres válidos, actualizar el umbral y agregarlo a la lista filtrada
            if valid_dsnames:
                threshold['dsnames'] = valid_dsnames
                filtered_thresholds.append(threshold)

        # Retornar la lista de umbrales filtrados
        return filtered_thresholds
    

    # -----------------------------------
    # setBoundTemplates
    # -----------------------------------
    def setBoundTemplates(self, api_login : API, template: dict):
        try:
            # Obtener los tipos validos de datasources.
            set_bound_templates = api_login.setBoundTemplates(template)
            template.update({'set_bound_templates' : set_bound_templates.get('success', False)})
        except Exception as error:
            pass
        return template


    # ████████╗███████╗███╗   ███╗██████╗ ██╗      █████╗ ████████╗███████╗
    # ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝
    #    ██║   █████╗  ██╔████╔██║██████╔╝██║     ███████║   ██║   █████╗  
    #    ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  
    #    ██║   ███████╗██║ ╚═╝ ██║██║     ███████╗██║  ██║   ██║   ███████╗
    #    ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

    # -----------------------------------
    # getTemplatesGeneral
    # -----------------------------------
    def getTemplatesGeneral(self, api_login: API) -> dict:
        """
        Obtiene las plantillas generales utilizando la API proporcionada.

        Parámetros:
        - api_login (API): Una instancia de la clase API que contiene el método getTemplatesGeneral.

        Retorna:
        - get_templates_general: El resultado de la llamada a la API, que contiene las plantillas generales.
        """
        # Llama al método getTemplatesGeneral de la instancia api_login para obtener las plantillas generales
        get_templates_general = api_login.getTemplatesGeneral()
        
        # Retorna el resultado obtenido de la API
        return get_templates_general
    

    #  █████╗  █████╗ ███╗   ███╗██████╗  █████╗ ███╗  ██╗███████╗███╗  ██╗████████╗███████╗ ██████╗
    # ██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗████╗ ██║██╔════╝████╗ ██║╚══██╔══╝██╔════╝██╔════╝
    # ██║  ╚═╝██║  ██║██╔████╔██║██████╔╝██║  ██║██╔██╗██║█████╗  ██╔██╗██║   ██║   █████╗  ╚█████╗ 
    # ██║  ██╗██║  ██║██║╚██╔╝██║██╔═══╝ ██║  ██║██║╚████║██╔══╝  ██║╚████║   ██║   ██╔══╝   ╚═══██╗
    # ╚█████╔╝╚█████╔╝██║ ╚═╝ ██║██║     ╚█████╔╝██║ ╚███║███████╗██║ ╚███║   ██║   ███████╗██████╔╝
    #  ╚════╝  ╚════╝ ╚═╝     ╚═╝╚═╝      ╚════╝ ╚═╝  ╚══╝╚══════╝╚═╝  ╚══╝   ╚═╝   ╚══════╝╚═════╝ 

    def getComponentTree(self, api_login: API, template: dict) -> dict:
        """
        Obtiene el árbol de componentes de un dispositivo utilizando su 'uid' proporcionado en el diccionario 'template'.
        
        Esta función hace uso de una API externa para:
        1. Obtener el árbol de componentes del dispositivo mediante la llamada `getComponentTree`.
        2. Iterar sobre cada componente en el árbol y obtener los detalles de los componentes de cada uno mediante la llamada `getComponents`.
        3. Actualizar el árbol de componentes con los detalles obtenidos.
        
        Si ocurre un error durante el proceso, se captura la excepción y se muestra un mensaje de error, devolviendo un mensaje 
        de error en lugar del árbol de componentes.
        
        Args:
            api_login (API): Instancia de la API para hacer las llamadas necesarias.
            template (dict): Diccionario que contiene el 'uid' del dispositivo para obtener el árbol de componentes.
        
        Returns:
            dict: Un diccionario con el 'uid' del dispositivo y el árbol de componentes obtenidos (o mensaje de error en caso de fallo).
        """
        try:
            # Obtener el árbol de los componentes del dispositivo usando el 'uid' del template
            get_component_tree = api_login.getComponentTree(template.get('uid'))
            
            # Iterar sobre cada componente en el árbol obtenido
            for component_tree in get_component_tree:
                # Obtener los detalles de los componentes del dispositivo utilizando su 'id'
                components = api_login.getComponents(template.get('uid'), component_tree.get('id'))
                
                # Actualizar el componente con la lista de componentes obtenida
                component_tree.update({'components': components})
        
        except Exception as error:
            # Manejar cualquier error y mostrar un mensaje con el error
            print(f"Error en getComponentTree: {template.get('uid')} \n{error}")
            
            # En caso de error, asignar un mensaje de error a la variable
            get_component_tree = "Error al obtener los componentes."
        
        # Retornar el 'uid' y el árbol de componentes (o mensaje de error)
        return {
            'uid': template.get('uid'),
            'component_tree': get_component_tree
        }


    def getComponentLocal(self, api_login: API, template: dict) -> dict:
        """
        Filtra los componentes locales de un dispositivo basándose en la presencia de una dirección IP en los datos de los componentes.
        
        Esta función recorre el árbol de componentes de un dispositivo, y para cada componente, obtiene sus plantillas asociadas. 
        Si encuentra que la plantilla de un componente contiene una dirección IP en su 'uid', considera dicho componente 
        como local y lo agrega a una lista filtrada. Solo los componentes locales se mantienen en el árbol de componentes 
        del dispositivo. Si no se encuentran componentes locales, la función retorna None.
        
        Args:
            api_login (API): Instancia de la API para hacer las llamadas necesarias.
            template (dict): Diccionario que contiene el 'uid' del dispositivo y su árbol de componentes.
        
        Returns:
            dict or None: Retorna el template con el árbol de componentes filtrado o None si no se encuentran componentes locales.
        """
        # Expresión regular para identificar una dirección IP
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

        # Crear una lista para almacenar los component_tree que tienen componentes locales
        filtered_component_trees = []

        # Recorrer cada elemento en el árbol de componentes
        for component_tree in template.get('component_tree', []):
            components = component_tree.get('components', {})
            data = components.get('data', [])

            # Crear una lista para almacenar los componentes que cumplen con la condición
            filtered_data = []

            # Recorrer cada componente en la lista de componentes
            for component in data:
                # Obtener el árbol de los componentes del dispositivo
                get_obj_templates = api_login.getObjTemplates(template.get('uid'), component.get('uid'))
                template_data = get_obj_templates.get('data', [])

                # Verificar si hay datos en el template
                if template_data:
                    # Buscar la dirección IP en la cadena 'uid'
                    is_local = bool(re.search(ip_pattern, template_data[0].get('uid', '')))

                    # Si es local, mantener el componente; de lo contrario, eliminarlo
                    if is_local:
                        component.update({'template' : template_data[0]})
                        filtered_data.append(component)

            # Actualizar la lista de componentes con los filtrados
            components['data'] = filtered_data

            # Si filtered_data no está vacío, mantener el component_tree
            if filtered_data:
                filtered_component_trees.append(component_tree)

        # Si no hay component_tree con componentes locales, retornar None
        if not filtered_component_trees:
            return None

        # Actualizar el template con los component_tree que tienen componentes locales
        template['component_tree'] = filtered_component_trees

        # Retornar el template modificado
        return template


    def getComponentTemplate(self, api_login: API, template: dict) -> dict:
        """
        Obtiene el template del componente de un dispositivo basado en su 'uid'.
        
        Esta función recorre el árbol de componentes de un dispositivo, obtiene las plantillas asociadas a cada 
        componente, y filtra aquellas cuya 'uid' no contiene una dirección IP. Luego, para cada componente, 
        se actualiza un diccionario con la información relevante: 'uid' del dispositivo, 'uid' del componente, 
        y el 'uid' del template filtrado.
        
        Args:
            api_login (API): Instancia de la API para hacer las llamadas necesarias.
            template (dict): Diccionario que contiene el 'uid' del dispositivo y su árbol de componentes.
        
        Returns:
            dict: Un diccionario con los 'uid' del dispositivo, componente y template filtrado.
        """
        # Diccionario para almacenar los templates de los componentes
        component_template = {}

        # Recorrer cada componente en el árbol de componentes
        for component_tree in template["component_tree"]:
            for component in component_tree["components"]["data"]:
                objTemplates = component.get('template')

                # Obtener la lista de templates para el dispositivo
                templates_device = api_login.getTemplates(objTemplates.get('uid'))

                # Expresión regular para detectar una dirección IP en el uid
                ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

                # Filtrar elementos cuyo uid no contiene una dirección IP
                uid_components = [item for item in templates_device if not ip_pattern.search(item['uid'])]

                # Actualizar el diccionario con los 'uid' correspondientes
                component_template.update({'uid' : template.get('uid')})
                component_template.update({'uid_component' : component.get('uid')})
                component_template.update({'uid_template' : uid_components[0].get('uid')})

        # Retornar el diccionario con la información de los templates
        return component_template


    def makeLocalRRDTemplate(self, api_login: API, template: dict) -> dict:
        """
        Crea un template RRD local para un componente específico y actualiza el template con el resultado.
        
        Esta función realiza una llamada a la API para crear un template RRD local, utilizando los 'uid' del 
        dispositivo, componente y template. Luego, actualiza el diccionario 'template' con el resultado de la operación.
        
        Args:
            api_login (API): Instancia de la API para hacer las llamadas necesarias.
            template (dict): Diccionario que contiene los 'uid' del dispositivo, componente y template.
        
        Returns:
            dict: El template actualizado con el resultado de la creación del template RRD local.
        """
        try:
            # Validar que exista el identificador del componente y realizar la operación de creación del template RRD local
            set_local = api_login.makeLocalRRDTemplate(template.get('uid'), template.get('uid_component'), template.get('uid_template'))
            
            # Actualizar el template con el resultado de la operación (éxito o fallo)
            template.update({"set_local_component" : set_local.get('success', False)})
        except Exception as error:
            # Actualizar el template con el resultado de la operación fallo
            template.update({"set_local_component" : False})
        # Retornar el template actualizado
        return template
    

    def componentAddDataSource(self, api_login: API, template: dict) -> dict:
        """
        Agrega un DataSource a un componente y actualiza el estado de la operación en el template.
        
        Esta función recorre la lista de datasources proporcionada en el template, y para cada uno de ellos, realiza las siguientes
        acciones:
        1. Verifica si el datasource tiene un nombre y es de tipo válido.
        2. Agrega el datasource usando la API.
        3. Actualiza la información del datasource usando la API.
        4. Si ocurre un error, se captura y se registra el error.
        
        Args:
            api_login (API): Instancia de la API para realizar las operaciones necesarias.
            template (dict): Diccionario que contiene información sobre el componente y los datasources.
        
        Returns:
            dict: El template actualizado con los resultados de las operaciones de agregar y actualizar los datasources.
        """
        try:
            # Proceso para migrar template.
            for datasource in template.get('datasources', []):
                # Obtener la parte relevante del uid_template.
                parte_relevante = template.get('uid_template').split('/rrdTemplates/')[-1]
                
                # Combinar las dos partes para formar el uid completo.
                uid = f"{template.get('uid_component')}/{parte_relevante}"
                success_add, success_set = False, False
                
                # Verificar condiciones y ejecutar operaciones si son válidas
                if datasource.get("name") and datasource.get('validType', False):
                    # Agregar el datasource a través de la API
                    add_result = api_login.addDataSource(uid, datasource)
                    success_add = add_result.get('success', False) if add_result else False
                    
                    # Copiar el diccionario excluyendo ciertas claves
                    excluded_keys = {'datapoints', 'validType', 'description', 'name', 'source', 'meta_type', 'testable', 'inspector_type', 'type', 'id'}
                    datasource_copy = {key: value for key, value in datasource.items() if key not in excluded_keys}
                    
                    # Actualizar la información del datasource
                    set_result = api_login.setInfo(datasource_copy)
                    success_set = set_result.get('success', False) if set_result else False
                
                # Actualizar el datasource con los resultados de las operaciones
                datasource.update({'resultAdd': success_add, 'resultSet': success_set})
        
        except KeyError as key_error:
            # Registrar error si hay un KeyError
            logging.error(f"KeyError in componentAddDataSource: {key_error} \n{template.get('uid')}")
        
        except Exception as error:
            # Registrar cualquier error inesperado
            logging.error(f"Unexpected error in componentAddDataSource: {error} \n{template.get('uid')}")
        
        # Retornar el template actualizado
        return template


    def componentAddDataPoint(self, api_login : API, template):
        """
        Agrega puntos de datos a los datasources de un componente y actualiza el estado de la operación en el template.
        
        Esta función recorre la lista de datasources en el template y, para cada uno que haya sido agregado
        correctamente, agrega sus puntos de datos asociados. Luego, actualiza el estado de la operación para cada punto
        de datos en el datasource.
        
        Args:
            api_login (API): Instancia de la API para realizar las operaciones necesarias.
            template (dict): Diccionario que contiene información sobre los datasources y los puntos de datos.
        
        Returns:
            dict: El template actualizado con los resultados de la operación de agregar los puntos de datos.
        """
        try:
            # Evitar error si 'datasources' es None o vacío
            for datasource in template.get('datasources', []):

                # Si el datasource se agregó correctamente
                if datasource.get('resultAdd', False):

                    # Recorrer cada punto de datos del datasource
                    for datapoint in datasource.get('datapoints', []):

                        # Verificar si el datapoint es válido
                        if datapoint:
                            # Agregar el punto de datos local a través de la API
                            add_data_point = api_login.addDataPointLocal(template.get('uid'), datapoint.get('newId'), datasource.get('id'))
                            # Actualizar el datapoint con el resultado de la operación
                            datapoint.update({'resultAdd': add_data_point.get('success', False)})
                        else:
                            # Si el datapoint no es válido, establecer 'resultAdd' como False
                            datapoint.update({'resultAdd': False})
        
        except Exception as error:
            # Registrar cualquier error inesperado
            print(f"Error in componentAddDataPoint: {template.get('uid')} - {error}")
        
        # Retornar el template actualizado con los resultados
        return template


    def setDataPointLocal(self, api_login: API, template: dict) -> dict:
        """
        Actualiza los puntos de datos de los datasources en el template.
        
        Esta función recorre la lista de datasources en el template y, para cada uno que haya sido agregado correctamente,
        actualiza los puntos de datos asociados. Durante este proceso, se eliminan algunas claves innecesarias y se actualiza
        la información de cada punto de datos utilizando la API.
        
        Args:
            api_login (API): Instancia de la API para realizar las operaciones necesarias.
            template (dict): Diccionario que contiene información sobre los datasources y los puntos de datos.
        
        Returns:
            dict: El template actualizado con los resultados de la operación de actualización de los puntos de datos.
        """
        try:
            # Evitar error si 'datasources' es None o vacío
            for datasource in template.get('datasources', []):

                # Si el datasource se agregó correctamente
                if datasource.get('resultAdd', False):
                    # Recorrer cada punto de datos del datasource
                    for datapoint in datasource.get('datapoints', []):

                        # Verificar si el datapoint es válido y si se agregó correctamente
                        if datapoint and datapoint.get('resultAdd', False):
                            # Copiar el diccionario excluyendo ciertas claves innecesarias
                            excluded_keys = {'isrow', 'leaf', 'availableRRDTypes', 'name', 'rate', 'meta_type', 'inspector_type', 'type', 'id'}
                            datapoint_copy = {key: value for key, value in datapoint.items() if key not in excluded_keys}
                            
                            # Eliminar claves innecesarias y cambiar el nombre de 'name' a 'id' en los aliases
                            excluded_keys = {'description', 'meta_type', 'inspector_type', 'id', 'uid'}
                            datapoint_copy["aliases"] = [{("id" if key == "name" else key): value for key, value in alias.items() if key not in excluded_keys} for alias in datapoint_copy["aliases"]]
                            
                            # Actualizar los datos del datapoint a través de la API
                            set_data_point = api_login.setInfolocal(template.get('uid'), datapoint_copy)
                            # Actualizar el resultado de la operación de actualización
                            datapoint.update({'resultSet': set_data_point.get('success', False)})
                        else:
                            # Si el datapoint no es válido o no se agregó correctamente, establecer 'resultSet' como False
                            datapoint.update({'resultSet': False})
        
        except Exception as error:
            # Registrar cualquier error inesperado
            print(f"Error in setDataPoint: {template.get('uid')} - {error}")
        
        # Retornar el template actualizado con los resultados de la operación
        return template


    def addThresholdLocal(self, api_login : API, template: dict) -> dict:
        """
        Agrega umbrales (thresholds) locales a un dispositivo y actualiza el estado de la operación en el template.
        
        Esta función recorre la lista de umbrales en el template y, para cada uno, lo agrega utilizando la API.
        Luego, actualiza los umbrales excluyendo claves innecesarias y actualizando la información de cada umbral.
        
        Args:
            api_login (API): Instancia de la API para realizar las operaciones necesarias.
            template (dict): Diccionario que contiene información sobre los umbrales a agregar.
        
        Returns:
            dict: El template actualizado con los resultados de la operación de agregar los umbrales.
        """
        try:
            # Recorrer cada umbral en la lista 'thresholds'
            for threshold in template.get('thresholds', []):
                # Agregar el umbral local a través de la API
                add_threshold = api_login.addThresholdLocal(template.get('uid'), threshold)
                # Actualizar el resultado de la operación de agregar umbral
                threshold.update({'resultAdd': add_threshold.get('success', False) if add_threshold else None})
                
                # Si el umbral se agregó correctamente
                if add_threshold.get('success', False):
                    # Copiar el diccionario excluyendo claves innecesarias
                    excluded_keys = {'dataPoints', 'meta_type', 'newId', 'inspector_type', 'type', 'id'}
                    threshold_copy = {key: value for key, value in threshold.items() if key not in excluded_keys}
                    
                    # Actualizar la información del umbral
                    set_info_threshold = api_login.setInfolocal(template.get('uid'), threshold_copy)
                    # Actualizar el resultado de la operación de actualización de umbral
                    threshold.update({'resultSet': set_info_threshold.get('success', False) if set_info_threshold else None})
        
        except Exception as error:
            # Registrar cualquier error inesperado
            # print(f"Error en addThresholdLocal: \n{template.get('uid')}")
            pass
        
        # Retornar el template actualizado con los resultados de la operación
        return template
    

    def addGraphDefinitionLocal(self, api_login : API, template: dict) -> dict:
        """
        Agrega una definición de gráfico local a un dispositivo y actualiza el estado de la operación en el template.
        
        Esta función recorre la lista de gráficos en el template, y para cada uno, verifica si existe previamente y lo elimina.
        Luego, agrega la nueva definición de gráfico y actualiza su configuración.
        
        Args:
            api_login (API): Instancia de la API para realizar las operaciones necesarias.
            template (dict): Diccionario que contiene información sobre los gráficos a agregar.
        
        Returns:
            dict: El template actualizado con los resultados de la operación de agregar los gráficos.
        """
        uid = template.get('uid')
        try:
            # Recorrer cada gráfico en la lista 'graphs'
            for graphs in template.get('graphs', []):
                # Si existe la gráfica, se elimina previamente
                get_graphs = api_login.getGraphs(graphs.get('uid').split('/graphDefs')[0])

                if get_graphs:

                    # Buscar y eliminar el gráfico existente
                    for element_graphs in get_graphs:

                        if graphs.get('uid') == element_graphs.get('uid'):
                            api_login.deleteGraphDefinitionLocal(uid, graphs.get('uid'))
                            break

                # Agregar la nueva definición de gráfico
                add_graph_definition = api_login.addGraphDefinitionLocal(uid, template.get('uid_template'), graphs.get('name'))
                # Actualizar el resultado de la operación de agregar gráfico
                graphs.update({'resultAdd': add_graph_definition.get('success', False) if add_graph_definition else None})
                
                # Si la operación de agregar gráfico fue exitosa
                if add_graph_definition.get('success', False):
                    # Copiar el diccionario excluyendo ciertas claves
                    excluded_keys = {'sequence', 'fakeGraphCommands', 'id', 'autoscale', 'custom', 'width', 
                                    'graphPoints', 'ceiling', 'rrdVariables', 'name', 'meta_type', 'inspector_type'}
                    graphs_copy = {key: value for key, value in graphs.items() if key not in excluded_keys}
                    
                    # Actualizar la configuración de la gráfica
                    set_graph_definition = api_login.setGraphDefinitionLocal(uid, graphs_copy)
                    # Actualizar el resultado de la operación de actualización de gráfico
                    graphs.update({'resultSet': set_graph_definition.get('success', False) if set_graph_definition else None})

                    # Agregar los UID de cada data point a cada configuración de la gráfica
                    datasources = template.get('datasources', {})
                    for point in graphs.get('getGraphPoints', []):
                        # Copiar el diccionario excluyendo ciertas claves
                        excluded_keys = {'description', 'id', 'meta_type', 'rrdVariables', 'inspector_type', 'cFunc', 'type', 'legend', 'dataPointUid'}
                        
                        # Si el tipo de punto es 'DataPoint'
                        if point.get('type') == 'DataPoint':
                            # Buscar coincidencias con los datos de las fuentes

                            for item in datasources:

                                for datapoint in item.get('datapoints', []):
                                    # Reemplazar '.' por '_' en 'name' para coincidencia
                                    modified_name = datapoint['name'].replace('.', '_')

                                    # Comparar con el nombre del punto de gráfico
                                    if modified_name == point.get('dpName'):
                                        point.update({'dataPointUid': datapoint.get('uid')})
                                        # Agregar el data point al gráfico
                                        add_data_point_to_graph = api_login.addDataPointToGraph(datapoint.get('uid'), graphs.get('uid'))
                                        point.update({'addDataPointToGraph': add_data_point_to_graph.get('success', False) if add_data_point_to_graph else False})

                                        if add_data_point_to_graph.get('success', False):
                                            point_copy = {key: value for key, value in point.items() if key not in excluded_keys}
                                            set_info_point_to_graph = api_login.setInfo(point_copy)
                                            point.update({'setInfoPointToGraph': set_info_point_to_graph.get('success', False) if set_info_point_to_graph else False})
                        # Si es de tipo 'thresholds'
                        else:
                            thresholds = template.get('thresholds', [])
                            # Buscar coincidencias con los umbrales
                            for threshold in thresholds:

                                if threshold.get('name') == point.get('name'):
                                    point.update({'dataPointUid': threshold.get('uid')})
                                    # Agregar el umbral al gráfico
                                    add_threshold_to_graph = api_login.addThresholdToGraph(threshold.get('uid'), graphs.get('uid'))
                                    point.update({'addThresholdToGraph': add_threshold_to_graph.get('success', False) if add_threshold_to_graph else None})

                                    if add_threshold_to_graph.get('success', False):
                                        point_copy = {key: value for key, value in point.items() if key not in excluded_keys}
                                        set_info_threshold_to_graph = api_login.setInfo(point_copy)
                                        point.update({'setInfoPointToGraph': set_info_threshold_to_graph.get('success', False) if set_info_threshold_to_graph else None})
        # Capturar y registrar cualquier error inesperado
        except Exception as error:
            # print(f"Error en addGraphDefinition: {uid} \n{error}")
            pass
        
        # Retornar el template actualizado con los resultados
        return template