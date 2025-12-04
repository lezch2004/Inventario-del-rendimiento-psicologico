from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Inventario Psicológico Deportivo", layout="wide")

# ------------------------------------------------------
# ENCABEZADO
# ------------------------------------------------------
st.markdown("""
# 🏆 Inventario Psicológico Deportivo   
### **Metodología: Centro de Rendimiento de Tenis ANDRADE**
### **Digitalización/Aplicativo por: Luis Eduardo Zaldumbide** 
---
""")

st.write("""
Este formulario ha sido diseñado para yudarle a lograr tener una idea más clara de sus fuerzas y debilidades mentales en relación a la psicología deportiva.
Responde cada ítem con sinceridad, pensando en el aquí y en el ahora.  
Las opciones SIEMPRE son:

**Casi siempre**  
**A menudo**  
**A veces**  
**Pocas veces**  
**Casi nunca**

""")

# ------------------------------------------------------
# OPCIONES DE RESPUESTA
# ------------------------------------------------------
OPCIONES_TEXTO = [
    "Casi siempre",
    "A menudo",
    "A veces",
    "Pocas veces",
    "Casi nunca"
]

# ------------------------------------------------------
# TODAS LAS PREGUNTAS COMPLETAS (1–20)
# invertida = True → usa escala 5→1
# ------------------------------------------------------
PREGUNTAS = {

    1:  {"texto": "Me veo más como un perdedor que como un ganador durante la competición.", "invertida": False},
    2:  {"texto": "Me enojo y frustro durante la competición.", "invertida": False},
    3:  {"texto": "Me distraigo y pierdo la concentración en la competición.", "invertida": False},
    4:  {"texto": "Antes de competir me veo rindiendo perfectamente.", "invertida": False},

    5:  {"texto": "Estoy altamente motivado para jugar lo mejor que pueda.", "invertida": True},
    6:  {"texto": "Puedo mantener una afluencia de energía positiva durante la competición.", "invertida": True},
    7:  {"texto": "Soy un pensador positivo durante la competición.", "invertida": True},
    8:  {"texto": "Creo en mí mismo como jugador.", "invertida": True},

    9:  {"texto": "Me pongo nervioso o miedoso en la competición.", "invertida": False},
    10: {"texto": "Parece que mi cabeza se acelera a 100 km por hora durante los momentos críticos de la competición.", "invertida": False},

    11: {"texto": "Practico mentalmente mis habilidades físicas.", "invertida": True},
    12: {"texto": "Las metas que me he impuesto como jugador me hacen trabajar mucho.", "invertida": True},
    13: {"texto": "Puedo disfrutar de la competición aunque se enfrente a muchos problemas difíciles.", "invertida": True},

    14: {"texto": "Me digo cosas negativas durante la competición.", "invertida": False},
    15: {"texto": "Pierdo la confianza rápidamente.", "invertida": False},
    16: {"texto": "Las equivocaciones me llevan a sentir y pensar negativamente.", "invertida": False},

    17: {"texto": "Puedo borrar emociones que interfieren y volverme a concentrar.", "invertida": True},
    18: {"texto": "La visualización de mi deporte me es fácil.", "invertida": True},
    19: {"texto": "No me tienen que empujar para jugar o entrenar fuertemente, yo me estimulo solo.", "invertida": True},

    20: {"texto": "Tiendo a sentirme aplastado emocionalmente cuando las cosas se vuelven en mi contra.", "invertida": False},
    21: {"texto": "Yo hago un cien por ciento de esfuerzo cuando juego, sin importarme nada.", "invertida": False},
    22: {"texto": "Puedo sentir en el pico máximo de mi talento y habilidad.", "invertida": False},
    23: {"texto": "Mis músculos se tensionan demasiado durante la competición.", "invertida": False},
    24: {"texto": "Mi mente se aleja del partido durante la competición.", "invertida": False},
    25: {"texto": "Yo me visualizo saliendo de situaciones difíciles previo a la competición.", "invertida": False},

    26: {"texto": "No estoy dispuesto a dar todo lo necesario para llegar a mi máximo potencial como jugador.", "invertida": False},
    27: {"texto": "Me cuesta o no me gusta entrenar con alta intensidad positiva.", "invertida": False},
    28: {"texto": "Me quedo estancado en estados emocionales negativos y se me dificulta cambiarlos a positivos por medio del control mental.", "invertida": False},
    29: {"texto": "Soy un competidor con fortaleza mental.", "invertida": True},

    30: {"texto": "Hechos incontrolables como el miedo, oponentes tramposos y malos hábitos me perturban.", "invertida": False},
    31: {"texto": "Mientras juego me encuentro pensando en equivocaciones pasadas u oportunidades perdidas.", "invertida": False},
    32: {"texto": "Uso imágenes mientras juego que me ayudan a jugar mejor.", "invertida": True},

    33: {"texto": "Me aburro y me agoto.", "invertida": False},
    34: {"texto": "Me lleno de sensaciones de desafío y me inspiro en situaciones difíciles.", "invertida": True},
    35: {"texto": "Mis entrenadores dirían que yo tengo una buena actitud.", "invertida": True},
    36: {"texto": "Yo proyecto la imagen de un luchador confiado.", "invertida": True},

    37: {"texto": "Puedo mantenerme calmado durante la competición cuando estoy confundido por problemas.", "invertida": True},
    38: {"texto": "Mi concentración se rompe fácilmente.", "invertida": False},
    39: {"texto": "Cuando me veo jugando puedo ver y sentir las cosas vívidamente.", "invertida": True},

    40: {"texto": "Me despierto por la mañana y estoy realmente excitado por jugar y entrenar.", "invertida": True},
    41: {"texto": "Al jugar este deporte me da un genuino sentido de gozo y realización.", "invertida": True},
    42: {"texto": "Yo puedo dar la vuelta a la crisis en oportunidad.", "invertida": True},

}

# ------------------------------------------------------
# CATEGORÍAS
# ------------------------------------------------------
CATEGORIAS = {
    "confianza en si mismo": [1, 8, 15, 22, 29, 36],
    "energia negativa": [2, 9, 16, 23, 30, 37],
    "control de atencion": [3, 10, 17, 24, 31, 38],
    "visual y control imaginario": [4, 11, 18, 25, 32, 39],
    "nivel motivacional": [4, 11, 18, 25, 32, 39],
    "energia positiva": [6, 13, 20, 27, 34, 41],
    "contra actitud": [7, 14, 21, 28, 35, 42],
}

# PERFIL IDEAL DE CAMPEÓN
PERFIL_IDEAL = {
    "confianza en si mismo": 29,
    "energia negativa": 27,
    "control de atencion": 29,
    "visual y control imaginario": 27,
    "nivel motivacional": 30,
    "energia positiva": 28,
    "contra actitud": 27,
}

# ------------------------------------------------------
# FORMULARIO — RESPUESTAS DEL USUARIO
# ------------------------------------------------------
st.subheader("Responde cada ítem:")

puntajes = {}  # Guarda el valor numérico REAL (1–5 o invertido 5–1)

for num, data in PREGUNTAS.items():

    # Mostrar pregunta COMPLETA
    st.markdown(f"""
    ### **{num}. {data['texto']}**
    """)

    # Radio buttons con las mismas opciones SIEMPRE
    opcion = st.radio(
        f"Pregunta {num}",
        OPCIONES_TEXTO,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Convertir la opción textual en índice 0–4
    idx = OPCIONES_TEXTO.index(opcion)

    # ------------------------------------------------------
    # LÓGICA REAL DE VALORES:
    # normal: 1→5
    # invertida: 5→1
    # ------------------------------------------------------
    if data["invertida"]:
        valor = 5 - idx   # 5,4,3,2,1
    else:
        valor = idx + 1   # 1,2,3,4,5

    puntajes[num] = valor  # Guardar el valor REAL usado en cálculos

st.write("---")

# ------------------------------------------------------
# FUNCIÓN DE INTERPRETACIÓN
# ------------------------------------------------------
def interpretar(total):
    if total >= 26:
        return "🟢 Excelente habilidad"
    elif total >= 20:
        return "🟡 Debe mejorar"
    else:
        return "🔴 Necesita atención especial"

# ------------------------------------------------------
# BOTÓN PARA CALCULAR
# ------------------------------------------------------
if st.button("Calcular resultados"):

    st.header("📊 Resultados por Categoría")

    resultados = {}
    interpretaciones = {}

    # Sumar puntajes reales por categoría
    for categoria, preguntas in CATEGORIAS.items():
        total = sum(puntajes[p] for p in preguntas)
        resultados[categoria] = total
        interpretaciones[categoria] = interpretar(total)

    # Crear DataFrame
    df = pd.DataFrame({
        "categoria": list(resultados.keys()),
        "puntaje": list(resultados.values()),
        "ideal": [PERFIL_IDEAL[c] for c in resultados.keys()]
    })

    st.dataframe(df)

    # Guardar para gráfico
    resultado_final = df


    # ------------------------------------------------------
    # GRÁFICO PRINCIPAL — PUNTOS + LÍNEAS
    # ------------------------------------------------------
    st.subheader("📈 Comparación con el Perfil de un Campeón")

    fig = px.scatter(
        resultado_final,
        x="categoria",
        y="puntaje",
        size=[20]*len(resultado_final),
        color_discrete_sequence=["#0077FF"],
        title="Perfil Psicológico vs Campeón",
    )

    # Línea del usuario
    fig.add_scatter(
        x=resultado_final["categoria"],
        y=resultado_final["puntaje"],
        mode="lines+markers",
        name="Tu perfil",
        line=dict(color="#0077FF", width=4),
        marker=dict(size=14)
    )

    # Línea del campeón
    fig.add_scatter(
        x=resultado_final["categoria"],
        y=resultado_final["ideal"],
        mode="lines+markers",
        name="Campeón",
        line=dict(color="#FF3333", width=4, dash="dash"),
        marker=dict(size=14, color="#FF3333", symbol="x")
    )

    fig.update_layout(
        height=600,
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=13),
        ),
        margin=dict(b=160, t=80),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------
    # RADAR CHART — GRÁFICO ARAÑA
    # ------------------------------------------------------
    st.subheader("🕸️ Radar Chart — Perfil Psicológico Completo")

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=resultado_final["puntaje"],
        theta=resultado_final["categoria"],
        fill='toself',
        name='Tu perfil',
        line=dict(color="#0066FF", width=3),
        marker=dict(size=10)
    ))

    radar.add_trace(go.Scatterpolar(
        r=resultado_final["ideal"],
        theta=resultado_final["categoria"],
        fill='toself',
        name='Campeón',
        line=dict(color="#FF3333", width=3, dash="dash"),
        marker=dict(size=10, color="#FF3333")
    ))

    radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[5, 35],
                tickfont=dict(size=12)
            ),
        ),
        showlegend=True,
        height=700
    )

    st.plotly_chart(radar, use_container_width=True)

    # ------------------------------------------------------
    # INTERPRETACIÓN FINAL
    # ------------------------------------------------------
    st.subheader("📝 Interpretación por Categoría")

    for categoria, msg in interpretaciones.items():
        st.markdown(f"### **{categoria.upper()}**: {msg}")
