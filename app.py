import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
from PIL import Image

# Forcer l'affichage à s'adapter parfaitement aux écrans de smartphones
st.set_page_config(page_title="Interventions", layout="centered")

st.title("🚒 Application Intervention")

# Connexion sécurisée au Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.subheader("📸 1. Capture de la fiche")
# Sur téléphone, ce bouton propose directement d'ouvrir l'appareil photo du mobile
uploaded_file = st.file_uploader("Prendre la photo du rapport", type=["jpg", "jpeg", "png"])

# Variables par défaut
num_inter = ""
date_inter = datetime.date.today()
nature_inter = ""
commune_inter = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Photo enregistrée", use_container_width=True)
    
    with st.spinner("IA : Extraction des données en cours..."):
        # Simulation de l'OCR intelligent
        num_inter = "INT-2026-953"
        date_inter = datetime.date(2026, 6, 27)
        nature_inter = "Secours à personne - Malaise"
        commune_inter = "Créon"  # Nouvelle variable extraite
    st.success("Extraction réussie !")

# --- Formulaire adapté aux pouces sur smartphone ---
st.markdown("### 📝 Vérification des données")
num_inter_input = st.text_input("N° Intervention", value=num_inter)
date_inter_input = st.date_input("Date", value=date_inter)
commune_input = st.text_input("Commune", value=commune_inter) # Ajout du champ commune
nature_inter_input = st.text_area("Nature de l'intervention", value=nature_inter)

st.markdown("---")

st.markdown("### ⏱️ 2. Saisie des Horaires")
# Sur mobile, alignement vertical simple pour faciliter la saisie au clavier
heure_depart = st.text_input("Heure de Départ", placeholder="HH:MM")
heure_sllx = st.text_input("Sur les lieux (Sllx)", placeholder="HH:MM")
heure_retour = st.text_input("Heure de Retour", placeholder="HH:MM")
heure_rentree = st.text_input("Heure de Rentrée", placeholder="HH:MM")

st.markdown("---")

# Bouton large, facile à cliquer sur un écran tactile
if st.button("💾 ENREGISTRER LE RAPPORT", type="primary", use_container_width=True):
    if not num_inter_input or not commune_input:
        st.error("Le numéro d'intervention et la commune sont obligatoires.")
    else:
        with st.spinner("Envoi au fichier central..."):
            # Préparation de la ligne pour le tableur
            nouvelle_ligne = pd.DataFrame([{
                "N° Intervention": num_inter_input,
                "Date": date_inter_input.strftime("%d/%m/%Y"),
                "Commune": commune_input, # Ajout dans la base Google Sheets
                "Nature": nature_inter_input,
                "Départ": heure_depart,
                "Sllx": heure_sllx,
                "Retour": heure_retour,
                "Rentrée": heure_rentree
            }])
            
            # Lecture et mise à jour
            donnees_existantes = conn.read()
            donnees_mises_a_jour = pd.concat([donnees_existantes, nouvelle_ligne], ignore_index=True)
            conn.update(data=donnees_mises_a_jour)
            
            st.balloons()
            st.success("Rapport envoyé sur Google Sheets !")
