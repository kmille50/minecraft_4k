import streamlit as st
import random

st.set_page_config(page_title="Survie Minecraft", page_icon="🧱")

# Initialisation des stats
if "health" not in st.session_state:
    st.session_state.health = 100
    st.session_state.inventory = []
    st.session_state.day = 1
    st.session_state.game_over = False

st.title("🧱 Survie Minecraft")
st.write("Prends des décisions pour survivre le plus longtemps possible !")

# Affichage des stats
st.write(f"❤️ Santé : {st.session_state.health}")
st.write(f"📅 Jour : {st.session_state.day}")
st.write(f"🎒 Inventaire : {', '.join(st.session_state.inventory) if st.session_state.inventory else 'Vide'}")

if st.session_state.game_over:
    st.error("💀 Game Over !")
    if st.button("🔄 Rejouer"):
        st.session_state.health = 100
        st.session_state.inventory = []
        st.session_state.day = 1
        st.session_state.game_over = False
    st.stop()

st.divider()

st.subheader("Que veux-tu faire ?")

col1, col2, col3 = st.columns(3)

# ACTION 1 : Récolter
if col1.button("🌲 Récolter du bois"):
    st.session_state.inventory.append("Bois")
    st.success("Tu as récupéré du bois !")

# ACTION 2 : Explorer
if col2.button("🧭 Explorer"):
    event = random.choice(["trésor", "monstre", "rien"])
    
    if event == "trésor":
        st.session_state.inventory.append("Fer")
        st.success("Tu trouves du fer !")
        
    elif event == "monstre":
        damage = random.randint(10, 30)
        st.session_state.health -= damage
        st.warning(f"Un zombie t'attaque ! -{damage} ❤️")
        
    else:
        st.info("Rien d'intéressant ici...")

# ACTION 3 : Se reposer
if col3.button("🔥 Se reposer"):
    heal = random.randint(5, 20)
    st.session_state.health += heal
    st.success(f"Tu récupères {heal} ❤️")

# Passage au jour suivant
if st.button("⏭️ Passer au jour suivant"):
    st.session_state.day += 1
    
    # Événement nocturne
    night_event = random.choice(["attaque", "calme"])
    
    if night_event == "attaque":
        damage = random.randint(5, 25)
        st.session_state.health -= damage
        st.warning(f"La nuit est dangereuse... -{damage} ❤️")
    else:
        st.success("Nuit calme 😌")

# Vérification mort
if st.session_state.health <= 0:
    st.session_state.game_over = True