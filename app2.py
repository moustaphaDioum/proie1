import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.integrate import solve_ivp
import time  

# === Modèle Lotka-Volterra ===
def lotka_volterra(t, z, alpha, beta, delta, gamma):
    x, y = z
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y

    return [dxdt, dydt]


# === Fonction pour exécuter la simulation ===
def run_simulation(alpha, beta, delta, gamma, x0, y0, t_max, points):
    t_span = (0, t_max)
    t_eval = np.linspace(*t_span, points)
    sol = solve_ivp(lotka_volterra, t_span, [x0, y0], args=(alpha, beta, delta, gamma), t_eval=t_eval)

    # Récupération des solutions
    t, x, y = sol.t, sol.y[0], sol.y[1]

    # Vérification et mise à jour des populations
    for i in range(len(t)):
        if x[i] < 1:  # Si les proies descendent sous 1
            x[i:] = 0  # Elles restent nulles
            y[i:] = y[i] * np.exp(-gamma * (t[i:] - t[i]))  # Décroissance exponentielle des prédateurs
            break  # On arrête la boucle car l'évolution est forcée

        if y[i] < 1:  # Si les prédateurs descendent sous 1
            y[i:] = 0  # Ils restent nuls
            x[i:] = x[i] * np.exp(alpha * (t[i:] - t[i]))  # Croissance exponentielle des proies sans prédateurs
            break  # On arrête la boucle

    return t, x, y


# === Interface Streamlit ===
st.markdown("""
    <style>
        .stApp {
            background-color: #e0e0e0;
        }
        .stMarkdown, .stText, .stSubheader, .stTitle , .stSlider{
            color: #8e44ad;  /* Couleur de tous les textes */
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color: #4CAF50;">Simulation Modèle Proie-Prédateur 🦊🐰</h1>', unsafe_allow_html=True)


# === Organisation en colonnes ===
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<p style="color: #8e44ad;">Modèle mathématique</p>', unsafe_allow_html=True)
    st.latex(r"""
    \begin{cases}
    \frac{dx}{dt} = \alpha x - \beta xy \\ 
    \frac{dy}{dt} = \delta xy - \gamma y
    \end{cases}
    """)

    st.markdown('<p style="color: #8e44ad;">Paramètres de simulation</p>', unsafe_allow_html=True)

    # Texte personnalisé avec couleur #8e44ad
    st.markdown('<p style="color: #8e44ad;">Taux de croissance des proies (α)</p>', unsafe_allow_html=True)
    alpha = st.slider(" ", 0.0, 1.0, 0.33, 0.05)

    # Texte personnalisé avec couleur #8e44ad
    st.markdown('<p style="color: #8e44ad;">Taux de prédation (β)</p>', unsafe_allow_html=True)
    beta = st.slider(" ", 0.0, 1.0, 0.02, 0.04)
    
    st.markdown('<p style="color: #8e44ad;">Conversion des proies en prédateurs (δ)</p>', unsafe_allow_html=True)
    delta = st.slider(" ", 0.0, 1.0, 0.02, 0.05)
    
    st.markdown('<p style="color: #8e44ad;">Mortalité des prédateurs (γ)</p>', unsafe_allow_html=True)
    gamma = st.slider(" ", 0.0, 1.0, 0.3, 0.02)
    
    st.markdown('<p style="color: #8e44ad;">Population initiale des proies</p>', unsafe_allow_html=True)
    x0 = st.number_input(" ", 0, 1000, 100)
    
    st.markdown('<p style="color: #8e44ad;">Population initiale des prédateurs</p>', unsafe_allow_html=True)
    y0 = st.number_input(" ", 0, 1000, 20)
    
    st.markdown('<p style="color: #8e44ad;">Temps de simulation</p>', unsafe_allow_html=True)
    t_max = st.slider(" ", 5, 100, 10)

   # points = st.slider("Nombre de points", 10, 100, 30)

    # Bouton pour lancer la simulation
    run_simulation_btn = st.button("Simuler 🚀")

with col2:
    if run_simulation_btn:
        with st.spinner("Simulation en cours... ⏳"):
            # Réinitialisation des valeurs
            st.session_state.x_values = [x0]  # Remet les proies à leur valeur initiale
            st.session_state.y_values = [y0]  # Remet les prédateurs à leur valeur initiale

            # Exécute la simulation
            t, x, y = run_simulation(alpha, beta, delta, gamma, x0, y0, t_max, 200)

            # Stocke les nouvelles valeurs
            st.session_state.x_values = x.copy()
            st.session_state.y_values = y.copy()

            st.success("Simulation terminée ✅")

            # Affichage du graphique des populations (courbes)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(t, x, label="Proies (Lapins)", color="blue")
            ax.plot(t, y, label="Prédateurs (Renards)", color="red")
            ax.set_xlabel("Temps")
            ax.set_ylabel("Population")
            ax.set_facecolor("white")  # Fond noir
            ax.title.set_color("black")  # Titre en blanc
            ax.legend()
            ax.set_title("Dynamique Lotka-Volterra")
            ax.grid()
            st.pyplot(fig)

            # === ANIMATION EN TEMPS RÉEL ===
            st.markdown('<p style="background-color: #8e44ad; padding: 10px; color: white; font-size: 20px;">Évolution des populations 📍</p>', unsafe_allow_html=True)

            # Création d'un espace pour mettre à jour l'affichage
            plot_spot = st.empty()

            for i in range(len(t)):
                fig_anim, ax_anim = plt.subplots(figsize=(6, 6))
                ax_anim.set_xlim(0, 10)
                ax_anim.set_ylim(0, 10)
                ax_anim.set_xticks([])
                ax_anim.set_yticks([])

                # Fond noir
                ax_anim.set_facecolor("#D3D3D3")

                # Nombre réel d'individus (limité à 500 pour éviter un affichage trop dense)
                n_lapins = min(500, max(0, round(st.session_state.x_values[i])))
                n_renards = min(500, max(0, round(st.session_state.y_values[i])))

                # Titre avec informations sur les populations
                ax_anim.set_title(f"Temps: {t[i]:.1f} | Lapins: {round(st.session_state.x_values[i])} | Renards: {round(st.session_state.y_values[i])}",
                                  fontsize=12, color="white")

                # Ajout des points pour représenter les populations
                ax_anim.scatter(np.random.rand(n_lapins) * 8 + 1, 
                                np.random.rand(n_lapins) * 8 + 1, 
                                color="blue", label=f"Lapins: {round(st.session_state.x_values[i])}", alpha=0.7)

                ax_anim.scatter(np.random.rand(n_renards) * 8 + 1, 
                                np.random.rand(n_renards) * 8 + 1, 
                                color="red", label=f"Renards: {round(st.session_state.y_values[i])}", alpha=0.7)

                # Ajout de la légende avec fond noir et texte en blanc
                legend = ax_anim.legend(facecolor="white", edgecolor="black", fontsize=10)
                for text in legend.get_texts():
                    text.set_color("black")  # Changer la couleur du texte de la légende en blanc

                # Affichage dans Streamlit
                plot_spot.pyplot(fig_anim)
                plt.close(fig_anim)  # Évite les fuites de mémoire

                time.sleep(0.3)  # Pause pour ralentir l'animation
