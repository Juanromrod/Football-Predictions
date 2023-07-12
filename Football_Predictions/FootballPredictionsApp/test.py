import footballData as fd

# Solicitar el nombre del equipo al usuario
equipo = input('Ingrese el nombre del equipo: ')
pais = input('Ingrese el país del equipo: ')
local_visitante = input('El equipo juega de Local o Visitante? ')

# Obtener los resultados del equipo
try:
#calcular_probabilidad_apuesta(equipo, pais)
#general, local, visitante = obtener_datos_equipo(equipo,pais)
#probabilidades = obtener_resultados(general,local,visitante)
    fd.calcular_probabilidad_apuesta(equipo,pais,local_visitante)
except:
    print('Parece que no se ha encontrado el equipo, busque el nombre del equipo en esta web: ')
    print('https://fbref.com/en/squads/')
#print(obtener_URL('Barcelona','Ecuador'))
#calcular_probabilidad_apuesta(equipo,pais,local_visitante)
#print(obtener_Equipo(equipo, obtener_Liga(pais)))