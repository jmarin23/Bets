# Bets Analysis

Este repositorio contiene varios scripts de Python para analizar datos relacionados con apuestas. Los códigos están diseñados para realizar análisis detallados de los resultados de apuestas, incluyendo el análisis mensual y acumulativo por tipster.

## Estructura del Repositorio

- **Data_analysis.py**: Este script contiene funciones y análisis generales para trabajar con conjuntos de datos relacionados con apuestas. Realiza cálculos estadísticos básicos y organiza la información para facilitar su visualización y análisis.

- **Month_analysis.py**: Este script está enfocado en el análisis mensual de los datos de apuestas. 
  - Genera gráficos para visualizar el profit acumulado, stake acumulado y yield acumulado de los tipsters, organizados por mes.
  - Permite analizar el rendimiento de cada tipster en diferentes periodos y calcular métricas acumulativas.

- **Primer_semestre_2024.csv**: Este archivo contiene los datos de las apuestas realizadas durante el primer semestre de 2024. Es la base de datos utilizada por los scripts para realizar los análisis.

## Requisitos

Para ejecutar los scripts, asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install pandas matplotlib
