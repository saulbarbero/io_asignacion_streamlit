# =====================================================
# PROYECTO FINAL - ASIGNACIÓN ÓPTIMA DE TAREAS

# =====================================================

import streamlit as st
import pandas as pd
import pulp as pl

# -----------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------
st.set_page_config(
    page_title="Asignación de Tareas",
    page_icon="🛠️",
    layout="wide"
)

# -----------------------------------------------------
# DATOS DE EJEMPLO 
# -----------------------------------------------------

programadores_ejemplo = [
    "Sergio Robles",
    "Saúl Barbero",
    "Carlos Urías",
    "Mateo Alfredo"
]

tareas_ejemplo = ["Frontend", "Backend", "Testing", "BaseDatos"]

disponibilidad_ejemplo = {
    "Sergio Robles": 20,
    "Saúl Barbero": 20,
    "Carlos Urías": 20,
    "Mateo Alfredo": 20
}

# Tiempos estimados (horas) 
tiempos_ejemplo = {
    ("Sergio Robles", "Frontend"): 10,
    ("Sergio Robles", "Backend"): 12,
    ("Sergio Robles", "Testing"): 9,
    ("Sergio Robles", "BaseDatos"): 8,

    ("Saúl Barbero", "Frontend"): 9,
    ("Saúl Barbero", "Backend"): 11,
    ("Saúl Barbero", "Testing"): 10,
    ("Saúl Barbero", "BaseDatos"): 12,

    ("Carlos Urías", "Frontend"): 8,
    ("Carlos Urías", "Backend"): 9,
    ("Carlos Urías", "Testing"): 7,
    ("Carlos Urías", "BaseDatos"): 10,

    ("Mateo Alfredo", "Frontend"): 12,
    ("Mateo Alfredo", "Backend"): 13,
    ("Mateo Alfredo", "Testing"): 11,
    ("Mateo Alfredo", "BaseDatos"): 15
}


def crear_dataframes_desde_ejemplo():
    """Crea los DataFrames de programadores y tiempos a partir de los datos de ejemplo."""
    df_prog = pd.DataFrame({
        "Programador": programadores_ejemplo,
        "Disponibilidad": [disponibilidad_ejemplo[p] for p in programadores_ejemplo]
    })

    df_tiempos = pd.DataFrame(
        index=programadores_ejemplo,
        columns=tareas_ejemplo
    )

    for p in programadores_ejemplo:
        for t in tareas_ejemplo:
            df_tiempos.loc[p, t] = tiempos_ejemplo[(p, t)]

    df_tiempos = df_tiempos.astype(float)
    return df_prog, df_tiempos


# -----------------------------------------------------
# RESOLVER MODELO DE ASIGNACIÓN
# -----------------------------------------------------

def resolver_asignacion(df_prog, df_tiempos):
    """
    Resuelve el modelo de asignación de tareas.
    df_prog: DataFrame con columnas ['Programador', 'Disponibilidad']
    df_tiempos: DataFrame con índice = Programador, columnas = tareas, valores = tiempo
    """

    programadores = df_prog["Programador"].tolist()
    tareas = df_tiempos.columns.tolist()

    # Disponibilidad
    disponibilidad = {
        fila["Programador"]: float(fila["Disponibilidad"])
        for _, fila in df_prog.iterrows()
    }

    # Tiempos y compatibilidad
    tiempo = {}
    compatibilidad = {}
    for p in programadores:
        for t in tareas:
            valor = float(df_tiempos.loc[p, t])
            tiempo[(p, t)] = valor
            compatibilidad[(p, t)] = 0 if valor == 0 else 1

    # Modelo
    modelo = pl.LpProblem("Asignacion_de_Tareas", pl.LpMinimize)

    x = pl.LpVariable.dicts(
        "x",
        (programadores, tareas),
        lowBound=0,
        upBound=1,
        cat="Binary"
    )

    # Función objetivo
    modelo += pl.lpSum(
        tiempo[(p, t)] * x[p][t]
        for p in programadores
        for t in tareas
    ), "Tiempo_Total"

    # Cada tarea se asigna exactamente a un programador
    for t in tareas:
        modelo += pl.lpSum(x[p][t] for p in programadores) == 1

    # Restricción de disponibilidad
    for p in programadores:
        modelo += pl.lpSum(tiempo[(p, t)] * x[p][t] for t in tareas) <= disponibilidad[p]

    # Compatibilidad (si tiempo = 0, no se puede asignar)
    for p in programadores:
        for t in tareas:
            if compatibilidad[(p, t)] == 0:
                modelo += x[p][t] == 0

    estado = modelo.solve()
    return modelo, x, tiempo, programadores, tareas


# =====================================================
# INTERFAZ EN STREAMLIT 
# =====================================================

# Encabezado
st.markdown("""
<h1 style='text-align:center;'>
🛠️ Optimización de Asignación de Tareas
</h1>
<p style='text-align:center; font-size:16px;'>
Proyecto Integrador – Investigación de Operaciones
</p>
""", unsafe_allow_html=True)

st.markdown("---")

st.sidebar.header("⚙️ Configuración")
st.sidebar.write("Puedes editar programadores, disponibilidades y tiempos.")
st.sidebar.write("Si un tiempo es 0, significa que el programador NO puede realizar esa tarea.")

# Crear DataFrames base
df_prog_base, df_tiempos_base = crear_dataframes_desde_ejemplo()

st.markdown("### 🧑‍💻 Programadores y su disponibilidad")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Programadores")
    df_prog = st.data_editor(
        df_prog_base,
        key="df_prog_editor",
        num_rows="dynamic"
    )

with col2:
    st.subheader("Tiempos estimados (horas)")
    df_tiempos = st.data_editor(
        df_tiempos_base,
        key="df_tiempos_editor",
        num_rows="dynamic"
    )

st.markdown("---")

# Botón para ejecutar el modelo
centrar = st.columns([1, 1, 1])
with centrar[1]:
    ejecutar = st.button("🚀 Resolver modelo de asignación")

# Resultados
if ejecutar:
    try:
        modelo, x, tiempo, programadores, tareas = resolver_asignacion(df_prog, df_tiempos)
    except Exception as e:
        st.error(f"Ocurrió un error al resolver el modelo: {e}")
    else:
        estado = pl.LpStatus[modelo.status]

        st.markdown("### 📌 Estado del modelo")
        st.write(f"**Estado:** {estado}")

        if estado != "Optimal":
            st.warning("No fue posible obtener una solución óptima con los datos proporcionados.")
        else:
            # Tiempo total
            tiempo_total = pl.value(modelo.objective)

            st.markdown("""
            <div style="
                background:#f2f2f2;
                padding:15px;
                border-radius:10px;
                border-left: 5px solid #4a6cf7;">
                <h3>⏱️ Tiempo total óptimo del proyecto</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<h2 style='color:#4a6cf7;'>{tiempo_total:.2f} horas</h2>", unsafe_allow_html=True)

            # Asignación óptima
            filas = []
            cargas = {p: 0 for p in programadores}

            for p in programadores:
                for t in tareas:
                    if x[p][t].value() == 1:
                        filas.append({
                            "Programador": p,
                            "Tarea": t,
                            "Tiempo (h)": tiempo[(p, t)]
                        })
                        cargas[p] += tiempo[(p, t)]

            df_resultado = pd.DataFrame(filas)

            st.markdown("### 📋 Asignación óptima de tareas")
            st.dataframe(df_resultado, use_container_width=True)

            # Gráfico de carga
            st.markdown("### 📊 Carga de trabajo por programador")
            df_cargas = pd.DataFrame({
                "Programador": list(cargas.keys()),
                "Horas asignadas": list(cargas.values())
            })
            st.bar_chart(df_cargas.set_index("Programador"))

            # Matriz binaria
            st.markdown("### 🧮 Matriz binaria de decisión (x[p][t])")

            matriz = []
            for p in programadores:
                fila = {"Programador": p}
                for t in tareas:
                    fila[t] = int(x[p][t].value())
                matriz.append(fila)

            st.dataframe(pd.DataFrame(matriz), use_container_width=True)
else:
    st.info("Edita los datos si lo deseas y luego presiona el botón para resolver el modelo.")

st.markdown("---")

st.markdown("""
<p style='text-align:center; color:gray; margin-top:20px;'>
Proyecto IO – 2025 · Asignación de tareas en un equipo de desarrollo de software
</p>
""", unsafe_allow_html=True)
