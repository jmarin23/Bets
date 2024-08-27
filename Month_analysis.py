import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
data_csv = pd.read_csv('./Primer_semestre_2024.csv')

data_csv['Date'] = pd.to_datetime(data_csv['Date'], format='%m/%d/%Y %H:%M')
meses = {
    1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL',
    5: 'MAYO', 6: 'JUNIO', 7: 'JULIO', 8: 'AGOSTO',
    9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
}
data_csv['Mes'] = data_csv['Date'].dt.month.map(meses)
print(data_csv[['Date', 'Mes']])

columns_to_drop = ['Date', 'Category', 'Competition', 'Winning bonus', 'Commission', 'Closing Odds', 'Comment', 'Type of bet' , 'Live', 'Free bet']
cleaned_data = data_csv.drop(columns=columns_to_drop)
print(cleaned_data.head(5))

print(data_csv['Tipster'].unique())

# Rellenar los valores NaN en la columna 'Tipster' con 'Lbtennis'
data_csv['Tipster'] = data_csv['Tipster'].fillna('Lbtennis')

# Verificar que los valores NaN han sido reemplazados
print(data_csv['Tipster'].unique())


# Agrupar por 'Tipster' y 'Mes', y calcular el total de 'Profit' y 'Stake'
tipster_month_analysis = data_csv.groupby(['Tipster', 'Mes']).agg({
    'Profit': 'sum',
    'Stake': 'sum'
}).reset_index()
# 1. Agregar la columna 'yield' a tipster_month_analysis
tipster_month_analysis['Yield'] = (tipster_month_analysis['Profit'] / tipster_month_analysis['Stake']) * 100
# tipster_month_analysis[['Profit', 'Stake']] = tipster_month_analysis[['Profit', 'Stake']].applymap(lambda x: f"{x:,.0f}")
# Verificar los datos con la nueva columna 'Yield'
print(tipster_month_analysis.head())


""""
Graficos
"""

order = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']

# Iterar sobre cada tipster
for tipster in tipster_month_analysis['Tipster'].unique():
    data = tipster_month_analysis[tipster_month_analysis['Tipster'] == tipster]
    
    # Ordenar los datos por Mes para asegurar el orden correcto
    data = data.sort_values('Mes', key=lambda x: x.map({month: i for i, month in enumerate(order)}))
    data = data.sort_values('Mes')


    # Calcular las métricas acumuladas
    data['Cumulative_Profit'] = data['Profit'].cumsum()
    data['Cumulative_Stake'] = data['Stake'].cumsum()
    data['Cumulative_Yield'] = (data['Cumulative_Profit'] / data['Cumulative_Stake']) * 100

    # Crear una figura y ejes para el gráfico
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Graficar Profit acumulado
    ax1.plot(data['Mes'], data['Cumulative_Profit'], marker='o', color='blue', label='Profit Acumulado')
    ax1.set_xlabel('Mes', fontsize=16)
    ax1.set_ylabel('Profit Acumulado', fontsize=16, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Crear un segundo eje para Stake acumulado
    ax2 = ax1.twinx()
    ax2.plot(data['Mes'], data['Cumulative_Stake'], marker='o', color='green', label='Stake Acumulado')
    ax2.set_ylabel('Stake Acumulado', fontsize=16, color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    # Crear un tercer eje para Yield acumulado
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Mover el tercer eje hacia la derecha
    ax3.plot(data['Mes'], data['Cumulative_Yield'], marker='o', color='red', label='Yield Acumulado')
    ax3.set_ylabel('Yield Acumulado (%)', fontsize=16, color='red')
    ax3.tick_params(axis='y', labelcolor='red')

    # Configurar el título y el diseño
    plt.title(f'Análisis Acumulado de {tipster}', fontsize=22)
    
    # Añadir leyendas
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='upper left')
    
    # Configurar el título y el diseño
    plt.title(f'Análisis Acumulado de {tipster}', fontsize=22, color='white')
    ax1.grid(color='white', linestyle='--', linewidth=0.5)  # Ajustar el color del grid para que sea visible
    
    # Personalizar el fondo
    fig.patch.set_facecolor('black')  # Fondo de la figura
    ax1.set_facecolor('black')  # Fondo del eje
    
    # Ajustar etiquetas del eje x
    plt.xticks(rotation=45, color='white')
    plt.tight_layout()
    plt.show()