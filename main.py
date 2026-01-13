# main.py


import streamlit as st
import os
import sys
# --- Configuration de la clé API ---
from dotenv import load_dotenv
import utils.config as config

# Configuration de la page
st.set_page_config(
    page_title="Parenti - Lawyer Bot",
    layout="wide",
    page_icon="💬 Assistant local"
)

# Définir le titre principal
st.title("Chatbot")
st.caption("Chatbot basé sur RAG")

# --- Vérification des chemins et imports internes ---

# Ajout du répertoire courant au chemin d'importation
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Vérification des sous-modules
expected_folders = ["ingestion", "llm", "storage", "utils"]
missing = [f for f in expected_folders if not os.path.isdir(os.path.join(BASE_DIR, f))]

if missing:
    st.error(f"Les dossiers suivants sont manquants : {', '.join(missing)}")
else:
    st.success("✅ Tous les modules internes sont présents et détectés.")

# --- Diagnostic rapide de l'environnement ---
with st.expander(" Diagnostic de l'environnement"):
    st.write("Répertoire courant :", BASE_DIR)
    st.write("Contenu du dossier :", os.listdir(BASE_DIR))

    try:
        import langchain
        import chromadb
        import openai
        st.write("✅ Librairies principales disponibles.")
    except Exception as e:
        st.warning(f"⚠️ Une dépendance semble manquante : {e}")

# --- Navigation Streamlit ---
st.markdown("### Navigation")
st.write("Sélectionne une page dans le menu latéral à gauche :")
st.markdown("""
1. **chat** - Pose une question et obtiens une réponse à partir de la documentation interne !
2. **docs manager** — Importe, supprime et vectorise les fichiers utilisés pour le RAG.
""")

# --- Message d'accueil ---
st.divider()
st.write(
    "Ce prototype vise à démontrer une intégration complète de RAG (Retrieval-Augmented Generation) "
    "dans une interface Streamlit sécurisée. Le modèle s'appuiera uniquement sur les documents internes "
    "uploadés via la page *Gestion des documents*."
)



st.subheader("🔐 Configuration de la clé API OpenAI")

# Charger une clé déjà existante si le fichier .env est présent
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

current_key = os.getenv("OPENAI_API_KEY", "")

with st.form("api_key_form"):
    api_key_input = st.text_input(
        "Saisis ta clé OpenAI (sk-...)",
        type="password",
        value=current_key,
        placeholder="sk-...",
        help="Ta clé est stockée localement dans un fichier .env"
    )
    submitted = st.form_submit_button("Enregistrer")

    if submitted:
        try:
            # Créer ou mettre à jour le fichier .env
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f"OPENAI_API_KEY={api_key_input.strip()}\n")
            st.success("✅ Clé OpenAI enregistrée avec succès.")
            st.rerun()
        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement de la clé : {e}")

# Afficher l'état actuel
if current_key:
    st.info("Une clé OpenAI est actuellement configurée.")
else:
    st.warning("Aucune clé API trouvée. Saisis ta clé pour activer le modèle.")
