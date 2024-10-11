import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import streamlit as st

# Título de la aplicación
st.title('Optimización del Presupuesto de Marketing Digital')

# Definición de las restricciones
# Coeficientes para maximizar 2x + (15/7)y
c = [-2, -15/7]

# Definición de las matrices de restricciones
A = [[1, 1],  # x + y <= 10000
     [1, 0],  # x <= 6000
     [0, 1]]  # y <= 5000

b = [10000, 6000, 5000]

# Resolución del problema de programación lineal
result = linprog(c, A_ub=A, b_ub=b, bounds=((0, None), (0, None)), method='highs')

# Resultados
if result.success:
    optimal_x, optimal_y = result.x
    max_clicks = -result.fun
    st.success(f"Inversión óptima en Google Ads: ${optimal_x:.2f}")
    st.success(f"Inversión óptima en Facebook Ads: ${optimal_y:.2f}")
    st.success(f"Número máximo de clics: {max_clicks:.2f}")
else:
    st.error("No se pudo encontrar una solución óptima.")

# Graficar las restricciones
x = np.linspace(0, 8000, 400)
y1 = 10000 - x  # x + y <= 10000
y2 = 5000 * np.ones_like(x)  # y <= 5000
x2 = 6000 * np.ones_like(x)  # x <= 6000

plt.figure(figsize=(10, 6))
plt.plot(x, y1, label=r'$x + y \leq 10000$', color='blue')
plt.plot(x, y2, label=r'$y \leq 5000$', color='orange')
plt.axvline(x=6000, label=r'$x \leq 6000$', color='green')

# Rellenar la región factible
plt.fill_between(x, 0, np.minimum(y1, y2), where=(x <= 6000), color='gray', alpha=0.5)

# Marcar la solución óptima
if result.success:
    plt.plot(optimal_x, optimal_y, 'ro', label='Solución Óptima')

# Configuración del gráfico
plt.xlim(0, 8000)
plt.ylim(0, 6000)
plt.xlabel('Inversión en Google Ads ($)')
plt.ylabel('Inversión en Facebook Ads ($)')
plt.title('Optimización del Presupuesto de Marketing Digital')
plt.legend()
plt.grid()

# Mostrar el gráfico en Streamlit
st.pyplot(plt)
