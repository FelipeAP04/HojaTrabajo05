import sys
print(sys.executable)

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

def main():
    resultados_a = []
    resultados_b = []

    # Inciso a
    print("Inciso a:")
    for num_procesos in [25, 50, 100, 150, 200]:
        datos = simular(num_procesos)
        resultados_a.append(datos)
        print(f"Para {num_procesos} procesos:")
        for proceso, tiempo_promedio, desviacion_estandar in datos:
            print(f"Proceso: {proceso}, Tiempo promedio: {tiempo_promedio}, Desviación estándar: {desviacion_estandar}")

    graficar_varios(resultados_a, "a")

    # Inciso b
    print("\nInciso b:")
    for intervalo in [5, 1]:
        resultados_b_intervalo = []
        for num_procesos in [25, 50, 100, 150, 200]:
            datos = simular(num_procesos, intervalo)
            resultados_b_intervalo.append(datos)
            print(f"Para {num_procesos} procesos con intervalo {intervalo}:")
            for proceso, tiempo_promedio, desviacion_estandar in datos:
                print(f"Proceso: {proceso}, Tiempo promedio: {tiempo_promedio}, Desviación estándar: {desviacion_estandar}")
        resultados_b.append((intervalo, resultados_b_intervalo))

    graficar_varios(resultados_b, "b")

def simular(num_procesos, intervalo_creacion_procesos=10):
    random_seed = 42
    capacidad_RAM = 100
    instrucciones_CPU = 3

    random.seed(random_seed)

    resultados = []

    for _ in range(10):  # Realizar múltiples simulaciones para obtener una muestra
        tiempos_procesos = []
        env = simpy.Environment()
        RAM = simpy.Container(env, init=capacidad_RAM, capacity=capacidad_RAM)
        CPU = simpy.Resource(env, capacity=1)

        for _ in range(num_procesos):
            env.process(llegada_procesos(env, RAM, CPU, tiempos_procesos, instrucciones_CPU))

        env.run(until=1000)  # Tiempo de simulación más largo

        tiempo_promedio = np.mean(tiempos_procesos)
        desviacion_estandar = np.std(tiempos_procesos)
        
        resultados.append((num_procesos, tiempo_promedio, desviacion_estandar))

    return resultados


def llegada_procesos(env, RAM, CPU, tiempos_procesos, instrucciones_CPU):
    memoria_necesaria = random.randint(1, 10)
    yield RAM.get(memoria_necesaria)

    instrucciones_totales = random.randint(1, 10)
    tiempo_inicio = env.now

    with CPU.request() as req:
        yield req
        while instrucciones_totales > 0:
            yield env.timeout(1)  # Simular 1 unidad de tiempo de CPU
            instrucciones_totales -= instrucciones_CPU
        tiempo_fin = env.now
        tiempo_proceso = tiempo_fin - tiempo_inicio
        tiempos_procesos.append(tiempo_proceso)
    yield RAM.put(memoria_necesaria)

def graficar_varios(resultados, inciso):
    for datos in resultados:
        num_procesos, tiempos_promedio, desviaciones_estandar = zip(*datos)
        plt.errorbar(num_procesos, tiempos_promedio, yerr=desviaciones_estandar, fmt='o', label=f"Inciso {inciso}")
    plt.title(f'Tiempo Promedio vs Número de Procesos (Inciso {inciso})')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Tiempo Promedio')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()