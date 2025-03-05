#!/usr/bin/python
# -*- coding: utf-8 -*-

""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: migrate.py
Fecha: 26/11/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

https://docs.zenoss.com/api/reference/zenpackrouter.html

--------------------------------------------------------------------------------------------
NOTA: CUANDO SE CREE EL RESPALDO AGREGAR EL COLECTOR QUE SE VA A UTILIZAR ENESTE CASO ISSSTE
--------------------------------------------------------------------------------------------

https://zenoss5.labzenossmty
172.20.45.146
admin
Itoc.Triara521*

###### ISSSTE #####
172.20.45.146	zenoss5.mxap-itoc-issstezcc01
###### LAB #####
172.20.45.146	zenoss5.labzenossmty
172.20.45.203	zenoss5.labzenossmty2

Comandos:
    -- Contraseñas
    echo "'zCommandPassword'='${device/zCommandPassword}', 'zOraclePassword'='${device/zOraclePassword}', 'zVSphereEndpointPassword'='${device/zVSphereEndpointPassword}', 'zWinRMPassword'='${device/zWinRMPassword}', 'zSnmpAuthPassword'='${device/zSnmpAuthPassword}', 'zILOPassword'='${device/zILOPassword}', 'zMySqlPassword'='${device/zMySqlPassword}'" | base64 -w 0

    echo "'zCommandPassword'='$(printf "%s" "${device/zCommandPassword}" | base64)', 'zOraclePassword'='$(printf "%s" "${device/zOraclePassword}" | base64)', 'zVSphereEndpointPassword'='$(printf "%s" "${device/zVSphereEndpointPassword}" | base64)', 'zWinRMPassword'='$(printf "%s" "${device/zWinRMPassword}" | base64)', 'zSnmpAuthPassword'='$(printf "%s" "${device/zSnmpAuthPassword}" | base64)', 'zILOPassword'='$(printf "%s" "${device/zILOPassword}" | base64)', 'zMySqlPassword'='$(printf "%s" "${device/zMySqlPassword}" | base64)'"

    echo "'zCommandPassword'="$$(printf '%s' '${device/zCommandPassword}' | base64)", 'zOraclePassword'="$$(printf '%s' "${device/zOraclePassword}" | base64)", 'zVSphereEndpointPassword'="$$(printf '%s' "${device/zVSphereEndpointPassword}" | base64)", 'zWinRMPassword'="$$(printf '%s' "${device/zWinRMPassword}" | base64)", 'zSnmpAuthPassword'="$$(printf '%s' "${device/zSnmpAuthPassword}" | base64)", 'zILOPassword'="$$(printf '%s' "${device/zILOPassword}" | base64)", 'zMySqlPassword'="$$(printf '%s' "${device/zMySqlPassword}" | base64)""

https://docs.zenoss.com/api/reference/devicedumploadrouter.html
https://docs.huihoo.com/zenoss/5/api/Zenoss-JSON-API-r5.0.4/identifier-index.html

DeviceDumpLoadRouter

github
zerozerozero3
Gera992007

https://github.com/zerogera30/migration.git

--------------------------------------------------------------------------------------------------- """

import re
import os
import sys
import json
import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from zenoss.api import API
from zenoss.settings.zenPack import ZenPack
from zenoss.devices.devices import Devices
from zenoss.devices.Location import Location

# ---------------------------------------------------------------------------------------------------------------- #
# --- ███╗   ███╗██╗ ██████╗ ██████╗  █████╗ ████████╗███████╗    ██████╗ ███████╗██╗   ██╗██╗ █████╗ ███████╗ --- #
# --- ████╗ ████║██║██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ██╔══██╗██╔════╝██║   ██║██║██╔══██╗██╔════╝ --- #
# --- ██╔████╔██║██║██║  ██╗ ██████╔╝███████║   ██║   █████╗      ██║  ██║█████╗  ╚██╗ ██╔╝██║██║  ╚═╝█████╗   --- #
# --- ██║╚██╔╝██║██║██║  ╚██╗██╔══██╗██╔══██║   ██║   ██╔══╝      ██║  ██║██╔══╝   ╚████╔╝ ██║██║  ██╗██╔══╝   --- #
# --- ██║ ╚═╝ ██║██║╚██████╔╝██║  ██║██║  ██║   ██║   ███████╗    ██████╔╝███████╗  ╚██╔╝  ██║╚█████╔╝███████╗ --- #
# --- ╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝ ╚════╝ ╚══════╝ --- #
# ---------------------------------------------------------------------------------------------------------------- #

# Configuracion general.
workers_min = 60
workers_max = 120
# Configurar conexiones.
origin = "zenoss_mty"
destination = "zenoss_issste"


class MigrateDevice:
    """
    MigrateDevice
    """
    
    def migrate(self):
        """
        migrate
        """
        try:

            print(f"INICIA MIGRACION DE {origin} HACIA {destination}")

            # -------------------------------------------------------
            # --- INFORMACION DISPOSITIVOS --------------------------
            # -------------------------------------------------------
            # -------------------------------------------------------
            # Parte 1 : Necesario para las partes del 1 al 11 -------
            self.devicesExport()
            # -------------------------------------------------------
            # # Parte 2
            # self.filterDevices()
            # # Parte 3
            # self.devicesClasss()
            # # Parte 4
            # self.devicesConfiguration()
            # # Parte 5
            # self.addDeviceDetail()
            # -------------------------------------------------------
            
            # -------------------------------------------------------
            # --- TEMPLATE GENERAL ----------------------------------
            # -------------------------------------------------------
            # Parte 6 - Necesario para la parte 7 u 8 ---------------
            self.templateGeneral()
            # -------------------------------------------------------
            # Parte 7 -----------------------------------------------
            # self.templateGeneralConfig()
            # -------------------------------------------------------

            # -------------------------------------------------------
            # --- TEMPLATE LOCAL ------------------------------------
            # -------------------------------------------------------
            # Parte 8 -----------------------------------------------
            # self.templateLocal()
            # -------------------------------------------------------
            # Parte 9 -----------------------------------------------
            # self.configTemplateDevice()
            # -------------------------------------------------------

            # -------------------------------------------------------
            # --- COMPONENTES ---------------------------------------
            # -------------------------------------------------------
            # Parte 10 - Necesario para la parte 11 -----------------
            self.componentDevice()
            # Parte 11 ----------------------------------------------
            self.migrateComponentDevice()
            # -------------------------------------------------------

            print("TERMINA MIGRACION")

        except Exception as error:
            print(f"Error in migrate: {error}")


    def devicesExport(self):
        """
        Exporta dispositivos desde una instancia de Zenoss (origen) y los prepara para su importación en otra instancia (destino).

        Pasos principales:
        1. Obtiene la configuración inicial y crea sesiones con las APIs de exportación e importación.
        2. Obtiene los tipos de data source válidos.
        3. Recupera los dispositivos de las instancias de exportación e importación.
        4. Filtra los dispositivos que no están en la instancia de destino y agrega una clave 'unique'.
        5. Guarda los resultados en archivos JSON para su revisión.
        """
        # Registrar el tiempo de inicio del paso 01
        self.last_execution_time = log_time("PASO 01", None)

        # Configuración inicial -------------------------------------------------------------------
        # Obtener la configuración desde el archivo de configuración
        self.config = getConfig()

        # Crear instancias de API para exportación e importación
        self.api_export, self.api_import = map(
            lambda env: API(self.config['instance'][env]), 
            [origin, destination]
        )

        # Crear sesiones de autenticación con las APIs
        self.createSession()

        # DEVICES ---------------------------------------------------------------------------------
        # Crear una instancia de la clase Devices
        self.device = Devices()

        # Obtener los tipos de data source válidos ------------------------------------------------
        self.data_source_types = self.device.getDataSourceTypes(self.api_import)
        saveToFile(self.data_source_types, "01.1 - data_source_types.json")

        # Total de dispositivos a exportar --------------------------------------------------------
        # Export ----------------------------------------------------------------------------------
        # Obtener el colector de la instancia de origen
        collector = self.config.get('instance', {}).get(origin, {}).get('collector', None)

        # Obtener los dispositivos de la instancia de exportación
        get_devices_export = self.device.getDevices(self.api_export, collector)
        self.devices_export = get_devices_export.get('devices')
        saveToFile(self.devices_export, "01.2 - devices_export.json")

        # Import ----------------------------------------------------------------------------------
        # Obtener el colector de la instancia de destino
        collector = self.config.get('instance', {}).get(destination, {}).get('collector', None)

        # Obtener los dispositivos de la instancia de importación
        get_devices_import = self.device.getDevices(self.api_import, collector)
        self.devices_import = get_devices_import.get('devices')
        saveToFile(self.devices_import, '01.3 - devices_import.json')

        # Filtrar los dispositivos y agregar la clave 'unique' ------------------------------------
        # Filtra los dispositivos de exportación que no están en la instancia de importación
        self.devices_export_filter = self.device.addFilterDevices(self.devices_export, self.devices_import)
        saveToFile(self.devices_export_filter, '01.4 - devices_export_filter.json')

        # Cerrar las sesiones de autenticación
        self.closeSession()


    def filterDevices(self):
        """
        Filtra los dispositivos que aún no se han agregado a la instancia de destino y verifica
        si los ZenPacks necesarios están instalados.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 02.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Obtiene las clases de Python (ZenPacks) utilizadas por los dispositivos de exportación.
        4. Verifica si faltan ZenPacks por instalar en la instancia de destino.
        5. Filtra los dispositivos que no se han agregado a la instancia de destino.
        6. Guarda los resultados en archivos JSON para su revisión.
        7. Cierra las sesiones de autenticación.
        """
        # Registrar el tiempo de inicio del paso 02
        self.last_execution_time = log_time("PASO 02", self.last_execution_time)

        # Crear sesiones de autenticación con las APIs
        self.createSession()

        # ZENPACK ---------------------------------------------------------------------------------
        # Obtener las clases de Python (ZenPacks) utilizadas por los dispositivos de exportación
        python_class = self.device.getPythonClass(self.devices_export)
        saveToFile(python_class, '02.1 - python_class.json')

        # Verificar si faltan ZenPacks por instalar en la instancia de destino
        find_missing_packs = self.find_missing_packs(python_class)
        if find_missing_packs:
            print(f"Faltan ZenPacks por instalar: {find_missing_packs}")
            return None  # Detener el proceso si faltan ZenPacks

        # Dispositivos que no se agregaron --------------------------------------------------------
        # Filtrar los dispositivos que aún no se han agregado a la instancia de destino
        filtered_devices = [
            {
                "ipAddressString": device["ipAddressString"], 
                "name": device["name"]
            } 
            for device in self.devices_export 
            if device.get("unique") is True  # Solo dispositivos con 'unique' igual a True
        ]
        print(f"    Dispositivos que aún no se agregan: {len(filtered_devices)}")
        saveToFile(filtered_devices, '02.2 - filtered_devices.json')

        # Cerrar las sesiones de autenticación
        self.closeSession()


    def devicesClasss(self):
        """
        Procesa y agrega las clases de dispositivos (device classes) que no existen en la instancia de destino.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 03.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Obtiene y filtra las clases de dispositivos que no existen en la instancia de destino.
        4. Agrega las clases de dispositivos faltantes a la instancia de destino.
        5. Inicia procesos para los plugins de modelado (Modeler Plugins).
        6. Guarda los resultados en archivos JSON para su revisión.
        7. Cierra las sesiones de autenticación.
        """
        # Registrar el tiempo de inicio del paso 03
        self.last_execution_time = log_time("PASO 03", self.last_execution_time)

        # Crear sesiones de autenticación con las APIs
        self.createSession()

        # Obtener el listado de clases de dispositivos que se van a insertar ----------------------
        self.parser_devices_class_export = self.device.parserDevicesClass(self.devices_export_filter)
        saveToFile(self.parser_devices_class_export, '03.1 - parser_devices_class_export.json')

        # Obtener el listado de clases de dispositivos en la instancia de importación
        parser_devices_class_import = self.device.parserDevicesClass(self.devices_import)
        saveToFile(parser_devices_class_import, '03.2 - parser_devices_class_import.json')

        # Filtrar las clases de dispositivos que no existen en la instancia de destino ------------
        parser_devices_class_export_filter = list(
            set(self.parser_devices_class_export) - set(parser_devices_class_import)
        )
        saveToFile(parser_devices_class_export_filter, '03.3 - parser_devices_class_export_filter.json')

        # Obtener detalles de las clases de dispositivos filtradas -------------------------------
        detail_devices_class_export = self.device.detailDevicesClass(self.api_export, parser_devices_class_export_filter)
        saveToFile(detail_devices_class_export, '03.4 - detail_devices_class_export.json')

        # Agregar las clases de dispositivos a la instancia de destino ----------------------------
        add_device_class_node = self.device.addDeviceClassNode(self.api_import, detail_devices_class_export)
        saveToFile(add_device_class_node, '03.5 - add_device_class_node.json')

        # Iniciar proceso para los plugins de modelado (Modeler Plugins) --------------------------
        modeler_plugins = self.modelerPlugins()
        saveToFile(modeler_plugins, '03.6 - modeler_plugins.json')

        # Iniciar proceso para los plugins de modelado locales (Modeler Plugins Local) ------------
        modeler_plugins_local = self.modelerPluginsLocal()
        saveToFile(modeler_plugins_local, '03.7 - modeler_plugins_local.json')

        # Cerrar las sesiones de autenticación
        self.closeSession()


    def devicesConfiguration(self):
        """
        Configura los dispositivos migrando y actualizando propiedades de configuración, propiedades personalizadas,
        y la información de grupos, localidades y sistemas. Además, registra el tiempo de ejecución y guarda los
        resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 04.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Migra las propiedades de configuración general:
        - Obtiene las propiedades generales.
        - Actualiza las propiedades en la instancia de destino.
        4. Migra las propiedades personalizadas:
        - Obtiene las propiedades personalizadas.
        - Actualiza y añade las propiedades en la instancia de destino.
        5. Migra la información de grupos, localidades y sistemas:
        - Obtiene los grupos, localidades y sistemas de los dispositivos exportados.
        - Añade los detalles de las localidades en la instancia de destino.
        6. Guarda los resultados en archivos JSON para su revisión.
        7. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 04
        self.last_execution_time = log_time("PASO 04", self.last_execution_time)
        
        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Migración de propiedades de configuración general ---
        # Obtiene las propiedades de configuración general de los dispositivos
        configuration_properties_general = self.zenPropertiesGeneral()
        # Guarda las propiedades generales en un archivo JSON
        saveToFile(configuration_properties_general, '04.1 - configuration_properties_general.json')

        # Actualiza las propiedades de configuración general en la instancia de destino
        update_configuration_properties_general = self.updateZenProperty(configuration_properties_general)
        # Guarda el resultado de la actualización en un archivo JSON
        saveToFile(update_configuration_properties_general, '04.2 - update_configuration_properties_general.json')

        # --- Migración de propiedades personalizadas ---
        # Obtiene las propiedades personalizadas generales de los dispositivos
        custom_properties_general = self.propertiesRouterGeneral()
        # Actualiza las propiedades personalizadas en la instancia de destino
        update_properties_router_general = self.updatePropertiesRouter(custom_properties_general)
        # Guarda el resultado de la actualización en un archivo JSON
        saveToFile(update_properties_router_general, '04.3 - update_properties_router_general.json')

        # Añade las propiedades personalizadas generales en la instancia de destino
        add_properties_router_general = self.addPropertiesRouter(custom_properties_general)
        # Guarda el resultado de la adición en un archivo JSON
        saveToFile(add_properties_router_general, '04.4 - add_properties_router_general.json')

        # --- Migración de grupos, localidades y sistemas ---
        # Obtiene los grupos, localidades y sistemas de los dispositivos exportados
        get_group_location = Location().getGroupLocationSystem(self.devices_export)
        # Obtiene los detalles de las localidades
        get_location_detail = Location().getLocationDetail(self.api_export, get_group_location)
        # Añade los detalles de las localidades en la instancia de destino
        add_location_detail = Location().addLocationDetail(self.api_import, get_location_detail)
        # Guarda el resultado de la adición en un archivo JSON
        saveToFile(add_location_detail, '04.5 - add_location_detail.json')

        # Cerrar la sesión de autenticación
        self.closeSession()


    def addDeviceDetail(self):
        """
        Procesa y agrega los detalles de los dispositivos, incluyendo sus propiedades personalizadas (custom properties)
        y de configuración (configuration properties). Además, maneja la migración de dispositivos y la carga de nodos principales.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 05.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Obtiene los detalles de las propiedades personalizadas y de configuración de cada dispositivo.
        4. Identifica los dispositivos que no se actualizaron correctamente en sus propiedades.
        5. Procesa y fusiona los datos de los dispositivos para su migración.
        6. Migra los dispositivos a la instancia de destino.
        7. Carga los nodos principales necesarios para la configuración.
        8. Guarda los resultados en archivos JSON para su revisión.
        9. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 05
        self.last_execution_time = log_time("PASO 05", self.last_execution_time)
        
        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Obtener detalles de las propiedades de cada dispositivo ---
        # Obtiene las propiedades personalizadas y de configuración de cada dispositivo
        detail_devices = self.detailDevices(self.devices_export)
        # Guarda los detalles de los dispositivos en un archivo JSON
        saveToFile(detail_devices, '05.1 - detail_devices.json')

        # --- Identificar dispositivos con errores en la actualización de propiedades ---
        # Filtra los dispositivos que no se actualizaron correctamente en sus propiedades
        detail_devices_error = [item for item in detail_devices if not item["replace_values_properties"]]
        # Guarda los dispositivos con errores en un archivo JSON
        saveToFile(detail_devices_error, '05.2 - detail_devices_error.json')

        # ---------------------------------------------------------------------------------------------
        # NOTA: Aquí se debe agregar primero la lógica relacionada con la alta del Event Class (zport/dmd/Events/eventclasses)
        # ---------------------------------------------------------------------------------------------

        # --- Procesar y fusionar datos de dispositivos ---
        # Parsea los datos de los dispositivos exportados
        parse_device_data = self.parseDeviceData(self.devices_export)
        # Guarda los datos parseados en un archivo JSON
        saveToFile(parse_device_data, '05.3 - parse_device_data.json')

        # Fusiona los datos parseados con los detalles de los dispositivos
        merge_device_data = self.device.mergeDeviceData(parse_device_data, detail_devices)
        # Guarda los datos fusionados en un archivo JSON
        saveToFile(merge_device_data, '05.4 - merge_device_data.json')

        # --- Migrar dispositivos a la instancia de destino ---
        # Añade los dispositivos a la instancia de destino
        add_device = self.addDevice(merge_device_data)
        # Guarda el resultado de la migración en un archivo JSON
        saveToFile(add_device, '05.5 - add_device.json')
        
        # --- Cargar nodos principales ---
        # Añade los nodos principales necesarios para la configuración
        add_template_general_node = self.addTemplateGeneralNode(self.parser_devices_class_export)
        # Guarda el resultado de la carga de nodos en un archivo JSON
        saveToFile(add_template_general_node, '05.6 - add_template_general_node.json')

        # Cerrar la sesión de autenticación
        self.closeSession()


    def templateGeneral(self):
        """
        Procesa y obtiene los templates generales (plantillas) que se van a migrar, incluyendo su detalle
        y la separación entre templates maestros y locales. Además, registra el tiempo de ejecución y guarda
        los resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 06.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Obtiene el listado de templates generales que se van a migrar.
        4. Agrega el detalle de los templates y los separa en maestros y locales.
        5. Guarda los resultados en archivos JSON para su revisión.
        6. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 06
        self.last_execution_time = log_time("PASO 06", self.last_execution_time)

        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Obtener listado de templates generales ---
        # Obtiene el listado de templates generales desde la API de exportación
        templates_general = self.device.getTemplatesGeneral(self.api_export)
        # Guarda el listado de templates generales en un archivo JSON
        saveToFile(templates_general, "06.1 - templates_general.json")

        # --- Agregar detalle de los templates y separar por maestros y locales ---
        # Obtiene el detalle completo de los templates y los separa en maestros y locales
        self.templates_full = self.getTemplatesGeneralDetail(templates_general)
        # Guarda el detalle completo de los templates en un archivo JSON
        saveToFile(self.templates_full, "06.2 - templates_full.json")

        # NOTA: Si se necesita enviar un template específico, se puede modificar la variable `templates_full`
        # para incluir solo los templates deseados. Por ejemplo:
        # templates_full = {
        #     "local": [
        #         # Lista de templates locales específicos
        #     ]
        # }

        # Cerrar la sesión de autenticación
        self.closeSession()


    def templateGeneralConfig(self):
        """
        Configura y migra los templates generales (plantillas) a la nueva instancia, incluyendo la adición de
        templates, actualización de descripciones, y la migración de Data Sources, Thresholds y Graph Definitions.
        Además, registra el tiempo de ejecución y guarda los resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 07.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Agrega los templates generales a la nueva instancia.
        4. Actualiza la descripción de los templates.
        5. Inicia el proceso de migración de Data Sources, Thresholds y Graph Definitions:
        - Obtiene y agrega los Data Sources.
        - Agrega y actualiza los Data Points.
        - Migra los Thresholds.
        - Migra las Graph Definitions.
        6. Guarda los resultados en archivos JSON para su revisión.
        7. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 07
        self.last_execution_time = log_time("PASO 07", self.last_execution_time)

        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Agregar templates generales a la nueva instancia ---
        # Agrega los templates maestros a la nueva instancia
        add_template_general = self.addTemplateGeneral(self.templates_full.get('master'))  # [0:10] para limitar la cantidad
        # Guarda el resultado de la adición de templates en un archivo JSON
        saveToFile(add_template_general, "07.2 - add_template_general.json")

        # --- Actualizar la descripción de los templates ---
        # Actualiza la descripción de los templates agregados
        set_info_template = self.setInfoTemplate(add_template_general.get('process'))
        # Guarda el resultado de la actualización en un archivo JSON
        saveToFile(set_info_template, "07.3 - set_info_template.json")

        # --- Migración de Data Sources, Thresholds y Graph Definitions ---
        # Obtiene los Data Sources de los templates
        get_data_sources_template = self.getDataSources(self.data_source_types, set_info_template)
        # Guarda los Data Sources obtenidos en un archivo JSON
        saveToFile(get_data_sources_template, "07.4 - get_data_sources_template.json")

        # Agrega los Data Sources a los templates
        add_data_source_template = self.addDataSource(get_data_sources_template)
        # Guarda el resultado de la adición de Data Sources en un archivo JSON
        saveToFile(add_data_source_template, "07.5 - add_data_source_template.json")

        # Agrega los Data Points a los Data Sources
        add_data_point_template = self.addDataPoint(add_data_source_template)
        # Guarda el resultado de la adición de Data Points en un archivo JSON
        saveToFile(add_data_point_template, "07.6 - add_data_point_template.json")

        # Actualiza los Data Points en los Data Sources
        set_data_point_template = self.setDataPoint(add_data_source_template)
        # Guarda el resultado de la actualización de Data Points en un archivo JSON
        saveToFile(set_data_point_template, "07.7 - set_data_point_template.json")

        # --- Migración de Thresholds ---
        # Agrega los Thresholds a los Data Sources
        add_thresholds_template = self.addThresholds(add_data_source_template)
        # Guarda el resultado de la adición de Thresholds en un archivo JSON
        saveToFile(add_thresholds_template, "07.8 - add_thresholds_template.json")

        # --- Migración de Graph Definitions ---
        # Agrega las Graph Definitions a los Data Sources
        add_graph_definition_template = self.addGraphDefinition(add_data_source_template)
        # Guarda el resultado de la adición de Graph Definitions en un archivo JSON
        saveToFile(add_graph_definition_template, "07.9 - add_graph_definition_template.json")

        # Cerrar la sesión de autenticación
        self.closeSession()


    def templateLocal(self):
        """
        Configura y migra los templates locales (plantillas específicas de dispositivos) a la nueva instancia,
        incluyendo la adición de templates, validación de su localidad, y la migración de Data Sources, Thresholds
        y Graph Definitions. Además, registra el tiempo de ejecución y guarda los resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 08.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Filtra los templates locales que están asociados a los dispositivos exportados.
        4. Agrega los templates locales a la nueva instancia.
        5. Valida que los templates agregados sean locales en la nueva instancia.
        6. Inicia el proceso de migración de Data Sources, Thresholds y Graph Definitions:
        - Obtiene y agrega los Data Sources.
        - Agrega y actualiza los Data Points.
        - Migra los Thresholds.
        - Migra las Graph Definitions.
        7. Guarda los resultados en archivos JSON para su revisión.
        8. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 08
        self.last_execution_time = log_time("PASO 08", self.last_execution_time)

        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Filtrar templates locales asociados a dispositivos exportados ---
        # Filtra los templates locales que están asociados a los dispositivos exportados
        filter_templates_export = self.filterTemplatesExport(self.devices_export, self.templates_full.get('local'))
        # Guarda los templates filtrados en un archivo JSON
        saveToFile(filter_templates_export, '08.1 - filter_templates_export.json')

        # --- Agregar templates locales a la nueva instancia ---
        # Agrega los templates locales filtrados a la nueva instancia
        add_template_local = self.addTemplateLocal(filter_templates_export.get('templates'))
        # Guarda el resultado de la adición de templates locales en un archivo JSON
        saveToFile(add_template_local, '08.2 - add_template_local.json')

        # --- Validar que los templates agregados sean locales en la nueva instancia ---
        # Obtiene y valida la información de los templates locales en la nueva instancia
        is_template_local = self.getTemplatesDeviceLocal(filter_templates_export.get('templates'))
        # Guarda el resultado de la validación en un archivo JSON
        saveToFile(is_template_local, '08.3 - is_template_local.json')

        # --- Migración de Data Sources, Thresholds y Graph Definitions ---
        # Obtiene los Data Sources de los templates locales
        data_sources_template_local = self.getDataSources(self.data_source_types, is_template_local.get('locals'))  # [0:10] para limitar la cantidad
        # Guarda los Data Sources obtenidos en un archivo JSON
        saveToFile(data_sources_template_local, '08.4 - data_sources_template_local.json')

        # Agrega los Data Sources a los templates locales
        add_data_source_template_local = self.addDataSource(data_sources_template_local)
        # Guarda el resultado de la adición de Data Sources en un archivo JSON
        saveToFile(add_data_source_template_local, '08.5 - add_data_source_template_local.json')

        # Agrega los Data Points a los Data Sources de los templates locales
        add_data_point_template_local = self.addDataPoint(add_data_source_template_local)
        # Guarda el resultado de la adición de Data Points en un archivo JSON
        saveToFile(add_data_point_template_local, '08.6 - add_data_point_template_local.json')

        # Actualiza los Data Points en los Data Sources de los templates locales
        set_data_point_template_local = self.setDataPoint(add_data_point_template_local)
        # Guarda el resultado de la actualización de Data Points en un archivo JSON
        saveToFile(set_data_point_template_local, '08.7 - set_data_point_template_local.json')

        # --- Migración de Thresholds ---
        # Agrega los Thresholds a los Data Sources de los templates locales
        add_thresholds_template_local = self.addThresholds(set_data_point_template_local)
        # Guarda el resultado de la adición de Thresholds en un archivo JSON
        saveToFile(add_thresholds_template_local, '08.8 - add_thresholds_template_local.json')

        # --- Migración de Graph Definitions ---
        # Agrega las Graph Definitions a los Data Sources de los templates locales
        add_graph_definition_template = self.addGraphDefinition(add_thresholds_template_local)
        # Guarda el resultado de la adición de Graph Definitions en un archivo JSON
        saveToFile(add_graph_definition_template, '08.9 - add_graph_definition_template.json')

        # Cerrar la sesión de autenticación
        self.closeSession()


    def configTemplateDevice(self):
        """
        Configura y asigna los templates generales a los dispositivos en la nueva instancia, basándose en la
        configuración de los dispositivos exportados. Además, registra el tiempo de ejecución y guarda los
        resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 09.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Obtiene los templates generales asignados a cada dispositivo en la instancia de exportación.
        4. Asigna los templates generales a los dispositivos en la nueva instancia.
        5. Guarda los resultados en archivos JSON para su revisión.
        6. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 09
        self.last_execution_time = log_time("PASO 09", self.last_execution_time)
        
        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Obtener templates generales asignados a los dispositivos ---
        # Obtiene los templates generales que están asignados a cada dispositivo en la instancia de exportación
        templates_device_monitoring = self.getTemplatesDeviceMonitoring(self.devices_export)
        # Guarda los templates asignados a los dispositivos en un archivo JSON
        saveToFile(templates_device_monitoring, '09.1 - templates_device_monitoring.json')

        # --- Asignar templates generales a los dispositivos en la nueva instancia ---
        # Asigna los templates generales a los dispositivos en la nueva instancia
        set_bound_templates = self.setBoundTemplates(templates_device_monitoring)
        # Guarda el resultado de la asignación de templates en un archivo JSON
        saveToFile(set_bound_templates, '09.2 - set_bound_templates.json')

        # Cerrar la sesión de autenticación
        self.closeSession()


    def componentDevice(self):
        """
        Procesa y obtiene los componentes asociados a los dispositivos, incluyendo la extracción de la estructura
        de componentes, la identificación de componentes locales y la obtención de templates asociados a dichos
        componentes. Además, registra el tiempo de ejecución y guarda los resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 10.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Obtiene la estructura de componentes de los dispositivos exportados.
        4. Identifica los componentes locales asociados a los dispositivos.
        5. Obtiene los templates asociados a los componentes locales.
        6. Guarda los resultados en archivos JSON para su revisión.
        7. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 10
        self.last_execution_time = log_time("PASO 10", self.last_execution_time)
        
        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Obtener la estructura de componentes de los dispositivos ---
        # Recorre cada dispositivo para obtener su árbol de componentes (se limita al primer dispositivo como ejemplo)
        components = self.getComponentTree(self.devices_export)
        # Guarda la estructura de componentes en un archivo JSON
        saveToFile(components, '10.1 - get_component_tree.json')

        # --- Identificar componentes locales ---
        # Obtiene el listado de componentes locales asociados a los dispositivos
        components_local = self.getComponentLocal(components)
        # Guarda los componentes locales en un archivo JSON
        saveToFile(components_local, '10.2 - get_components_local.json')

        # --- Obtener templates asociados a los componentes locales ---
        # Recorre cada dispositivo para obtener los templates asociados a los componentes locales
        self.components_local_template = self.getComponentTemplate(components_local)
        # Guarda los templates asociados a los componentes locales en un archivo JSON
        saveToFile(self.components_local_template, '10.3 - components_local_template.json')

        # Cerrar la sesión de autenticación
        self.closeSession()


    def migrateComponentDevice(self):
        """
        Migra los componentes de los dispositivos, incluyendo la configuración de Data Sources, Thresholds y
        Graph Definitions asociados a los componentes locales. Además, registra el tiempo de ejecución y guarda
        los resultados en archivos JSON para su revisión.

        Pasos principales:
        1. Registra el tiempo de inicio del paso 10.
        2. Crea una sesión con las APIs de exportación e importación.
        3. Inicia el proceso de migración de Data Sources, Thresholds y Graph Definitions:
        - Obtiene los Data Sources asociados a los componentes locales.
        - Crea plantillas RRD locales para los componentes.
        - Agrega los Data Sources a los componentes locales.
        - Agrega y actualiza los Data Points.
        - Migra los Thresholds.
        - Migra las Graph Definitions.
        4. Guarda los resultados en archivos JSON para su revisión.
        5. Cierra la sesión de autenticación.
        """
        # Registrar el tiempo de inicio del paso 10
        self.last_execution_time = log_time("PASO 10", self.last_execution_time)

        # Crear una sesión con las APIs de exportación e importación
        self.createSession()

        # --- Migración de Data Sources, Thresholds y Graph Definitions ---
        # Obtiene los Data Sources asociados a los componentes locales
        components_data_sources_template_local = self.getDataSources(self.data_source_types, self.components_local_template)
        # Guarda los Data Sources obtenidos en un archivo JSON
        saveToFile(components_data_sources_template_local, '11.1 - components_data_sources_template_local.json')

        # --- Crear plantillas RRD locales para los componentes ---
        # Crea plantillas RRD locales para los componentes
        components_make_local_RRDTemplate = self.makeLocalRRDTemplate(components_data_sources_template_local)
        # Guarda las plantillas RRD locales en un archivo JSON
        saveToFile(components_make_local_RRDTemplate, '11.2 - components_make_local_RRDTemplate.json')

        # --- Agregar Data Sources a los componentes locales ---
        # Agrega los Data Sources a los componentes locales
        components_add_data_source_template_local = self.componentAddDataSource(components_data_sources_template_local)
        # Guarda el resultado de la adición de Data Sources en un archivo JSON
        saveToFile(components_add_data_source_template_local, '11.3 - components_add_data_source_template_local.json')

        # --- Agregar Data Points a los componentes locales ---
        # Agrega los Data Points a los Data Sources de los componentes locales
        components_add_data_point_template_local = self.componentAddDataPoint(components_add_data_source_template_local)
        # Guarda el resultado de la adición de Data Points en un archivo JSON
        saveToFile(components_add_data_point_template_local, '11.4 - components_add_data_point_template_local.json')

        # --- Actualizar Data Points en los componentes locales ---
        # Actualiza los Data Points en los Data Sources de los componentes locales
        components_set_data_point_template_local = self.componentSetDataPoint(components_add_data_point_template_local)
        # Guarda el resultado de la actualización de Data Points en un archivo JSON
        saveToFile(components_set_data_point_template_local, '11.5 - components_set_data_point_template_local.json')

        # --- Migración de Thresholds ---
        # Agrega los Thresholds a los Data Sources de los componentes locales
        components_add_thresholds_template_local = self.componentAddThresholds(components_set_data_point_template_local)
        # Guarda el resultado de la adición de Thresholds en un archivo JSON
        saveToFile(components_add_thresholds_template_local, '11.6 - components_add_thresholds_template_local.json')

        # --- Migración de Graph Definitions ---
        # Agrega las Graph Definitions a los Data Sources de los componentes locales
        components_add_graph_definition_template = self.componentAddGraphDefinition(components_add_thresholds_template_local)
        # Guarda el resultado de la adición de Graph Definitions en un archivo JSON
        saveToFile(components_add_graph_definition_template, '11.7 - components_add_graph_definition_template.json')

        # Cerrar la sesión de autenticación
        self.closeSession()


    def createSession(self):
        """
        Crea sesiones de autenticación con Zenoss para las APIs de exportación e importación.

        La función intenta iniciar sesión en Zenoss utilizando las APIs `api_export` y `api_import`.
        Si alguna de las sesiones no se crea correctamente, se muestra un mensaje de error y se
        finaliza la ejecución del programa con un código de salida 1.

        Retorna:
        - None: La función no retorna ningún valor, pero puede finalizar la ejecución del programa.
        """
        
        # Se crea la sesión con Zenoss para la API de exportación
        self.login_export = self.api_export.login()
        
        # Se crea la sesión con Zenoss para la API de importación
        self.login_import = self.api_import.login()
        
        # Verifica si alguna de las sesiones no se creó correctamente
        if self.login_export is None or self.login_import is None:
            # Muestra un mensaje de error indicando que no se pudo iniciar sesión
            print("No se inició la sesión con Zenoss")
            
            # Finaliza la ejecución del programa con un código de salida 1 (error)
            return sys.exit(1)
    

    def closeSession(self):
        """
        Cierra las sesiones activas con Zenoss para las APIs de exportación e importación.

        Esta función llama al método `logout()` de las APIs `api_export` y `api_import`
        para cerrar las sesiones de manera segura y liberar los recursos asociados.

        Retorna:
        - None: La función no retorna ningún valor.
        """

        # Cierra la sesión de la API de exportación
        self.api_export.logout()

        # Cierra la sesión de la API de importación
        self.api_import.logout()
        

    def find_missing_packs(self, export_zenpack: list) -> list:
        """
        Encuentra los ZenPacks faltantes en el sistema de destino comparando con una lista de ZenPacks de exportación.

        Parámetros:
        - export_zenpack (list): Lista de ZenPacks obtenidos desde el sistema de exportación.

        Retorna:
        - find_missing_packs (list): Lista de ZenPacks que están en `export_zenpack` pero no en el sistema de destino.
        """
        try:
            # Obtener la lista de ZenPacks instalados en el sistema de destino
            zenPacks = ZenPack().checkZenpack(self.api_export)

            # Filtrar la lista `export_zenpack` para incluir solo los elementos que comienzan con 'ZenPacks'
            export_zenpack = [item for item in export_zenpack if item.startswith('ZenPacks')]

            # Encontrar los ZenPacks faltantes comparando `export_zenpack` con `zenPacks`
            find_missing_packs = ZenPack().find_missing_packs(export_zenpack, zenPacks)

            # Retornar la lista de ZenPacks faltantes
            return find_missing_packs

        except Exception as error:
            # Capturar y mostrar cualquier excepción que ocurra durante el proceso
            print(f"Error in find_missing_packs: {error}")
    

    def modelerPlugins(self) -> list:
        """
        Compara y sincroniza los plugins de modelado (zCollectorPlugins) entre los sistemas de exportación e importación.

        Retorna:
        - bool: True si la configuración se sincronizó correctamente en el sistema de importación.
        - list: Una lista vacía si no hay diferencias entre las configuraciones de exportación e importación.
        """

        # UID base para acceder a las propiedades de los dispositivos
        uid = "/zport/dmd/Devices"

        # Obtener la propiedad zCollectorPlugins del sistema de exportación
        get_zen_property_export = Devices().getZenProperty(self.api_export, uid)

        # Obtener la propiedad zCollectorPlugins del sistema de importación
        get_zen_property_import = Devices().getZenProperty(self.api_import, uid)

        # Extraer los valores de la propiedad zCollectorPlugins de ambos sistemas
        value_zen_property_export = get_zen_property_export.get('data')
        value_zen_property_import = get_zen_property_import.get('data')

        # Comparar los valores de los plugins de modelado entre exportación e importación
        value_not = list(set(value_zen_property_export.get('value')) - set(value_zen_property_import.get('value')))

        # Si hay diferencias, sincronizar la configuración
        if value_not:
            # Combinar y ordenar los valores de ambos sistemas
            value_zen_property = sorted(set(value_zen_property_export.get('value')) | set(value_zen_property_import.get('value')))

            # Preparar los datos para actualizar la propiedad en el sistema de importación
            data = {
                "uid": uid,  # UID de la propiedad
                "zProperty": "zCollectorPlugins",  # Nombre de la propiedad
                "value": value_zen_property  # Nuevo valor de la propiedad
            }

            # Actualizar la propiedad en el sistema de importación
            set_zenp_roperty = Devices().setZenPropertyModel(self.api_import, data)

            # Retornar el resultado de la operación (True si fue exitosa)
            result = set_zenp_roperty.get('success')
            return [result] 
        else:
            # Retornar una lista vacía si no hay diferencias
            return value_not
        

    def modelerPluginsLocal(self) -> list:
        """
        Obtiene y establece las propiedades Zen (ZenProperty) localmente para los dispositivos de exportación.

        Esta función realiza dos operaciones principales:
        1. Obtiene las propiedades Zen de los dispositivos de exportación.
        2. Establece las propiedades Zen localmente para los dispositivos de exportación.

        Retorna:
        - list: Una lista que contiene los resultados de establecer las propiedades Zen localmente.
        """

        # Obtener las propiedades Zen de los dispositivos de exportación
        get_zen_property_export_local = self.getZenPropertyLocal(self.devices_export)

        # Establecer las propiedades Zen localmente utilizando los datos obtenidos
        set_zen_property_local = self.setZenPropertyLocal(get_zen_property_export_local)

        # Retornar los resultados de establecer las propiedades Zen localmente
        return set_zen_property_local


    def zenPropertiesGeneral(self) -> list:
        """
        Compara las propiedades Zen generales entre los sistemas de exportación e importación.

        Esta función realiza las siguientes operaciones:
        1. Procesa y agrupa las propiedades Zen por su 'id'.
        2. Compara las propiedades entre los sistemas de exportación e importación, omitiendo la clave 'description'.
        3. Retorna una lista de diferencias encontradas.

        Retorna:
        - list: Una lista de diccionarios que contienen las diferencias entre las propiedades Zen de exportación e importación.
        """

        def process_and_group(properties: list) -> dict:
            """
            Procesa y agrupa las propiedades Zen por su 'id'.

            Parámetros:
            - properties (list): Lista de propiedades Zen.

            Retorna:
            - dict: Un diccionario donde las claves son los 'id' de las propiedades y los valores son las propiedades procesadas.
            """

            processed = []
            for item in properties:
                # Convertir valores a enteros si el tipo es "int"
                if item.get('type') == "int":
                    item['value'] = int(item.get('value')) if item.get('value') is not None else item.get('value')
                    item['valueAsString'] = int(item.get('valueAsString')) if item.get('valueAsString') is not None else item.get('valueAsString')
                processed.append(item)
            # Agrupar propiedades por 'id'
            return {item['id']: item for item in processed}

        def compare_without_description(item1: dict, item2: dict) -> bool:
            """
            Compara dos diccionarios omitiendo la clave 'description'.

            Parámetros:
            - item1 (dict): Primer diccionario a comparar.
            - item2 (dict): Segundo diccionario a comparar.

            Retorna:
            - bool: True si los diccionarios son diferentes (sin considerar 'description'), False en caso contrario.
            """

            # Crear copias de los diccionarios sin la clave 'description'
            item1_copy = {key: value for key, value in item1.items() if key != 'description'}
            item2_copy = {key: value for key, value in item2.items() if key != 'description'}
            # Comparar los diccionarios
            return item1_copy != item2_copy

        # Obtener y procesar propiedades Zen de exportación e importación
        export_properties = Devices().getZenPropertiesGeneral(self.api_export).get('data', [])
        import_properties = Devices().getZenPropertiesGeneral(self.api_import).get('data', [])

        # Agrupar propiedades por 'id'
        export_group = process_and_group(export_properties)
        import_group = process_and_group(import_properties)

        # Encontrar diferencias entre las propiedades de exportación e importación
        differences = [
            {
                'id': id,
                'zen_property_export': zen_property_export,
                'zen_property_import': import_group.get(id),
            }
            for id, zen_property_export in export_group.items()
            if id in import_group and compare_without_description(zen_property_export, import_group.get(id))
        ]

        # Retornar la lista de diferencias
        return differences
    

    def updateZenProperty(self, configuration_properties_general: list) -> list:
        """
        Actualiza las propiedades Zen generales en el sistema de importación si existen diferencias.

        Parámetros:
        - configuration_properties_general (list): Lista de diccionarios que contienen las propiedades Zen
          de exportación e importación, así como las diferencias encontradas.

        Retorna:
        - list: La lista de diccionarios actualizada con los resultados de la operación de actualización.
        """

        # Iterar sobre cada propiedad en la lista de propiedades generales
        for configuration_properties in configuration_properties_general:
            # Obtener la propiedad de exportación
            configuration_export = configuration_properties.get('zen_property_export')

            # Si existe la propiedad de exportación, actualizarla en el sistema de importación
            if configuration_export:
                # Ejecutar el método de actualización y almacenar el resultado
                result = Devices().setZenPropertyGeneral(
                    self.api_import, 
                    "zDeviceTemplates", 
                    configuration_export.get('value')
                )

                # Eliminar la propiedad de importación del diccionario (ya no es necesaria)
                configuration_properties.pop('zen_property_import', None)

                # Agregar el resultado de la actualización al diccionario
                configuration_properties['updateZenProperty'] = result.get('success')

        # Retornar la lista de propiedades generales actualizada con los resultados
        return configuration_properties_general


    def propertiesRouterGeneral(self) -> dict:
        """
        Compara las propiedades del enrutador general entre los sistemas de exportación e importación.

        Esta función realiza las siguientes operaciones:
        1. Obtiene y procesa las propiedades del enrutador general de los sistemas de exportación e importación.
        2. Crea diccionarios indexados por 'id' para facilitar la comparación.
        3. Encuentra elementos faltantes en el sistema de importación.
        4. Encuentra elementos diferentes entre los sistemas, omitiendo la clave 'description'.
        5. Retorna un diccionario con los resultados de la comparación.

        Retorna:
        - dict: Un diccionario que contiene dos claves:
            - 'missing': Elementos presentes en exportación pero no en importación.
            - 'different': Elementos presentes en ambos sistemas pero con diferencias (sin considerar 'description').
        """

        # Obtener y procesar propiedades del enrutador general
        export_properties = Devices().getPropertiesRouterGeneral(self.api_export).get('data', [])
        import_properties = Devices().getPropertiesRouterGeneral(self.api_import).get('data', [])

        # Crear diccionarios indexados por 'id' para facilitar la comparación
        export_dict = {property_item.get('id'): property_item for property_item in export_properties}
        import_dict = {property_item.get('id'): property_item for property_item in import_properties}

        # Encontrar elementos faltantes en el sistema de importación
        missing_properties = {
            property_id: export_dict.get(property_id)
            for property_id in export_dict
            if property_id not in import_dict
        }

        # Encontrar elementos diferentes entre los sistemas, omitiendo 'description'
        different_properties = {
            property_id: {
                'export': export_dict.get(property_id),
                'import': import_dict.get(property_id)
            }
            for property_id in export_dict
            if property_id in import_dict and
            {key: value for key, value in export_dict.get(property_id).items() if key != 'description'} !=
            {key: value for key, value in import_dict.get(property_id).items() if key != 'description'}
        }

        # Crear el diccionario de resultados
        result = {'missing': missing_properties, 'different': different_properties}

        # Retornar los resultados
        return result


    def updatePropertiesRouter(self, propertiesRouterGeneral: dict) -> dict:
        """
        Actualiza las propiedades de un router basado en un diccionario de propiedades generales.

        Parámetros:
        - propertiesRouterGeneral (dict): Un diccionario que contiene las propiedades generales del router,
        incluyendo las diferencias que necesitan ser actualizadas.

        Retorna:
        - dict: Un diccionario que contiene los resultados de las actualizaciones realizadas,
        donde la clave es el identificador del nodo y el valor es el resultado de la operación de actualización.
        """
        # Obtener las diferencias del diccionario propertiesRouterGeneral
        differents = propertiesRouterGeneral.get('different', {})
        
        # Diccionario para almacenar los resultados de las actualizaciones
        results = {}
        
        # Iterar sobre cada diferencia encontrada
        for key, value in differents.items():
            # Obtener la información de exportación de la diferencia
            diferent_export = value.get('export')
            
            # Verificar si hay una exportación válida para actualizar
            if diferent_export:
                # Ejecutar el método de actualización y almacenar el resultado
                result = Devices().updatePropertiesRouterGeneral(
                    self.api_import,  # API de importación
                    diferent_export.get('id'),  # ID del nodo a actualizar
                    diferent_export.get('value')  # Nuevo valor a asignar
                )
                
                # Guardar el resultado en el diccionario bajo la clave del nodo
                results[key] = result
        
        # Retornar el diccionario con los resultados de las actualizaciones
        return results


    def addPropertiesRouter(self, propertiesRouterGeneral: dict) -> dict:
        """
        Agrega las propiedades del enrutador faltantes en el sistema de importación.

        Parámetros:
        - propertiesRouterGeneral (dict): Un diccionario que contiene las propiedades faltantes
          y diferentes entre los sistemas de exportación e importación.

        Retorna:
        - dict: Un diccionario que contiene los resultados de la operación de agregar propiedades.
        """

        # Obtener las propiedades faltantes del diccionario de propiedades generales
        missing_properties = propertiesRouterGeneral.get('missing', {})

        # Diccionario para almacenar los resultados de la operación
        results = {}

        # Iterar sobre cada propiedad faltante
        for property_id, export_property in missing_properties.items():
            if export_property:
                # Eliminar las claves innecesarias de la propiedad de exportación
                export_property.pop('valueAsString', None)
                export_property.pop('islocal', None)

                # Asegurar que la propiedad tenga las claves necesarias
                if 'description' not in export_property:
                    export_property['description'] = ""
                if 'label' not in export_property:
                    export_property['label'] = ""
                if 'value' not in export_property:
                    export_property['value'] = ""

                # Ejecutar el método para agregar la propiedad en el sistema de importación
                result = Devices().addPropertiesRouterGeneral(self.api_import, export_property)

                # Guardar el resultado en el diccionario de resultados
                results[property_id] = result

        # Retornar los resultados de la operación
        return results
    

    def dataModelerPlugins(self, device: dict) -> dict:
        """
        Configura los plugins de modelado (modeler plugins) para un dispositivo específico.

        Parámetros:
        - device (dict): Un diccionario que contiene información del dispositivo,
        incluyendo los plugins de modelado que se desean configurar.

        Retorna:
        - dict: El diccionario del dispositivo actualizado con el resultado de la operación
        de configuración del plugin de modelado.
        """
        # Obtener el plugin de modelado del dispositivo
        modelerPlugin = device.get('modelerPlugin')
        
        # Preparar los datos para configurar la propiedad Zenoss
        data = {
            "uid": device.get('uid'),  # Identificador único del dispositivo
            "zProperty": "zCollectorPlugins",  # Propiedad Zenoss a configurar
            "value": modelerPlugin.get('data').get('value')  # Valor del plugin de modelado
        }
        
        # Configurar la propiedad Zenoss utilizando el método setZenPropertyModel
        set_zenp_roperty = Devices().setZenPropertyModel(self.api_import, data)
        
        # Actualizar el diccionario del plugin de modelado con el resultado de la operación
        modelerPlugin['setModelerPlugin'] = set_zenp_roperty.get('success')
        
        # Retornar el diccionario del dispositivo actualizado
        return device


    def separateTemplates(self, templates_general_detail: list) -> dict:
        """
        Separa las plantillas en dos categorías: 'master' y 'local', basándose en su definición.

        Parámetros:
        - templates_general_detail (list): Una lista de diccionarios que contienen detalles de las plantillas,
        incluyendo su definición.

        Retorna:
        - dict: Un diccionario con dos listas: 'master' y 'local', que contienen las plantillas separadas.
        """
        # Expresión regular para detectar direcciones IP en la ruta "/devices/..."
        pattern = re.compile(r"/devices/.*\b(?:\d{1,3}\.){3}\d{1,3}\b")
        
        # Diccionario para almacenar las plantillas separadas
        templates_general_separated = {'master': [], 'local': []}
        
        # Iterar sobre cada plantilla en la lista de detalles
        for template in templates_general_detail:
            # Obtener el valor de 'definition' del template, o una cadena vacía si no existe
            definition = template.get('definition', "")
            
            # Verificar si 'definition' coincide con el patrón de la expresión regular
            matches_pattern = bool(pattern.search(definition))
            
            # Verificar si 'definition' contiene el texto "os/interfaces"
            contains_excluded_text = "os/interfaces" in definition
            
            # Asignar 'local' solo si se encuentra el patrón y no contiene "os/interfaces", de lo contrario, asignar 'master'
            key = "local" if matches_pattern and not contains_excluded_text else "master"
            
            # Agregar la plantilla a la lista correspondiente en el diccionario
            templates_general_separated[key].append(template)
        
        # Retornar el diccionario con las plantillas separadas
        return templates_general_separated


    def filterTemplatesExport(self, export: list, templates: list) -> dict:
        """
        Filtra las plantillas en dos categorías: 'templates' y 'components', basándose en los UID de exportación
        y ciertas condiciones relacionadas con el icono y el UID de las plantillas.

        Parámetros:
        - export (list): Una lista de diccionarios que contiene los UID de exportación.
        - templates (list): Una lista de diccionarios que contiene las plantillas a filtrar.

        Retorna:
        - dict: Un diccionario con dos listas: 'templates' y 'components', que contienen las plantillas filtradas.
        """
        # Extraer los UID de la lista export
        export_uids = [item.get('uid') for item in export]
        
        # Inicializar los resultados en dos listas
        result = {'templates': [], 'components': []}
        
        # Clasificar los templates según su iconCls y UID
        for template in templates:
            # Verificar si el UID del template inicia con alguno de los UID de export
            if any(template.get('uid').startswith(uid) for uid in export_uids):
                # Verifica si la clave "iconCls" está en el template y si su valor contiene "tree-template-icon-component"
                has_icon = "iconCls" in template and "tree-template-icon-component" in template.get('iconCls')
                
                # Lista de cadenas que queremos comprobar en la clave "uid"
                uid_checks = ["/os/filesystems/", "/hw/harddisks/"]
                
                # Verifica si alguna de las cadenas en uid_checks está contenida en el valor de la clave "uid" del template
                has_uid = any(check in template.get('uid', "") for check in uid_checks)
                
                # Si se cumple alguna de las condiciones: tiene el icono o el UID contiene alguna de las cadenas
                if has_icon or has_uid:
                    result.get('components').append(template)
                else:
                    result.get('templates').append(template)
        
        # Retornar el diccionario con las plantillas filtradas
        return result


    # ██████╗ ███████╗██╗   ██╗██╗ █████╗ ███████╗ ██████╗
    # ██╔══██╗██╔════╝██║   ██║██║██╔══██╗██╔════╝██╔════╝
    # ██║  ██║█████╗  ╚██╗ ██╔╝██║██║  ╚═╝█████╗  ╚█████╗ 
    # ██║  ██║██╔══╝   ╚████╔╝ ██║██║  ██╗██╔══╝   ╚═══██╗
    # ██████╔╝███████╗  ╚██╔╝  ██║╚█████╔╝███████╗██████╔╝
    # ╚═════╝ ╚══════╝   ╚═╝   ╚═╝ ╚════╝ ╚══════╝╚═════╝ 

    def getZenPropertyLocal(self, devices: list) -> list:
        """
        Obtiene las propiedades Zen (ZenProperty) de una lista de dispositivos de manera paralela.

        Parámetros:
        - devices (list): Lista de dispositivos para los cuales se obtendrán las propiedades Zen.

        Retorna:
        - list: Una lista de resultados que contiene las propiedades Zen de los dispositivos.
          Los resultados nulos (None) son filtrados.
        """
        # Usar ThreadPoolExecutor para procesar los dispositivos en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getZenProperty para cada dispositivo en paralelo
            results = list(tqdm(
                executor.map(lambda device: Devices().getZenProperty(self.api_export, device), devices), 
                desc="Procesando setZenPropertyLocal".ljust(50), # Descripción de la barra de progreso
                total=len(devices) # Total de elementos a procesar
            ))

        # Filtrar resultados nulos y retornar la lista de propiedades Zen
        getZenPropertyLocal = [result for result in results if result is not None]
        return getZenPropertyLocal


    def setZenPropertyLocal(self, devices: list) -> list:
        """
        Establece las propiedades Zen (ZenProperty) para una lista de dispositivos de manera paralela.

        Parámetros:
        - devices (list): Lista de dispositivos para los cuales se establecerán las propiedades Zen.

        Retorna:
        - list: Una lista de resultados que contiene el estado de la operación para cada dispositivo.
          Los resultados nulos (None) son filtrados.
        """

        # Usar ThreadPoolExecutor para procesar los dispositivos en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar dataModelerPlugins para cada dispositivo en paralelo
            results = list(tqdm(
                executor.map(lambda device: self.dataModelerPlugins(device), devices), 
                desc="Procesando setZenPropertyLocal".ljust(50), # Descripción de la barra de progreso
                total=len(devices) # Total de elementos a procesar
            ))

        # Filtrar resultados nulos y retornar la lista de estados de la operación
        setZenPropertyLocal = [result for result in results if result is not None]
        return setZenPropertyLocal
    

    def detailDevices(self, devices: list) -> list:
        """
        Obtiene detalles de una lista de dispositivos en paralelo utilizando ThreadPoolExecutor.

        Parámetros:
        - devices (list): Lista de dispositivos para los cuales se obtendrán los detalles.

        Retorna:
        - list: Una lista plana que contiene los detalles de todos los dispositivos procesados.
        """

        # Usar ThreadPoolExecutor para procesar los dispositivos en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar detailDevices para cada dispositivo en paralelo
            results = list(tqdm(
                executor.map(lambda device: Devices().detailDevices(self.api_export, [device]), devices),
                desc="Procesando detailDevices".ljust(50), # Descripción de la barra de progreso
                total=len(devices) # Total de elementos a procesar
            ))

        # Aplanar la lista de resultados (si es necesario) y retornarla
        return [item for sublist in results for item in sublist]
    

    def parseDeviceData(self, devices: list) -> list:
        """
        Procesa los datos de una lista de dispositivos en paralelo utilizando ThreadPoolExecutor.

        Parámetros:
        - devices (list): Lista de dispositivos que se procesarán.

        Retorna:
        - list: Una lista plana que contiene los resultados del procesamiento de todos los dispositivos.
        """
        # Usar ThreadPoolExecutor para procesar los dispositivos en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar parseDeviceData para cada dispositivo en paralelo
            results = list(tqdm(
                executor.map(lambda device: Devices().parseDeviceData([device]), devices),
                desc="Procesando parseDeviceData".ljust(50), # Descripción de la barra de progreso
                total=len(devices) # Total de elementos a procesar
            ))

        # Aplanar la lista de resultados (si es necesario) y retornarla
        return [item for sublist in results for item in sublist]


    def addDevice(self, devices: list) -> list:
        """
        Agrega dispositivos en paralelo utilizando ThreadPoolExecutor.

        Parámetros:
        - devices (list): Lista de dispositivos que se agregarán.

        Retorna:
        - list: Una lista que contiene los resultados de la operación de agregado para cada dispositivo.
        """
        # Usar ThreadPoolExecutor para agregar dispositivos en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addDevice para cada dispositivo en paralelo
            results = list(tqdm(
                executor.map(lambda device: Devices().addDevice(self.api_import, device), devices),
                desc="Procesando addDevice".ljust(50), # Descripción de la barra de progreso
                total=len(devices) # Total de elementos a procesar
            ))

        # Retornar la lista de resultados
        return results


    def addTemplateGeneralNode(self, template_class: list) -> list:
        """
        Agrega nodos de plantillas generales en paralelo utilizando ThreadPoolExecutor.

        Parámetros:
        - template_class (list): Lista de plantillas que se agregarán como nodos generales.

        Retorna:
        - list: Una lista filtrada de resultados de la operación de agregado, excluyendo valores `None`.
        """
        # Usar ThreadPoolExecutor para agregar nodos de plantillas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addTemplateGeneralNode para cada plantilla en paralelo
            results = list(tqdm(
                executor.map(lambda template: Devices().addTemplateGeneralNode(self.api_import, template), template_class),
                desc="Procesando addTemplateGeneralNode".ljust(50), # Descripción de la barra de progreso
                total=len(template_class) # Total de elementos a procesar
            ))

        # Filtrar los resultados para excluir los valores None
        filtered_results = [result for result in results if result is not None]

        # Retornar la lista de resultados filtrados
        return filtered_results


    def getTemplatesDeviceMonitoring(self, templates: list) -> list:
        """
        Obtiene las plantillas de monitoreo de dispositivos de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas para las cuales se obtendrá el monitoreo de dispositivos.

        Retorna:
        - list: Una lista de resultados de monitoreo de dispositivos, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar getTemplatesDeviceMonitoring para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getTemplatesDeviceMonitoring(self.api_export, template), templates),
                desc="Procesando getTemplatesDeviceMonitoring".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        templates_device_monitoring = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return templates_device_monitoring
    

    def setBoundTemplates(self, templates: list) -> list:
        """
        Asigna plantillas vinculadas (bound templates) a dispositivos de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas que se asignarán a los dispositivos.

        Retorna:
        - list: Una lista de resultados de la asignación de plantillas, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar setBoundTemplates para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().setBoundTemplates(self.api_import, template), templates),
                desc="Procesando setBoundTemplates".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        set_bound_templates = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return set_bound_templates


    # # -------------------
    # # getInfoTemplate
    # # -------------------
    # def getInfoTemplate(self, templates):
    #     with ThreadPoolExecutor(max_workers=workers_max) as executor:
    #         # Ejecutar parseDeviceData para cada dispositivo de manera paralela
    #         results = list(tqdm(executor.map(lambda template: Devices().getInfoTemplate(self.api_import, template), templates), desc="Procesando getInfoTemplate".ljust(50), total=len(templates)))
    #     # Combinar el resultado con la estructura requerida
    #     get_info_template = [result for result in results if result is not None]
    #     # Aplanar el resultado si es necesario
    #     return get_info_template
    

    # ████████╗███████╗███╗   ███╗██████╗ ██╗      █████╗ ████████╗███████╗
    # ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝
    #    ██║   █████╗  ██╔████╔██║██████╔╝██║     ███████║   ██║   █████╗  
    #    ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  
    #    ██║   ███████╗██║ ╚═╝ ██║██║     ███████╗██║  ██║   ██║   ███████╗
    #    ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

    # █▀▀ █▀▀ █▄ █ █▀▀ █▀█ ▄▀█ █  
    # █▄█ ██▄ █ ▀█ ██▄ █▀▄ █▀█ █▄▄

    def getTemplatesGeneralDetail(self, templates: list) -> dict:
        """
        Obtiene detalles generales de las plantillas de manera paralela utilizando un ThreadPoolExecutor.
        Además, filtra y separa las plantillas en categorías "master" y "local".

        Parámetros:
        - templates (list): Una lista de plantillas para las cuales se obtendrán los detalles generales.

        Retorna:
        - dict: Un diccionario con dos listas: 'master' y 'local', que contienen las plantillas separadas.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getTemplatesGeneralDetail para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getTemplatesGeneralDetail(self.api_export, template), templates),
                desc="Procesando getTemplatesGeneralDetail".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_info_template = [result for result in results if result is not None]
        
        # Aplanar la lista de resultados, ya que algunos pueden ser listas de plantillas
        templates_general_detail = [x for item in get_info_template for x in (item if isinstance(item, list) else [item])]
        
        # Eliminar diccionarios con UID duplicada
        templates_general_detail = list({item["uid"]: item for item in templates_general_detail}.values())
        
        # Separar las plantillas en categorías "master" y "local"
        templates_general_separated = self.separateTemplates(templates_general_detail)
        
        # Retornar el diccionario con las plantillas separadas
        return templates_general_separated


    def addTemplateGeneral(self, template_class: dict) -> dict:
        """
        Agrega plantillas generales de manera paralela utilizando un ThreadPoolExecutor.
        Filtra los resultados y los clasifica en dos categorías: 'process' (éxito) y 'missing' (fallo).

        Parámetros:
        - template_class (dict): Un diccionario que contiene las plantillas que se agregarán.

        Retorna:
        - dict: Un diccionario con dos listas:
            - 'process': Plantillas que se agregaron correctamente.
            - 'missing': Plantillas que no se pudieron agregar.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addTemplateGeneral para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addTemplateGeneral(self.api_import, template), template_class),
                desc="Procesando addTemplateGeneral".ljust(50), # Descripción de la barra de progreso
                total=len(template_class) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        filtered_results = list(filter(None, results))
        
        # Clasificar los resultados en dos categorías: 'process' (éxito) y 'missing' (fallo)
        return {
            'process': [item for item in filtered_results if item.get("templateGeneral_add") == True],  # Plantillas agregadas correctamente
            'missing': [item for item in filtered_results if item.get("templateGeneral_add") == False]  # Plantillas no agregadas
        }


    def setInfoTemplate(self, templates: list) -> list:
        """
        Configura la información de las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas para las cuales se configurará la información.

        Retorna:
        - list: Una lista de resultados de la configuración, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar setInfoTemplate para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().setInfoTemplate(self.api_import, template), templates),
                desc="Procesando setInfoTemplate".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        set_info_template = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return set_info_template
    

    def getDataSources(self, data_source_types: list, templates: list) -> list:
        """
        Obtiene las fuentes de datos (datasources), umbrales (thresholds) y gráficos (graphs) asociados a las plantillas
        de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - data_source_types (list): Una lista de tipos de fuentes de datos que se desean obtener.
        - templates (list): Una lista de plantillas para las cuales se obtendrán las fuentes de datos.

        Retorna:
        - list: Una lista de diccionarios que contienen las fuentes de datos, umbrales y gráficos asociados a cada plantilla.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getDataSources para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getDataSources(self.api_export, data_source_types, template), templates),
                desc="Procesando getDataSources".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Combinar los resultados con la estructura requerida
        get_data_sources = [
            {
                "uid": template.get('uid'),  # UID de la plantilla
                **({"uid_component": template['uid_component']} if "uid_component" in template else {}),  # UID del componente (si existe)
                **({"uid_template": template['uid_template']} if "uid_template" in template else {}),  # UID de la plantilla (si existe)
                "datasources": result.get('datasources', []),  # Fuentes de datos obtenidas
                "thresholds": result.get('thresholds', []),  # Umbrales obtenidos
                "graphs": result.get('graphs', [])  # Gráficos obtenidos
            } 
            for template, result in zip(templates, results) if result is not None  # Filtrar resultados nulos
        ]
        
        # Retornar la lista de resultados combinados
        return get_data_sources


    def addDataSource(self, templates: list) -> list:
        """
        Agrega fuentes de datos (datasources) a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán las fuentes de datos.

        Retorna:
        - list: Una lista de resultados de la operación de agregado, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addDataSource para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addDataSource(self.api_import, template), templates),
                desc="Procesando addDataSource".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_data_source = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_data_source


    def addDataPoint(self, templates: list) -> list:
        """
        Agrega puntos de datos (datapoints) a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán los puntos de datos.

        Retorna:
        - list: Una lista de resultados de la operación de agregado, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addDataPoint para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addDataPoint(self.api_import, template), templates),
                desc="Procesando addDataPoint".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_data_point = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_data_point
    

    def setDataPoint(self, templates: list) -> list:
        """
        Configura los puntos de datos (datapoints) en las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas en las cuales se configurarán los puntos de datos.

        Retorna:
        - list: Una lista de resultados de la operación de configuración, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar setDataPoint para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().setDataPoint(self.api_import, template), templates),
                desc="Procesando setDataPoint".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        set_data_point = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return set_data_point


    def addThresholds(self, templates: list) -> list:
        """
        Agrega umbrales (thresholds) a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán los umbrales.

        Retorna:
        - list: Una lista de resultados de la operación de agregado, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addThreshold para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addThreshold(self.api_import, template), templates),
                desc="Procesando addThresholds".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_thresholds = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_thresholds
    

    def addGraphDefinition(self, templates: list) -> list:
        """
        Agrega definiciones de gráficos (graph definitions) a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán las definiciones de gráficos.

        Retorna:
        - list: Una lista de resultados de la operación de agregado, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addGraphDefinition para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addGraphDefinition(self.api_import, template), templates),
                desc="Procesando addGraphDefinition".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_graph_definition = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_graph_definition


    # █   █▀█ █▀▀ ▄▀█ █  
    # █▄▄ █▄█ █▄▄ █▀█ █▄▄


    def addTemplateLocal(self, template_class: list) -> list:
        """
        Agrega plantillas locales de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - template_class (list): Una lista de plantillas que se agregarán como locales.

        Retorna:
        - list: Una lista de resultados de la operación de agregado, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addTemplateLocal para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addTemplateLocal(self.api_import, template), template_class),
                desc="Procesando addTemplateLocal".ljust(50), # Descripción de la barra de progreso
                total=len(template_class) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        filtered_results = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return filtered_results


    def getTemplatesDeviceLocal(self, templates: list) -> dict:
        """
        Obtiene las plantillas locales y generales de los dispositivos de manera paralela utilizando un ThreadPoolExecutor.
        Clasifica las plantillas en dos categorías: 'locals' (locales) y 'generals' (generales).

        Parámetros:
        - templates (list): Una lista de plantillas para las cuales se obtendrá la información.

        Retorna:
        - dict: Un diccionario con dos listas:
            - 'locals': Plantillas locales.
            - 'generals': Plantillas generales.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getTemplatesDeviceLocal para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getTemplatesDeviceLocal(self.api_export, template), templates),
                desc="Procesando getTemplatesDeviceLocal".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_info_template = [result for result in results if result is not None]
        
        # Crear un diccionario para clasificar las plantillas en 'locals' y 'generals'
        result_dict = {'locals': [], 'generals': []}
        for result in get_info_template:
            # Determinar si la plantilla es local o general
            key = 'locals' if result.get('isTemplateLocal') else 'generals'
            # Agregar la plantilla a la lista correspondiente
            result_dict[key].append(result)
        
        # Retornar el diccionario con las plantillas clasificadas
        return result_dict
    

    #  █████╗  █████╗ ███╗   ███╗██████╗  █████╗ ███╗  ██╗███████╗███╗  ██╗████████╗███████╗ ██████╗
    # ██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗████╗ ██║██╔════╝████╗ ██║╚══██╔══╝██╔════╝██╔════╝
    # ██║  ╚═╝██║  ██║██╔████╔██║██████╔╝██║  ██║██╔██╗██║█████╗  ██╔██╗██║   ██║   █████╗  ╚█████╗ 
    # ██║  ██╗██║  ██║██║╚██╔╝██║██╔═══╝ ██║  ██║██║╚████║██╔══╝  ██║╚████║   ██║   ██╔══╝   ╚═══██╗
    # ╚█████╔╝╚█████╔╝██║ ╚═╝ ██║██║     ╚█████╔╝██║ ╚███║███████╗██║ ╚███║   ██║   ███████╗██████╔╝
    #  ╚════╝  ╚════╝ ╚═╝     ╚═╝╚═╝      ╚════╝ ╚═╝  ╚══╝╚══════╝╚═╝  ╚══╝   ╚═╝   ╚══════╝╚═════╝ 

    # █▀█ █▀█ █ █▀▀ █▀▀ █▄ █
    # █▄█ █▀▄ █ █▄█ ██▄ █ ▀█

    def getComponentTree(self, templates: list) -> list:
        """
        Obtiene el árbol de componentes (component tree) asociado a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas para las cuales se obtendrá el árbol de componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getComponentTree para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getComponentTree(self.api_export, template), templates),
                desc="Procesando getComponentTree".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_component_tree = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return get_component_tree


    def getComponentLocal(self, templates: dict) -> list:
        """
        Obtiene los componentes locales asociados a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (dict): Un diccionario de plantillas para las cuales se obtendrán los componentes locales.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getComponentLocal para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getComponentLocal(self.api_export, template), templates),
                desc="Procesando getComponentLocal".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_component_local = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return get_component_local


    def getComponentTemplate(self, templates: dict) -> list:
        """
        Obtiene las plantillas de componentes asociadas a las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (dict): Un diccionario de plantillas para las cuales se obtendrán las plantillas de componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar getComponentTemplate para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().getComponentTemplate(self.api_export, template), templates),
                desc="Procesando getComponentTemplate".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_component_local = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return get_component_local


    # █▀▄ █▀▀ █▀ ▀█▀ █ █▄ █ █▀█
    # █▄▀ ██▄ ▄█  █  █ █ ▀█ █▄█


    def makeLocalRRDTemplate(self, templates: dict) -> list:
        """
        Crea plantillas RRD locales para las plantillas proporcionadas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (dict): Un diccionario de plantillas para las cuales se crearán las plantillas RRD locales.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar makeLocalRRDTemplate para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().makeLocalRRDTemplate(self.api_import, template), templates),
                desc="Procesando makeLocalRRDTemplate".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_component_local = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return get_component_local


    def componentAddDataSource(self, templates: dict) -> list:
        """
        Agrega fuentes de datos (datasources) a los componentes de las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (dict): Un diccionario de plantillas para las cuales se agregarán las fuentes de datos a los componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_max) as executor:
            # Ejecutar componentAddDataSource para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().componentAddDataSource(self.api_import, template), templates),
                desc="Procesando componentAddDataSource".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        get_component_local = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return get_component_local


    def componentAddDataPoint(self, templates: list) -> list:
        """
        Agrega puntos de datos (datapoints) a los componentes de las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán los puntos de datos a los componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar componentAddDataPoint para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().componentAddDataPoint(self.api_import, template), templates),
                desc="Procesando componentAddDataPoint".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_data_point = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_data_point


    def componentSetDataPoint(self, templates: list) -> list:
        """
        Configura los puntos de datos (datapoints) en los componentes de las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas en las cuales se configurarán los puntos de datos de los componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar setDataPointLocal para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().setDataPointLocal(self.api_import, template), templates),
                desc="Procesando componentSetDataPoint".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        set_data_point = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return set_data_point


    def componentAddThresholds(self, templates: list) -> list:
        """
        Agrega umbrales (thresholds) a los componentes de las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán los umbrales a los componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addThresholdLocal para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addThresholdLocal(self.api_import, template), templates),
                desc="Procesando componentAddThresholds".ljust(50), # Descripción de la barra de progreso
                total=len(templates) # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_thresholds = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_thresholds
    

    def componentAddGraphDefinition(self, templates: list) -> list:
        """
        Agrega definiciones de gráficos (graph definitions) a los componentes de las plantillas de manera paralela utilizando un ThreadPoolExecutor.

        Parámetros:
        - templates (list): Una lista de plantillas a las cuales se agregarán las definiciones de gráficos a los componentes.

        Retorna:
        - list: Una lista de resultados de la operación, filtrada para excluir valores nulos.
        """
        # Crear un ThreadPoolExecutor para ejecutar tareas en paralelo
        with ThreadPoolExecutor(max_workers=workers_min) as executor:
            # Ejecutar addGraphDefinitionLocal para cada plantilla de manera paralela
            # Usar tqdm para mostrar una barra de progreso
            results = list(tqdm(
                executor.map(lambda template: Devices().addGraphDefinitionLocal(self.api_import, template), templates),
                desc="Procesando componentAddGraphDefinition".ljust(50),  # Descripción de la barra de progreso
                total=len(templates)  # Total de elementos a procesar
            ))
        
        # Filtrar los resultados para excluir valores nulos
        add_graph_definition = [result for result in results if result is not None]
        
        # Retornar la lista de resultados filtrados
        return add_graph_definition
    

# ----------------------------------------#
# --- ███╗   ███╗ █████╗ ██╗███╗  ██╗ --- #
# --- ████╗ ████║██╔══██╗██║████╗ ██║ --- #
# --- ██╔████╔██║███████║██║██╔██╗██║ --- #
# --- ██║╚██╔╝██║██╔══██║██║██║╚████║ --- #
# --- ██║ ╚═╝ ██║██║  ██║██║██║ ╚███║ --- #
# --- ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚══╝ --- #
# ----------------------------------------#

def getConfig():
    """
    Lee y carga la configuración desde un archivo JSON llamado 'instance.json' ubicado en el directorio actual.

    Retorna:
    - data (dict): Un diccionario con la configuración cargada desde el archivo JSON.
    """

    # Obtener la ruta completa del archivo '/zenoss/instance.json' en el directorio actual
    config_path = os.getcwd() + '/zenoss/instance.json'

    # Abrir el archivo JSON en modo lectura
    with open(config_path) as file:
        # Cargar los datos del archivo JSON en un diccionario
        data = json.load(file)

    # Retornar el diccionario con la configuración cargada
    return data


def log_time(part_name: str, last_time=None):
    """
    Registra el tiempo transcurrido entre la última marca de tiempo y la actual.

    Parámetros:
    - part_name (str): Nombre de la parte o sección que se está registrando.
    - last_time (datetime, opcional): La última marca de tiempo registrada. Si no se proporciona, se asume que es la primera vez.

    Retorna:
    - current_time (datetime): La marca de tiempo actual, que puede usarse como `last_time` en la siguiente llamada.
    """

    # Obtiene la fecha y hora actual
    current_time = datetime.datetime.now()

    # Formatea la fecha y hora actual en el formato día/mes/año hora:minuto:segundo
    date_time_str = current_time.strftime('%d/%m/%Y %H:%M:%S')

    # Calcula el tiempo transcurrido si se proporcionó una marca de tiempo anterior
    if last_time:
        elapsed_time = current_time - last_time
        minutes_elapsed = elapsed_time.total_seconds() / 60
    else:
        # Si no hay una marca de tiempo anterior, el tiempo transcurrido es 0
        minutes_elapsed = 0

    # Imprime el log en el formato especificado
    print(f"{part_name} --- {date_time_str} --- Tiempo transcurrido: {minutes_elapsed:.2f} --------------------")

    # Retorna la marca de tiempo actual para su uso en la siguiente llamada
    return current_time


def saveToFile(dictionary: str, filename: str):
    """
    Guarda un diccionario en un archivo JSON dentro de una carpeta llamada 'output'.

    Parámetros:
    - dictionary (dict): El diccionario que se desea guardar en formato JSON.
    - filename (str): El nombre del archivo donde se guardará el diccionario.

    Retorna:
    - None: La función no retorna ningún valor, pero imprime mensajes en la consola.
    """

    # Obtén el directorio del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Ruta completa de la carpeta 'output' dentro del directorio del script
    output_dir = os.path.join(script_dir, "output")

    # Crea la carpeta 'output' si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ruta completa del archivo, incluyendo la carpeta 'output' y el nombre del archivo
    file_path = os.path.join(output_dir, filename)

    try:
        # Abre el archivo en modo escritura y guarda el diccionario en formato JSON
        with open(file_path, "w") as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)
        
        # Mensaje de éxito indicando la ruta donde se guardó el archivo
        print(f"El archivo se guardó en {file_path}")

    except Exception as e:
        # Captura cualquier excepción que ocurra durante el proceso de guardado
        print(f"Ocurrió un error al guardar el archivo JSON: {e}")

# -------------------
# Inicio del proceso.
# -------------------
if __name__ == '__main__':
    MigrateDevice().migrate()