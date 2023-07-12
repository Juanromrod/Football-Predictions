import requests
from bs4 import BeautifulSoup

def obtener_Liga(nombre_pais):
    print('Buscando equipo...')
    # URL de la página de resultados del equipo
    base_url = 'https://fbref.com/en/squads'

    # Realizar la solicitud GET a la página
    response = requests.get(base_url)

    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(response.content, features='html.parser')

    # Encontrar la tabla de resultados
    tabla_resultados = soup.find('table', id="countries")

    # Verificar si se encontraron resultados para el pais
    if tabla_resultados is None:
        print('No se encontraron resultados para el país.')
        return

    # Encontrar las filas de los resultados
    filas_resultados = tabla_resultados.find_all('tr')

    # Recorrer las filas y extraer los resultados
    liga_link = None
    for fila in filas_resultados:
        # Extrae las columnas
        liga = fila.find_all('th')[0].text.strip()
        if nombre_pais.capitalize() in liga:
            print(liga)
            liga_link = base_url[:17]+fila.find_next('a')['href']
            break
    # Verificar si se encontró el enlace del equipo
    if liga_link is None:
        print('No se encontró la liga.')
    else:
        print(liga_link)

    return liga_link

def obtener_Equipo(nombre_equipo, liga_link):
    print('Buscando equipo...')

    # URL base de la página de equipos
    url_base = 'https://fbref.com/en/squads/'
    
    # Realizar la solicitud GET a la página
    response = requests.get(liga_link)

    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(response.content, features='html.parser')

    # Encontrar la tabla de resultados
    tabla_resultados = soup.find('table', id="clubs")

    # Verificar si se encontraron resultados para el pais
    if tabla_resultados is None:
        print('No se encontraron resultados.')
        return

    # Encontrar las filas de los resultados
    filas_resultados = tabla_resultados.find_all('tr')

    # Recorrer las filas y extraer los resultados
    equipo_link = None
    for fila in filas_resultados:
        # Extrae las columnas
        clubs = fila.find_all('th')[0].text.strip()
        if nombre_equipo.capitalize() in clubs:
            equipo = clubs
            print(equipo)
            club_id = fila.find_next('a')['href'][11:19]
            equipo_link = url_base + club_id
            break
    # Verificar si se encontró el enlace del equipo
    if equipo_link is None:
        print('No se encontró el equipo.')

    return equipo, equipo_link

def obtener_datos_equipo(nombre_equipo, nombre_pais):
    # Obtener la URL del equipo
    equipo, url = obtener_Equipo(nombre_equipo, obtener_Liga(nombre_pais))
    print(url)

    # Realizar la solicitud GET a la página
    response = requests.get(url)

    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(response.content, features='html.parser')

    # Encontrar la tabla de resultados
    tabla_resultados = soup.find('table', id="matchlogs_for")

    # Encontrar las filas de los resultados
    filas_resultados = tabla_resultados.find_all('tr')

    # Recorrer las filas al revés y extraer los resultados
    resultados, resultados_local, resultados_visitante = [], [], []

    for fila in reversed(filas_resultados[1:]):  # Recorrer las filas en reversa
        # Extraer las columnas
        columnas = fila.find_all('td')

        # Extraer el resultado
        resultado = columnas[5].text.strip()

        # Verificar si el partido se ha jugado y tiene un resultado
        if resultado:
            # Extraer la fecha
            fecha = fila.find('th').text.strip()

            # Eliminar la bandera a los equipos
            if (columnas[8].text.strip()[2] == ' '):
                oponente = columnas[8].text.strip()[3:]
            elif (columnas[8].text.strip()[3] == ' '):
                oponente = columnas[8].text.strip()[4:]
            else:
                oponente = columnas[8].text.strip()

            # Agregar el marcador
            goles_favor = columnas[6].text.strip()[0]
            goles_contra = columnas[7].text.strip()[0]

            # Verificar si el equipo jugó como local o visitante
            local_visitante = columnas[4].text.strip()
            if local_visitante == 'Home' and len(resultados_local) < 10:
                resultados_local.append((fecha, oponente, resultado, goles_favor, goles_contra))
            elif local_visitante == 'Away' and len(resultados_visitante) < 10:
                resultados_visitante.append((fecha, oponente, resultado, goles_favor, goles_contra))

            if len(resultados) < 10:
                resultados.append((fecha, oponente, resultado, goles_favor, goles_contra))

        # Verificar si se han obtenido los últimos 10 partidos jugados
        if len(resultados) >= 10 and len(resultados_local) >= 10 and len(resultados_visitante) >= 10:
            break

    # Imprimir los resultados en orden inverso
    """print("Últimos 10 partidos jugados:")
    for resultado in reversed(resultados):
        print(f'Fecha: {resultado[0]}, Oponente: {resultado[1]}, Resultado: {resultado[2]} {resultado[3]}-{resultado[4]}')

    print("Últimos 10 partidos como local:")
    for resultado in reversed(resultados_local):
        print(f'Fecha: {resultado[0]}, Oponente: {resultado[1]}, Resultado: {resultado[2]} {resultado[3]}-{resultado[4]}')

    print("Últimos 10 partidos como visitante:")
    for resultado in reversed(resultados_visitante):
        print(f'Fecha: {resultado[0]}, Oponente: {resultado[1]}, Resultado: {resultado[2]} {resultado[3]}-{resultado[4]}')"""

    return resultados, resultados_local, resultados_visitante, equipo

def obtener_resultados(resultados, resultados_local, resultados_visitante):
    probabilidades, probabilidades_local, probabilidades_visitante = [], [], []
    probabilidades = calcular_probabilidad(resultados)
    probabilidades.append((calcular_goles(resultados)[0],calcular_goles(resultados)[0]/len(resultados)))
    probabilidades.append((calcular_goles(resultados)[1],calcular_goles(resultados)[1]/len(resultados)))
    probabilidades_local = calcular_probabilidad(resultados_local)
    probabilidades_local.append((calcular_goles(resultados_local)[0],calcular_goles(resultados_local)[0]/len(resultados_local)))
    probabilidades_local.append((calcular_goles(resultados_local)[1],calcular_goles(resultados_local)[1]/len(resultados_local)))
    probabilidades_visitante = calcular_probabilidad(resultados_visitante)
    probabilidades_visitante.append((calcular_goles(resultados_visitante)[0],calcular_goles(resultados_visitante)[0]/len(resultados_visitante)))
    probabilidades_visitante.append((calcular_goles(resultados_visitante)[1],calcular_goles(resultados_visitante)[1]/len(resultados_visitante)))
    print(f'Resultados (Últimos 10 partidos):')
    print(f'Goles anotados: {probabilidades[3][0]} ({probabilidades[3][1]}) || Goles recibidos: {probabilidades[4][0]} ({probabilidades[4][1]})')
    print(f'Victoria: {probabilidades[0]*100}%')
    print(f'Empate: {probabilidades[1]*100}%')
    print(f'Derrota: {probabilidades[2]*100}%')
    print(f'Resultados como local (Últimos 10 partidos):')
    print(f'Goles anotados: {probabilidades_local[3][0]} ({probabilidades_local[3][1]}) || Goles recibidos: {probabilidades_local[4][0]} ({probabilidades_local[4][1]})')
    print(f'Victoria: {probabilidades_local[0]*100}%')
    print(f'Empate: {probabilidades_local[1]*100}%')
    print(f'Derrota: {probabilidades_local[2]*100}%')
    print(f'Resultados como visitante: (Últimos 10 partidos)')
    print(f'Goles anotados: {probabilidades_visitante[3][0]} ({probabilidades_visitante[3][1]}) || Goles recibidos: {probabilidades_visitante[4][0]} ({probabilidades_visitante[4][1]})')
    print(f'Victoria: {probabilidades_visitante[0]*100}%')
    print(f'Empate: {probabilidades_visitante[1]*100}%')
    print(f'Derrota: {probabilidades_visitante[2]*100}%')
    return probabilidades, probabilidades_local, probabilidades_visitante

def calcular_goles(resultados):
    goles_anotados = 0
    goles_recibidos = 0
    for r in resultados:
        goles_anotados += int(r[3])
        goles_recibidos += int(r[4])
    return goles_anotados, goles_recibidos

def calcular_probabilidad(resultados):
    v = 0
    e = 0
    d = 0
    for r in resultados:
        if r[2].lower() == 'w':
            v+=1
        elif r[2].lower() == 'l':
            d+=1
        else:
            e += 1
    return [v/10,e/10,d/10]

def calcular_probabilidad_apuesta(equipo,pais,local_visitante, handicap):
    probabilidad, probabilidad_handicap = 0, 0
    general, local, visitante, equipo = obtener_datos_equipo(equipo,pais)
    probabilidades, probabilidades_local, probabilidades_visitante = obtener_resultados(general,local,visitante)
    resultados = [probabilidades, probabilidades_local, probabilidades_visitante]
    #print("Probando resultados:")
    #print(resultados)
    pesos = [0.6, 0.4]
    if local_visitante.lower() == 'l':
        # Cálculo de la probabilidad ponderada de ganar
        probabilidad_ganar = (pesos[0] * probabilidades[0]) + (pesos[1] * probabilidades_local[0])
        # Cálculo de la probabilidad ponderada de empatar
        probabilidad_empatar = (pesos[0] * probabilidades[1]) + (pesos[1] * probabilidades_local[1])
        probabilidad = probabilidad_ganar + probabilidad_empatar
        print(f'La probabilidad de acertar al 1 X = {probabilidad*100}%')
    elif local_visitante.lower() == 'v':
        # Cálculo de la probabilidad ponderada de ganar
        probabilidad_ganar = (pesos[0] * probabilidades[0]) + (pesos[1] * probabilidades_visitante[0])
        # Cálculo de la probabilidad ponderada de empatar
        probabilidad_empatar = (pesos[0] * probabilidades[1]) + (pesos[1] * probabilidades_visitante[1])
        probabilidad = probabilidad_ganar + probabilidad_empatar
        print(f'La probabilidad de acertar al X 2 = {probabilidad*100}%')
        # Handicap
        casos_favorables_general, casos_favorables_visitante = 0, 0
        # Encontrando cuantos partidos se ganaron con ese handicap en los ultimos 10 partidos
        if handicap > 0:
            #print("General:")
            for r in general:
                #print(r)
                if int(r[3])+handicap > int(r[4]):
                    #print(f'Favorable {r[3]}+2 - {r[4]}')
                    casos_favorables_general+=1
            # Encontrando cuantos partidos se ganaron con ese handicap en los ultimos 10 partidos de visitante
            #print("Visitante:")
            for v in visitante:
                #print(v)
                if int(v[3])+handicap > int(v[4]):
                    #print(f'Favorable {v[3]}+2 - {v[4]}')
                    casos_favorables_visitante+=1
            # Cálculo de la probabilidad ponderada de ganar con handicap
            probabilidad_handicap = (pesos[1] * casos_favorables_general/len(general)) + (pesos[0] * casos_favorables_visitante/len(visitante))
            print(f'La probabilidad de acertar con handicap de {handicap} = {probabilidad_handicap*100}%')
    #print(resultados)
    return probabilidad, probabilidad_handicap, equipo, resultados