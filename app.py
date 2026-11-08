
import streamlit as st
import json
import os

st.set_page_config(
    page_title="Vasalósor Vezérlő",
    layout="wide"
)

DATA_FILE = "vasalosor_allapot.json"


def load_state():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    state = {
        "index": 0,
        "utolso_darab": False,
        "lista": [
            {"ceg": "Mika", "textil": "paplan"},
            {"ceg": "Mika", "textil": "lepedő"},
            {"ceg": "Netizen", "textil": "paplan"},
            {"ceg": "Netizen", "textil": "lepedő"},
            {"ceg": "Wonder", "textil": "paplan"},
            {"ceg": "Wonder", "textil": "lepedő"},
        ]
    }

    save_state(state)
    return state


def save_state(state):
    temp_file = DATA_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(
            state,
            f,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temp_file, DATA_FILE)


st.markdown("""
<style>

@keyframes villog {
    0% { opacity: 1; }
    50% { opacity: 0.3; }
    100% { opacity: 1; }
}

.figyelem-villog {
    animation: villog 1s infinite;
    background-color: #000000;
    color: #FFD700;
    border: 4px solid #FFD700;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


params = st.query_params
nezet = params.get("view", "hatul")


@st.fragment(run_every=1)
def futo_nezet():

    current_state = load_state()

    lista = current_state["lista"]

    if not lista:
        st.warning("Nincs aktív feladat.")
        return

    idx = current_state["index"]

    if idx >= len(lista):
        idx = 0
        current_state["index"] = 0
        save_state(current_state)

    utolso = current_state["utolso_darab"]

    ceg_opciok = [
        f"{item['ceg']} {item['textil']}"
        for item in lista
    ]

    st.title("🏭 Vasalósor Vezérlő")

    # AKTUÁLIS MUNKA

    with st.container(border=True):

        st.markdown(
            '<p style="color:#28a745;'
            'font-size:20px;font-weight:bold;margin:0;">'
            '🟢 AKTUÁLIS MUNKA:</p>',
            unsafe_allow_html=True
        )

        if nezet == "elol":

            valasztott = st.selectbox(
                "Aktuális",
                ceg_opciok,
                index=idx,
                key="aktualis_selectbox",
                label_visibility="collapsed"
            )

            uj_idx = ceg_opciok.index(valasztott)

            if uj_idx != idx:
                current_state["index"] = uj_idx
                save_state(current_state)
                st.rerun()

        else:

            aktualis_nev = ceg_opciok[idx]

            st.markdown(
                f"""
                <div style="
                    background:#123d20;
                    color:white;
                    padding:15px;
                    border-radius:8px;
                    font-size:25px;
                    font-weight:bold;
                    text-align:center;">
                    {aktualis_nev}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("---")

    col1, col2 = st.columns([1.5, 1])

    with col1:

        # ELSŐ KEZELŐ

        if nezet == "elol":

            if not utolso:

                if st.button(
                    "🛑 UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE",
                    use_container_width=True,
                    type="primary"
                ):

                    current_state["utolso_darab"] = True
                    save_state(current_state)
                    st.rerun()

            else:

                st.markdown("""
                <div class="figyelem-villog">
                    ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE
                    <br>
                    <span style="font-size:16px;">
                    Várakozás a hátsó nyugtázásra...
                    </span>
                </div>
                """, unsafe_allow_html=True)

        # HÁTSÓ KEZELŐ

        elif nezet == "hatul":

            if utolso:

                st.markdown("""
                <div class="figyelem-villog">
                    ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BENN!
                    <br>
                    <span style="font-size:16px;">
                    Kérlek vedd ki és nyugtázd!
                    </span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <audio autoplay loop>
                    <source
                    src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"
                    type="audio/mpeg">
                </audio>
                """, unsafe_allow_html=True)

                st.write("")

                if st.button(
                    "✅ KIVÉVE / NYUGTÁZÁS",
                    use_container_width=True,
                    type="primary"
                ):

                    # CSAK A RIASZTÁST TÖRÖLJÜK!
                    # A CÉGINDEXHEZ NEM NYÚLUNK!

                    current_state["utolso_darab"] = False

                    save_state(current_state)

                    st.rerun()

            else:

                st.markdown("""
                <div style="
                    background-color:#222;
                    color:#FFD700;
                    border:2px solid #FFD700;
                    padding:15px;
                    border-radius:10px;
                    text-align:center;
                    font-weight:bold;
                    font-size:18px;">
                    🟡 Állapot: Normál menetben
                </div>
                """, unsafe_allow_html=True)


futo_nezet()
