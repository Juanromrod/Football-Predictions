from django.shortcuts import render
from .footballData import calcular_probabilidad_apuesta

def calcular_probabilidad(request):
    if request.method == 'POST':
        equipo = request.POST.get('equipo')
        pais = request.POST.get('pais')
        local_visitante = request.POST.get('local_visitante')
        handicap = 0
        visitante = False
        
        if local_visitante.lower() == 'v':
            visitante = True
            handicap = int(request.POST.get('handicap'))

        probabilidad, probabilidad_handicap, equipo, resultados = calcular_probabilidad_apuesta(equipo, pais, local_visitante, handicap)
        probabilidad = round(probabilidad*100,2)
        probabilidad_handicap = round(probabilidad_handicap * 100,2)
        resultados_multiplicados = [[elemento * 100 if not isinstance(elemento, tuple) else elemento for elemento in sub_arreglo] for sub_arreglo in resultados]

        
        context = {
            'equipo': equipo,
            'probabilidad': probabilidad,
            'handicap': handicap,
            'probabilidad_handicap': probabilidad_handicap,
            'visitante': visitante,
            'resultados': resultados_multiplicados,
        }

        return render(request, 'FootballPredictionsApp/calcular_probabilidad.html', context)

    return render(request, 'FootballPredictionsApp/calcular_probabilidad.html')

