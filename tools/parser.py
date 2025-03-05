#!/usr/bin/python
# -*- coding: utf-8 -*-

""" ---------------------------------------------------------------------------------------------------

Nombre: Gerardo Treviño Montelongo
Clase: migrate.py
Fecha: 26/11/2024
Correo: gerardo.trevino@triara.com
Version 1.00
Sistema: Linux

--------------------------------------------------------------------------------------------------- """

import re
import json
import base64
from bs4 import BeautifulSoup

class Html:

    # -------------------
    # html_to_json
    # -------------------
    def html_to_json(self, html, tbody_id):
        soup = BeautifulSoup(html, 'lxml')
        tbody = soup.find('tbody', id=tbody_id)
        if not tbody:
            return f'No se encontró el <tbody> con el id "{tbody_id}".'
        # Extraer encabezados y filas de datos
        headers = [th.get_text(strip=True) for th in tbody.find('tr').find_all('th')]
        data_rows = tbody.find_all('tr')[1:]  # Omitir la fila de encabezados
        # Convertir filas en un diccionario
        zenpacks = [
            {headers[i]: td.get_text(strip=True) for i, td in enumerate(tr.find_all('td')) if headers[i]}
            for tr in data_rows
        ]
        # Retorna el diccionario de ZenPacks
        return zenpacks

    # -------------------
    # html_to_json_2
    # -------------------
    def html_to_json_2(self, html, tbody_id):
        # Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        # Buscar el tbody cuyo id comience con "Stateattime"
        tbody = soup.find('tbody', id=re.compile(r'^Stateattime'))
        if not tbody:
            return f'No se encontró el <tbody> con el id "{tbody_id}".'
        rows = tbody.find_all('tr')
        zenpacks = {}
        # Recorremos todas las filas para procesar los valores
        for row in rows:
            header_cell = row.find('td', class_='tableheader')
            value_cell = row.find('td', class_='tablevalues')
            if not header_cell or not value_cell:
                continue  # Ignorar filas sin ambos celdas
            header = header_cell.get_text(strip=True)
            # Si es el campo de autenticación
            if 'Authentication' in header:
                radio_buttons = value_cell.find_all('input', type='radio')
                for radio in radio_buttons:
                    radio_label = radio.find_next('label')
                    if radio_label:
                        auth_type = radio_label.get_text(strip=True)
                        if radio.get('checked'):
                            # Asignar el valor correcto según el radio button seleccionado
                            if auth_type == "Cookie-based Authentication":
                                zenpacks['AuthenticationYou will have to log off for this setting to take effect.'] = 'cookie'
                            elif auth_type == "Session-based Authentication (More Secure)":
                                zenpacks['AuthenticationYou will have to log off for this setting to take effect.'] = 'session'
                continue
            # Procesar checkbox
            checkbox = value_cell.find('input', type='checkbox')
            if checkbox:
                # Convertir el valor booleano a cadena en minúsculas
                zenpacks[header] = 'true' if checkbox.get('checked') else 'false'
                continue
            # Procesar inputs de texto
            input_field = value_cell.find('input', type='text')
            if input_field:
                zenpacks[header] = input_field.get('value', '').strip()
                continue
            # Procesar textarea
            textarea = value_cell.find('textarea')
            if textarea:
                zenpacks[header] = textarea.get_text(strip=True)
                continue
            # Si no hay checkbox, input o textarea, guardar el texto directamente
            zenpacks[header] = value_cell.get_text(strip=True)
        return zenpacks
    
    # -----------------------------------
    # extractBase64Html
    # -----------------------------------
    def extractBase64Html(self, content):
        # Parse the HTML
        soup = BeautifulSoup(content, 'html.parser')
        # Find the last div element with the class "streaming-line odd"
        div = soup.find_all('div', class_='streaming-line odd')
        if div:
            # Extract the text content of the last div
            encoded_text = div[-1].get_text(strip=True)
            # Try to decode the base64 string
            try:
                # Dividir el texto por comas
                pairs = encoded_text.split(", ")
                # Crear un diccionario separando por el signo igual y decodificando los valores
                result = {}
                for pair in pairs:
                    key_value = pair.split("=", 1)
                    # Verifica que contenga dos elementos
                    if len(key_value) == 2:
                        key, value = key_value
                        # Decodificar el valor después del igual, si tiene
                        decoded_value = base64.b64decode(value).decode('utf-8') if value else value
                        result[key] = decoded_value
                return result
            except Exception as e:
                # Return None if decoding or conversion fails
                print(f"Error in extractBase64Html: \n{encoded_text} \n{e}")
                return None
        # If no div is found, return None
        return None

    # -----------------------------------
    # decodeBase64Dict
    # -----------------------------------
    def decodeBase64Dict(self, base64_str):
        # Decodificar el string base64
        decoded_data = base64.b64decode(base64_str).decode('utf-8')
        # Convertir el string JSON decodificado a un diccionario
        data_dict = self.parse_to_dict(decoded_data.replace('\n', ''))
        return data_dict
    
    # -----------------------------------
    # parse_to_dict
    # -----------------------------------
    def parse_to_dict(self, input_string):
        # Crear un diccionario vacío para almacenar los pares clave-valor
        result = {}
        # Dividir la cadena por ', ' para obtener pares clave-valor
        pairs = input_string.split(", ")
        for pair in pairs:
            # Ignorar entradas vacías
            if "=" in pair:
                key, value = pair.split("=", 1)
                # Agregar el par clave-valor al diccionario
                result[key] = value
        return result