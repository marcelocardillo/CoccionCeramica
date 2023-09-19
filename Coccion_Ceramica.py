import streamlit as st
import pandas as pd
import altair as alt

# Título de la aplicación
st.title('Gráfico de Temperatura de Cocción')

# Sidebar con controles de entrada
st.sidebar.header('Configuración de Datos')

# Campo de entrada de hora en formato numérico
hora_decimal = st.sidebar.number_input('Hora de Cocción (en horas):', 0.0, 24.0, 0.0)

temperatura = st.sidebar.number_input('Temperatura de Cocción (en °C):', 0, 1500, 100)

# Botón para agregar datos
if st.sidebar.button('Agregar Datos'):
    data = {'Hora': [hora_decimal], 'Temperatura': [temperatura]}
    df = pd.DataFrame(data)

    # Si es la primera vez que se agrega un dato, creamos el DataFrame
    if 'data' not in st.session_state:
        st.session_state.data = df
        y_min = temperatura  # Establecer el límite inferior del eje y
    else:
        # Si ya existe el DataFrame, lo actualizamos agregando los nuevos datos
        st.session_state.data = pd.concat([st.session_state.data, df], ignore_index=True)
        y_min = min(st.session_state.data['Temperatura'])  # Actualizar el límite inferior del eje y

# Gráfico de línea con los datos ingresados
if 'data' in st.session_state:
    st.header('Gráfico de Temperatura de Cocción')
    chart = alt.Chart(st.session_state.data).mark_line(color='#0068c9').encode(
        x='Hora:Q',  # Cambio en el eje X
        y=alt.Y('Temperatura:Q', scale=alt.Scale(domain=[y_min, 1500]))  # Personalizar el límite inferior del eje y
    ).properties(height=500, width=500)
    st.altair_chart(chart)

    # Calcular la media de temperatura a partir de la segunda medición
    if len(st.session_state.data) > 1:
        mean_temperature = st.session_state.data['Temperatura'].mean()
        st.write(f'Media de Temperatura a partir de la segunda medición: {mean_temperature:.3f} °C')

    # Calcular el tiempo total de cocción en horas
    total_cooking_time = st.session_state.data['Hora'].max() - st.session_state.data['Hora'].min()
    st.write(f'Tiempo Total de Cocción en Horas: {total_cooking_time:.3f} horas')
