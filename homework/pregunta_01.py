"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import re

def pregunta_01():
    # Leer el archivo
    with open('files/input/clusters_report.txt', 'r') as file:
        lines = file.readlines()

    # Procesar el contenido del archivo
    content = ''.join(lines)
    content = re.split(r'\-{5,}', content)[1].strip()
    rows = content.split('\n')
    
    # Preparar los datos para el DataFrame
    data = []
    current_row = []
    for row in rows:
        if re.match(r'^\s*\d', row):
            if current_row:
                data.append(current_row)
            current_row = re.split(r'\s{2,}', row.strip())
        else:
            current_row[-1] += ' ' + row.strip()
    data.append(current_row)
    
    # Ajustar las filas para que todas tengan 4 columnas
    cleaned_data = []
    for row in data:
        if len(row) == 4:
            cleaned_data.append(row)
        else:
            cluster, cantidad, porcentaje, *keywords = row
            keywords = ' '.join(keywords)
            cleaned_data.append([cluster, cantidad, porcentaje, keywords])
    
    # Crear el DataFrame
    columns = ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave']
    df = pd.DataFrame(cleaned_data, columns=columns)
    
    # Limpiar el DataFrame
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace('%', '').str.replace(',', '.').astype(float)
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace('\s+', ' ', regex=True).str.replace(' ,', ',', regex=False).str.replace('\s*,\s*', ', ', regex=True)
    
    # Convertir las palabras clave a una cadena separada por comas y quitar el punto final
    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(lambda x: ', '.join([item.strip() for item in x.split(',')]).rstrip('.'))

    return df

# Ejecutar la función para crear el DataFrame
df = pregunta_01()
print(df)



"""
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
