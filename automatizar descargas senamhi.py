import requests
from bs4 import BeautifulSoup
import csv

codigo_estacion = "100109"
# tipo de estación puede ser AUTOMATICA (para las automáticas) o REAL (para las convencionales)
tipo_estacion = "REAL"
ruta_salida = "C:/Users/hp/Downloads/"

first_row_auto = ["date", "hour", "temp", "rain", "humidity", "wind_Dir", "wind_speed"]
first_row_real = ["date", "temp_max", "temp_min", "humidity", "rain"]
first_row = []

if tipo_estacion == "AUTOMATICA":
    first_row = first_row_auto
elif tipo_estacion == "REAL":
    first_row = first_row_real

# URL base y formato de URL para cada mes
base_url = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/_dato_esta_tipo02.php?CBOFiltro=%s&estaciones={0}&t_e=M&estado={1}&cod_old=&cate_esta=EAMA&soloAlt=4".format(codigo_estacion, tipo_estacion)

start_date = "202308"
end_date = "202310"
current_date = start_date

# Crear un archivo CSV único para todos los datos con encabezados personalizados
with open(""+ruta_salida+"datos_senamhi_"+codigo_estacion+"_"+start_date+"_"+end_date+".csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)

    # Agregar encabezados al archivo CSV
    csv_writer.writerow(first_row)

    # Iterar para cada mes
    while current_date <= end_date:
        # Formatear la URL para el mes actual
        url = base_url % current_date

        # Realizar una solicitud GET a la página
        response = requests.get(url)

        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            # Analizar el contenido HTML de la página
            soup = BeautifulSoup(response.text, "html.parser")

            # Encontrar la segunda tabla con el ID "datTable"
            table = soup.find("table", {"id": "dataTable"})

            # Comprobar si se encontró la tabla
            if table:
                # Indicador para ignorar la primera fila
                skip_rows = 1 if tipo_estacion == "AUTOMATICA" else 2

                # Iterar a través de las filas de la tabla
                for i, row in enumerate(table.find_all("tr")):
                    # Ignorar la primera fila
                    if i < skip_rows:
                        continue

                    data = []
                    # Iterar a través de los elementos <div> en cada fila
                    for div in row.find_all("div"):
                        data.append(div.get_text(strip=True))  # Obtener el texto dentro del div
                    csv_writer.writerow(data)

            else:
                print(f"No se encontró la tabla 'datTable' en {url}")
        else:
            print(f"No se pudo acceder a {url}")

        year = int(current_date[:4])
        month = int(current_date[4:])
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        current_date = f"{year}{str(month).zfill(2)}"
print("Descarga de datos completada. Todos los datos se han guardado en 'todos_los_datos.csv' con encabezados personalizados.")
