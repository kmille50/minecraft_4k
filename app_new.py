import random
import streamlit as st

# ---------------------------------------------------------------------------
# 🎮 MINI-CRAFT — un petit bac à sable inspiré de Minecraft, fait avec Streamlit
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Mini-Craft 🧱", page_icon="🧱", layout="wide")

TAILLE_GRILLE = 10

BLOCS = {
    "Herbe": "🟩",
    "Terre": "🟫",
    "Pierre": "⬜",
    "Bois": "🟧",
    "Eau": "🟦",
    "Lave": "🟥",
    "Diamant": "💎",
    "Or": "🟨",
    "TNT": "🧨",
    "Vide": "⬛",
}

MOBS = ["🐷", "🐔", "🐄", "🐑", "🧟", "🕷️", "🐺", "🐢", "🐝"]

ACHIEVEMENTS_POSSIBLES = {
    "premier_bloc": "🏆 Premier bloc posé !",
    "dix_blocs": "🏆 Bâtisseur en herbe (10 blocs posés) !",
    "cinquante_blocs": "🏆 Maître bâtisseur (50 blocs posés) !",
    "diamant_trouve": "🏆 Chanceux ! Un diamant posé !",
    "explosion": "🏆 Boum ! Première explosion de TNT !",
    "mob_invoque": "🏆 Dresseur de mobs !",
    "monde_efface": "🏆 On recommence à zéro !",
}


# ---------------------------------------------------------------------------
# Initialisation de l'état du jeu
# ---------------------------------------------------------------------------
def init_etat():
    if "grille" not in st.session_state:
        st.session_state.grille = [["Vide" for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
    if "bloc_selectionne" not in st.session_state:
        st.session_state.bloc_selectionne = "Herbe"
    if "points" not in st.session_state:
        st.session_state.points = 0
    if "blocs_poses" not in st.session_state:
        st.session_state.blocs_poses = 0
    if "achievements" not in st.session_state:
        st.session_state.achievements = set()
    if "jour" not in st.session_state:
        st.session_state.jour = True
    if "message" not in st.session_state:
        st.session_state.message = "Bienvenue dans ton monde Mini-Craft ! Choisis un bloc et clique dans la grille 👇"
    if "inventaire" not in st.session_state:
        st.session_state.inventaire = []


def debloquer_achievement(cle):
    if cle not in st.session_state.achievements:
        st.session_state.achievements.add(cle)
        st.balloons()
        st.session_state.message = ACHIEVEMENTS_POSSIBLES[cle]


def poser_bloc(x, y):
    ancien = st.session_state.grille[x][y]
    nouveau = st.session_state.bloc_selectionne

    if nouveau == "TNT" and ancien != "Vide":
        # Explosion rigolote : ça vide une petite zone autour du clic
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < TAILLE_GRILLE and 0 <= ny < TAILLE_GRILLE:
                    st.session_state.grille[nx][ny] = "Vide"
        st.session_state.message = "💥 BOUM ! La TNT a tout fait sauter autour !"
        st.session_state.points += 5
        debloquer_achievement("explosion")
        return

    st.session_state.grille[x][y] = nouveau
    st.session_state.blocs_poses += 1
    st.session_state.points += 1

    if st.session_state.blocs_poses == 1:
        debloquer_achievement("premier_bloc")
    if st.session_state.blocs_poses == 10:
        debloquer_achievement("dix_blocs")
    if st.session_state.blocs_poses == 50:
        debloquer_achievement("cinquante_blocs")
    if nouveau == "Diamant":
        st.session_state.points += 10
        debloquer_achievement("diamant_trouve")
        st.session_state.message = "💎 Superbe ! Tu as posé un diamant !"


def generer_monde_aleatoire():
    choix = ["Herbe", "Terre", "Pierre", "Bois", "Eau"]
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            st.session_state.grille[i][j] = random.choice(choix)
    # Petite pépite de diamant cachée quelque part, pour le fun
    dx, dy = random.randint(0, TAILLE_GRILLE - 1), random.randint(0, TAILLE_GRILLE - 1)
    st.session_state.grille[dx][dy] = "Diamant"
    st.session_state.message = "🌍 Un nouveau monde vient d'apparaître ! Un diamant s'y cache quelque part 👀"


def effacer_monde():
    st.session_state.grille = [["Vide" for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
    st.session_state.message = "🧹 Le monde a été effacé, table rase !"
    debloquer_achievement("monde_efface")


def invoquer_mob():
    x, y = random.randint(0, TAILLE_GRILLE - 1), random.randint(0, TAILLE_GRILLE - 1)
    mob = random.choice(MOBS)
    st.session_state.message = f"{mob} Un mob sauvage est apparu en case ({x}, {y}) !"
    st.session_state.inventaire.append(mob)
    debloquer_achievement("mob_invoque")


def miner_bloc_chance():
    """Petit mini-jeu de minage avec une chance de trouver un trésor."""
    resultat = random.choices(
        ["Rien du tout...", "🪨 Un peu de pierre", "🟨 Une pépite d'or !", "💎 UN DIAMANT !!!"],
        weights=[40, 35, 20, 5],
        k=1,
    )[0]
    st.session_state.message = f"⛏️ Tu creuses... {resultat}"
    if "DIAMANT" in resultat:
        st.session_state.points += 15
        debloquer_achievement("diamant_trouve")
    elif "or" in resultat:
        st.session_state.points += 5


def crafter():
    """Mini crafting rigolo : combine 2 objets au hasard en un objet surprise."""
    recettes = [
        "🗡️ Épée en diamant", "🛡️ Bouclier solide", "🏠 Une petite maison",
        "🚀 Une fusée (why not)", "🐴 Une selle de cheval", "🍞 Du pain magique",
        "🎣 Une canne à pêche dorée", "🧪 Une potion mystère",
    ]
    objet = random.choice(recettes)
    st.session_state.inventaire.append(objet)
    st.session_state.message = f"🔨 Tu as crafté : {objet} !"


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------
init_etat()

if st.session_state.jour:
    fond, texte = "#87CEEB", "#1b1b1b"
else:
    fond, texte = "#0b1026", "#f0f0f0"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {fond};
        color: {texte};
    }}
    div.stButton > button {{
        font-size: 26px;
        height: 42px;
        width: 42px;
        padding: 0px;
        border-radius: 6px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧱 Mini-Craft — le bac à sable pour petits bâtisseurs")
st.info(st.session_state.message)

col_grille, col_side = st.columns([3, 1])

with col_side:
    st.subheader("🎒 Choisis ton bloc")
    for nom, emoji in BLOCS.items():
        if st.button(f"{emoji} {nom}", key=f"choix_{nom}", use_container_width=True):
            st.session_state.bloc_selectionne = nom
    st.success(f"Bloc actuel : {BLOCS[st.session_state.bloc_selectionne]} {st.session_state.bloc_selectionne}")

    st.divider()
    st.subheader("✨ Actions rigolotes")

    if st.button("🌍 Monde aléatoire", use_container_width=True):
        generer_monde_aleatoire()
    if st.button("🧹 Effacer le monde", use_container_width=True):
        effacer_monde()
    if st.button("🌗 Jour / Nuit", use_container_width=True):
        st.session_state.jour = not st.session_state.jour
        st.session_state.message = "☀️ C'est le jour !" if st.session_state.jour else "🌙 La nuit tombe..."
    if st.button("👾 Invoquer un mob", use_container_width=True):
        invoquer_mob()
    if st.button("⛏️ Miner un bloc (chance)", use_container_width=True):
        miner_bloc_chance()
    if st.button("🔨 Crafter un objet surprise", use_container_width=True):
        crafter()

    st.divider()
    st.subheader("🏅 Score")
    st.metric("Points", st.session_state.points)
    st.metric("Blocs posés", st.session_state.blocs_poses)

    if st.session_state.inventaire:
        st.subheader("🎒 Inventaire")
        st.write(" ".join(st.session_state.inventaire[-15:]))

    if st.session_state.achievements:
        st.subheader("🏆 Succès débloqués")
        for cle in st.session_state.achievements:
            st.write(ACHIEVEMENTS_POSSIBLES[cle])

with col_grille:
    st.subheader("🗺️ Ton monde")
    for i in range(TAILLE_GRILLE):
        cols = st.columns(TAILLE_GRILLE, gap="small")
        for j in range(TAILLE_GRILLE):
            emoji = BLOCS[st.session_state.grille[i][j]]
            with cols[j]:
                if st.button(emoji, key=f"case_{i}_{j}"):
                    poser_bloc(i, j)

st.caption("Astuce : pose de la TNT 🧨 sur une case déjà construite pour la faire exploser !")
