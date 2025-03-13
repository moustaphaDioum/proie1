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
    return sol.t, sol.y[0], sol.y[1]

# === Interface Streamlit ===
st.title("Simulation Lotka-Volterra 🦊🐰")

# === Organisation en colonnes ===
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Modèle mathématique")
    st.latex(r"""
    \begin{cases}
    \frac{dx}{dt} = \alpha x - \beta xy \\ 
    \frac{dy}{dt} = \delta xy - \gamma y
    \end{cases}
    """)

    st.subheader("Paramètres de simulation")
    alpha = st.slider("Taux de croissance des proies (α)", 0.0, 1.0, 0.4, 0.01)
    beta = st.slider("Taux de prédation (β)", 0.0, 0.1, 0.02, 0.001)
    delta = st.slider("Conversion des proies en prédateurs (δ)", 0.0, 0.2, 0.1, 0.001)
    gamma = st.slider("Mortalité des prédateurs (γ)", 0.0, 1.0, 0.3, 0.01)

    x0 = st.number_input("Population initiale des proies", 0, 1000, 10)
    y0 = st.number_input("Population initiale des prédateurs", 0, 1000, 5)

    t_max = st.slider("Temps de simulation", 5, 100, 10)
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
            t, x, y = run_simulation(alpha, beta, delta, gamma, x0, y0, t_max, 100)

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
            ax.set_facecolor("black")  # Fond noir
            ax.title.set_color("white")  # Titre en blanc
            ax.legend()
            ax.set_title("Dynamique Lotka-Volterra")
            ax.grid()
            st.pyplot(fig)

            # === ANIMATION EN TEMPS RÉEL ===
            st.subheader("Évolution des populations 📍")

            # Création d'un espace pour mettre à jour l'affichage
            plot_spot = st.empty()

            for i in range(len(t)):
                fig_anim, ax_anim = plt.subplots(figsize=(6, 6))
                ax_anim.set_xlim(0, 10)
                ax_anim.set_ylim(0, 10)
                ax_anim.set_xticks([])
                ax_anim.set_yticks([])
            
                # Fond noir
                ax_anim.set_facecolor("black")
            
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
                legend = ax_anim.legend(facecolor="black", edgecolor="white", fontsize=10)
                for text in legend.get_texts():
                    text.set_color("white")  # Changer la couleur du texte de la légende en blanc
            
                # Affichage dans Streamlit
                plot_spot.pyplot(fig_anim)
                plt.close(fig_anim)  # Évite les fuites de mémoire
            
                time.sleep(0.3)  # Pause pour ralentir l'animation