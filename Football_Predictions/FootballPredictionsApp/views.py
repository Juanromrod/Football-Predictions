from django.shortcuts import render
from .footballData import calcular_probabilidad_apuesta, calcular_resultado_probable

def calcular_probabilidad(request):
    if request.method == 'POST':
        equipo1 = request.POST.get('equipo-local')
        pais1 = request.POST.get('pais-local')
        equipo2 = request.POST.get('equipo-visitante')
        pais2 = request.POST.get('pais-visitante')

        local = calcular_probabilidad_apuesta(equipo1, pais1, 'local')
        visitante = calcular_probabilidad_apuesta(equipo2, pais2, 'visitante')
        probabilidad1, equipo1, resultados1 = local
        probabilidad2, probabilidad_handicap2, equipo2, resultados2 = visitante
        pronostico = calcular_resultado_probable(local,visitante)
        probabilidad_handicap2 = round(probabilidad_handicap2 * 100,2)
        resultados_multiplicados1 = [[elemento * 100 if not isinstance(elemento, tuple) else elemento for elemento in sub_arreglo] for sub_arreglo in resultados1]
        resultados_multiplicados2 = [[elemento * 100 if not isinstance(elemento, tuple) else elemento for elemento in sub_arreglo] for sub_arreglo in resultados2]
        
        context = {
            'local': equipo1,
            'probabilidad_local': probabilidad1,
            'probabilidad_visitante': probabilidad2,
            'handicap': 2,
            'probabilidad_handicap2': probabilidad_handicap2,
            'visitante': equipo2,
            'resultados_local': resultados_multiplicados1,
            'resultados_visitante': resultados_multiplicados2,
            'pronostico': pronostico,
        }

        return render(request, 'FootballPredictionsApp/calcular_probabilidad.html', context)

    return render(request, 'FootballPredictionsApp/calcular_probabilidad.html')

