import requests
from bs4 import BeautifulSoup
import numpy as np
from scipy.stats import poisson

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
        if nombre_equipo.lower() in clubs.lower():
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

            """
            # Eliminar la bandera a los equipos
            if (columnas[8].text.strip()[2] == ' '):
                oponente = columnas[8].text.strip()[3:]
            elif (columnas[8].text.strip()[3] == ' '):
                oponente = columnas[8].text.strip()[4:]
            else:"""
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
    probabilidades.append((calcular_goles(resultados)[0], round(calcular_goles(resultados)[0]/len(resultados),1)))
    probabilidades.append((calcular_goles(resultados)[1],round(calcular_goles(resultados)[1]/len(resultados),1)))
    probabilidades_local = calcular_probabilidad(resultados_local)
    probabilidades_local.append((calcular_goles(resultados_local)[0],round(calcular_goles(resultados_local)[0]/len(resultados_local),1)))
    probabilidades_local.append((calcular_goles(resultados_local)[1],round(calcular_goles(resultados_local)[1]/len(resultados_local),1)))
    probabilidades_visitante = calcular_probabilidad(resultados_visitante)
    probabilidades_visitante.append((calcular_goles(resultados_visitante)[0],round(calcular_goles(resultados_visitante)[0]/len(resultados_visitante),1)))
    probabilidades_visitante.append((calcular_goles(resultados_visitante)[1],round(calcular_goles(resultados_visitante)[1]/len(resultados_visitante),1)))
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

def calcular_probabilidad_apuesta(equipo,pais,local_visitante):
    probabilidad, probabilidad_handicap = 0, 0
    general, local, visitante, equipo = obtener_datos_equipo(equipo,pais)
    probabilidades, probabilidades_local, probabilidades_visitante = obtener_resultados(general,local,visitante)
    resultados = [probabilidades, probabilidades_local, probabilidades_visitante]
    probabilidad_ganar, probabilidad_empatar, probabilidad_perder = 0, 0, 0
    #print("Probando resultados:")
    #print(resultados)
    pesos = [0.6, 0.4]
    if local_visitante.lower() == 'local':
        # Cálculo de la probabilidad ponderada de ganar
        probabilidad_ganar = (pesos[0] * probabilidades[0]) + (pesos[1] * probabilidades_local[0])
        # Cálculo de la probabilidad ponderada de empatar
        probabilidad_empatar = (pesos[0] * probabilidades[1]) + (pesos[1] * probabilidades_local[1])
        # Cálculo de la probabilidad ponderada de perder
        probabilidad_perder = 1 - (probabilidad_ganar + probabilidad_empatar)
        #print(f'La probabilidad de acertar al 1 X = {(probabilidad_ganar+probabilidad_empatar)*100}%')
        probabilidad = [probabilidad_ganar, probabilidad_empatar, probabilidad_perder]
        #print(resultados)
        return probabilidad, equipo, resultados
    else:
        # Cálculo de la probabilidad ponderada de ganar
        probabilidad_ganar = (pesos[0] * probabilidades[0]) + (pesos[1] * probabilidades_visitante[0])
        # Cálculo de la probabilidad ponderada de empatar
        probabilidad_empatar = (pesos[0] * probabilidades[1]) + (pesos[1] * probabilidades_visitante[1])
        # Cálculo de la probabilidad ponderada de perder
        probabilidad_perder = 1 - (probabilidad_ganar + probabilidad_empatar)
        #print(f'La probabilidad de acertar al X 2 = {(probabilidad_ganar+probabilidad_empatar)*100}%')
        # Handicap
        probabilidad_handicap = calcular_handicap(general, visitante, pesos)        
        print(f'La probabilidad de acertar con handicap de +2 = {probabilidad_handicap*100}%')
        probabilidad = [probabilidad_ganar, probabilidad_empatar, probabilidad_perder]
        #print(resultados)
        return probabilidad, probabilidad_handicap, equipo, resultados

def calcular_handicap(general, visitante, pesos):
    handicap = 2
    casos_favorables_general, casos_favorables_visitante = 0, 0
    # Encontrando cuantos partidos se ganaron con ese handicap en los ultimos 10 partidos
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
    return probabilidad_handicap 

# probabilidad = [probabilidad_ganar, probabilidad_empatar, probabilidad_perder]
# probabilidad_handicap = number
# equipo = string
# resultados = [probabilidades, probabilidades_local, probabilidades_visitante]
def calcular_doble_oportunidad(probabilidades):
    # Calcula probabilidades de Doble Oportunidad
    ganar_empatar = probabilidades[0]+probabilidades[1]
    ganar_perder = probabilidades[0]+probabilidades[2]
    empatar_perder = probabilidades[1]+probabilidades[2]
    doble_oportunidad = [ganar_empatar, ganar_perder, empatar_perder]
    # Encuentra la maxima probabilidad
    max_probabilidad = max(doble_oportunidad)
    indice = -1
    rep = 0
    # Comprueba si hay una misma probabilidad entre dos eventos de doble oportunidad y selecciona un priorizando empates y local
    for i in doble_oportunidad:
        if i == max_probabilidad:
            rep += 1
    if rep > 1:
        if ganar_empatar == ganar_perder or ganar_empatar == empatar_perder:
            indice = 0
        elif ganar_perder == empatar_perder:
            indice = 2
        else:
            indice = 1
    else:
        indice = doble_oportunidad.index(max_probabilidad)
    return max_probabilidad, indice

def calcular_resultado_probable (local, visitante):
    # ganar_empatar = 0, ganar_perder = 1, empatar_perder = 2
    mejor_prob_local = calcular_doble_oportunidad(local[0])
    mejor_prob_visita = calcular_doble_oportunidad(visitante[0])
    pronostico = "N/A"
    if mejor_prob_local[1] == 0 and mejor_prob_visita[1] == 2:
        pronostico = '1X'
        print("Probabilidad Alta!")
        print("Primero")
    elif mejor_prob_local[1] == 0 and mejor_prob_visita[1] == 0:
        # Si el visitante ha sacado 3 victorias mas que el local el pronostico favorecera al visitante
        if (visitante[0][0]-local[0][0]) > 0.2:
            pronostico = 'X2'
        else:
            pronostico = '1X'
        print("Segundo")
    elif mejor_prob_local[1] == 0 and mejor_prob_visita[1] == 1:
        if mejor_prob_visita[0] > mejor_prob_local[0]:
            # Si el visitante ha ganado mas que el local y el porcentaje de victorias es mayor al de derrotas
            if visitante[0][0] > local[0][0] and visitante[0][0] > visitante[0][2]:
                pronostico = 'X2'
            else:
                pronostico = '1X'
        else:
            pronostico = '1X'
        print("Tercero")     
    elif mejor_prob_local[1] == 1 and mejor_prob_visita[1] == 1:
        # Solo apoya al visitante si ha ganado mas veces que el local
        if local[0][2] > local[0][0] and local[0][2] > visitante[0][2]:
            pronostico = 'X2'
        else:
            pronostico = '1X'
        print("Cuarto")
    elif mejor_prob_local[1] == 1 and mejor_prob_visita[1] == 0:
        if local[0][2] > 0.5:
            pronostico = 'X2'
        elif mejor_prob_visita[0] > mejor_prob_local[0]:
            # Si el visitante ha ganado mas que el local y el porcentaje de victorias es mayor al de derrotas
            if visitante[0][0] > local[0][0] and visitante[0][0] > visitante[0][2]:
                pronostico = 'X2'
            else:
                pronostico = '1X'
        else:
            pronostico = '1X'
        print("Quinto")
    elif mejor_prob_local[1] == 1 and mejor_prob_visita[1] == 2:
        # Si el local gana mas de lo que pierde
        if local[0][0] >= local[0][2]:
            pronostico = "1X"
        # Si el visitante pierde mas de lo que empata
        elif visitante[0][2] > visitante[0][1]:
            pronostico = "1X"
        else:
            pronostico = "X2"
        print("Sexto")
    elif mejor_prob_local[1] == 2 and mejor_prob_visita[1] == 0:
        pronostico = "X2"
        print("Probabilidad Alta!")
        print("Septimo")
    elif mejor_prob_local[1] == 2 and mejor_prob_visita[1] == 1:
        # Si el visitante gana mas de lo que pierde
        if visitante[0][0] >= visitante[0][2]:
            pronostico = "X2"
        # Si el local pierde mas de lo que empata
        elif local[0][2] > local[0][1]:
            pronostico = "X2"
        else:
            pronostico = "1X"
        print("Octavo")
    else:
        # Si el visitante pierde menos que el local
        if visitante[0][2] < local[0][2]:
            pronostico = "X2"
        else:
            pronostico = "1X"
        print("Noveno")
    return pronostico

def prob_goles(goles_local, goles_visitante):
    # Cálculo de los parámetros de la distribución Poisson
    media_goles_local = np.mean(goles_local)
    media_goles_visitante = np.mean(goles_visitante)

    # Cálculo de las probabilidades de goles usando la distribución Poisson
    probabilidades_local = poisson.pmf(goles_local, media_goles_local)
    probabilidades_visitante = poisson.pmf(goles_visitante, media_goles_visitante)

    return probabilidades_local, probabilidades_visitante

def resultado_exacto(local,visitante):
    resultado = "N/A"
    prob = []
    arreglo = []
    arreglo.append((local[0]+visitante[2])/2)
    arreglo.append((local[1]+visitante[1])/2)
    arreglo.append((local[2]+visitante[0])/2)
    print(arreglo)
    max_prob = 0
    for i in range(len(arreglo)):
        if arreglo[i] > arreglo[max_prob]:
            max_prob = i
        elif arreglo[i] == arreglo[max_prob] and i > 0:
            print("Hay dos probabilidades iguales")
            prob.append(i)
    prob.append(max_prob)
    print(max_prob)
    print(f"Probabilidades: {prob}")
    if len(prob) == 1:
        if prob[0] == 0:
            resultado = "1"
        elif prob[0] == 1:
            resultado = "X"
        else:
            resultado = "2"
    else:
        if 1 in prob:
            resultado = "X"
        else:
            if local[0] >= visitante[0]:
                resultado = "1"
            else:
                resultado = "2"
    return resultado