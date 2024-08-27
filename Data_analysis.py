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

# Crear un DataFrame separado que agrupe todos los meses para cada tipster
tipster_total_analysis = data_csv.groupby(['Tipster']).agg({
    'Profit': 'sum',
    'Stake': 'sum'
}).reset_index()

# Calcular el yield total para cada tipster
tipster_total_analysis['Yield'] = (tipster_total_analysis['Profit'] / tipster_total_analysis['Stake']) * 100

# tipster_total_analysis[['Profit', 'Stake']] = tipster_total_analysis[['Profit', 'Stake']].applymap(lambda x: f"{x:,.0f}")
# Verificar el DataFrame agrupado por tipster
print(tipster_total_analysis)

tipster_total_analysis['Profit'] = pd.to_numeric(tipster_total_analysis['Profit'], errors='coerce')

"""
Gráfico de barras con yield
"""

plt.figure(figsize=(12, 12))
plt.bar(tipster_total_analysis['Tipster'], tipster_total_analysis['Profit'], color='skyblue')

# Configuración del gráfico
plt.xlabel('Tipster analizado')
plt.ylabel('Profit')
plt.title('Profit por Tipster 1er semestre 2024')

# Preparar el texto para el cuadro
header = 'Tipster         Yield\n'
rows = '\n'.join([
    f"{row['Tipster'][:15]:<15} {row['Yield']:.2f}"
    for index, row in tipster_total_analysis.iterrows()
])
textstr = header + rows

# Posición del cuadro de texto
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.gca().text(
    0.95, 0.05,  # posición (x, y) en la figura
    textstr,
    transform=plt.gca().transAxes,  # usa coordenadas en relación al eje
    fontsize=10,
    verticalalignment='bottom',
    horizontalalignment='right',
    bbox=props
)

# Ajustar el diseño y mostrar el gráfico
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('./Rendimiento_con_yield.png', dpi=300)
# plt.show()

"""
Gráfico scatter Yield
"""

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

plt.figure(figsize=(12, 8))
plt.scatter(tipster_total_analysis['Yield'], tipster_total_analysis['Profit'], color='orange')

# Configurar etiquetas y título
plt.xlabel('Yield', fontsize=20, color='Black')
plt.ylabel('Profit', fontsize=20, color='Black')
plt.title('Profit vs Yield por Tipster', fontsize=22, color='Black')

# Etiquetar los puntos con los nombres de los tipsters
for i, row in tipster_total_analysis.iterrows():
    plt.text(row['Yield'], row['Profit'], row['Tipster'], fontsize=9, ha='right')

plt.grid(True)
plt.tight_layout()
plt.savefig('./Profit_vs_Yield_por_Tipster.png', dpi=300)
# plt.show()


'''
PRUEBAS 
'''

# plt.figure(figsize=(10, 6))
# plt.scatter(tipster_total_analysis['Yield'], tipster_total_analysis['Profit'], color='blue')
# plt.xlabel('Yield')
# plt.ylabel('Profit')
# plt.title('Profit vs Yield')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig('./Profit_vs_Yield.png', dpi=300)
# plt.show()
"""
Gráfica horizontal con rendimiento y yield por tipster  ME GUSTÓ MÁS ESTA
"""
plt.rcParams['figure.figsize'] = (12, 8)
fig, ax = plt.subplots()

# Crear el gráfico de barras horizontal
bars = ax.barh(tipster_total_analysis['Tipster'], tipster_total_analysis['Profit'], color='skyblue')

# Configurar etiquetas y título
font_used = {'fontname': 'DejaVu Sans', 'color': 'Black'}
ax.set_xlabel('Profit', fontsize=20, **font_used)
ax.set_ylabel('Tipster analizado', fontsize=20, **font_used)
ax.set_title('Profit por Tipster', fontsize=22, **font_used)

# Preparar el texto para el cuadro
header = 'Tipster         Yield\n'
rows = '\n'.join([
    f"{row['Tipster'][:15]:<15} {row['Yield']:.2f}"
    for index, row in tipster_total_analysis.iterrows()
])
textstr = header + rows

# Posición del cuadro de texto
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

plt.gca().text(
    0.95, 0.05,  # posición (x, y) en la figura
    textstr,
    transform=plt.gca().transAxes,  # usa coordenadas en relación al eje
    fontsize=10,
    verticalalignment='bottom',
    horizontalalignment='right',
    bbox=props
)

# Ajustar el diseño y mostrar el gráfico
plt.tight_layout()
# Añadir un ajuste a los límites del gráfico para asegurar visibilidad
plt.xlim(ax.get_xlim()[0], ax.get_xlim()[1] + 0.3 * (ax.get_xlim()[1] - ax.get_xlim()[0]))

plt.savefig('./Profit_por_Tipster_Horizontal_con_Yield.png', dpi=300)
# plt.show()


