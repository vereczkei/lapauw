
import streamlit as st
import json
import os
import html

# =========================================================
# ALAPBEÁLLÍTÁSOK
# =========================================================

st.set_page_config(
    page_title="Vasalósor Vezérlő",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = "vasalosor_allapot.json"

# =========================================================
# CÉGLISTA - ABC SORRENDBEN
# =========================================================

CEGEK = [
    "1.0",
    "2.0",
    "Airport",
    "Ambassador",
    "Amberlyn",
    "Aurea",
    "BQA Apartman",
    "BQA Hotel",
    "BQA Spanyol",
    "City Home",
    "Császár",
    "Danube",
    "Flow",
    "Intercity",
    "Kimpton",
    "La Rouge",
    "Menza Futó",
    "Mika",
    "Netizen",
    "Noble",
    "President",
    "Stories",
    "Wonder",
]

# Stories és La Rouge esetében csak lepedő

CSAK_LEPEDO = [
    "Stories",
    "La Rouge",
]

DEFAULT_LISTA = []

for ceg in CEGEK:
    if ceg in CSAK_LEPEDO:
        DEFAULT_LISTA.append({
            "ceg": ceg,
            "textil": "lepedő"
        })
    else:
        DEFAULT_LISTA.append({
            "ceg": ceg,
            "textil": "paplan"
        })

        DEFAULT_LISTA.append({
            "ceg": ceg,
            "textil": "lepedő"
        })

# =========================================================
# ÁLLAPOT BETÖLTÉSE ÉS MENTÉSE
# =========================================================

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


def load_state():

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)

            old_lista = state.get("lista", [])
            old_index = state.get("index", 0)

            if not isinstance(old_lista, list):
                old_lista = []

            if not isinstance(old_index, int):
                old_index = 0

            # Régi aktuális munka megőrzése,
            # ha az új listában is szerepel.

            aktualis = None

            if 0 <= old_index < len(old_lista):
                aktualis = old_lista[old_index]

            uj_index = 0

            if aktualis in DEFAULT_LISTA:
                uj_index = DEFAULT_LISTA.index(aktualis)

            state["lista"] = DEFAULT_LISTA.copy()
            state["index"] = uj_index

            state.setdefault("utolso_darab", False)
            state.setdefault("elvalasztott_ceg", "")

            save_state(state)

            return state

        except (json.JSONDecodeError, OSError, TypeError):
            pass

    state = {
        "index": 0,
        "utolso_darab": False,
        "elvalasztott_ceg": "",
        "lista": DEFAULT_LISTA.copy()
    }

    save_state(state)

    return state


# =========================================================
# MODERN MEGJELENÉS
# =========================================================

st.markdown("""
<style>

/* ALAP HÁTTÉR */

.stApp {
    background:
        radial-gradient(
            ellipse at top,
            #263440 0%,
            #151d25 48%,
            #10151b 100%
        );

    color: #f1f5f9;
}

/* FELSŐ TERÜLET */

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* OLDALCÍM */

.main-title {
    text-align: center;
    font-size: clamp(27px, 4vw, 42px);
    font-weight: 900;
    letter-spacing: 2px;
    color: #f8fafc;
    margin-bottom: 5px;
}

.main-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
    letter-spacing: 3px;
    margin-bottom: 25px;
}

/* KÖZÖS LOGÓ */

.logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
}

.logo-box {
    width: 65px;
    height: 65px;
    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        145deg,
        #d9a441,
        #8e641b
    );

    border: 2px solid #f8d477;
    border-radius: 17px;

    color: #111820;
    font-size: 27px;
    font-weight: 1000;

    box-shadow: 0 5px 25px rgba(218,164,65,0.25);
}

/* KÁRTYÁK */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 17px;
    padding: 15px;
}

/* AKTUÁLIS MUNKA */

.section-label {
    color: #4ade80;
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 1px;
    text-align: center;
    margin-bottom: 14px;
}

.current-work {
    background: linear-gradient(
        135deg,
        #123d2b,
        #175239
    );

    border: 2px solid #36b879;
    border-radius: 14px;

    padding: 22px 12px;

    color: #ffffff;
    text-align: center;

    font-size: clamp(23px, 3vw, 34px);
    font-weight: 900;

    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
}

/* GOMBOK */

.stButton > button {
    min-height: 65px;

    border-radius: 13px;
    border: 1px solid #536272;

    background: linear-gradient(
        135deg,
        #344454,
        #253341
    );

    color: white;

    font-size: 17px;
    font-weight: 800;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #e8b94f;
    color: #ffd76a;
    transform: translateY(-2px);
}

/* ELSŐDLEGES GOMB */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #b78a2f,
        #896018
    );

    color: #ffffff;
    border: 2px solid #f1cc72;

    font-weight: 900;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(
        135deg,
        #d2a640,
        #a57924
    );

    color: #ffffff;
}

/* LEGÖRDÜLŐ MENÜ */

div[data-baseweb="select"] > div {
    background-color: #202d39;
    border: 2px solid #536779;
    border-radius: 12px;
    min-height: 60px;
    color: white;
}

div[data-baseweb="select"] span {
    font-size: 20px;
    font-weight: 800;
}

/* FIGYELMEZTETÉS */

@keyframes villog {
    0% {
        opacity: 1;
        border-color: #ffd700;
    }

    50% {
        opacity: 0.55;
        border-color: #ff8c00;
    }

    100% {
        opacity: 1;
        border-color: #ffd700;
    }
}

.figyelem-villog {
    animation: villog 1s infinite;

    background: linear-gradient(
        135deg,
        #471717,
        #230d0d
    );

    color: #ffd700;

    border: 4px solid #ffd700;
    border-radius: 17px;

    padding: 25px 12px;

    text-align: center;

    font-size: clamp(20px, 3vw, 30px);
    font-weight: 1000;

    box-shadow: 0 0 25px rgba(255,180,0,0.25);

    margin: 10px 0;
}

/* ELVÁLASZTÓ CÉGNEVE */

.ceg-nev {
    background: linear-gradient(
        135deg,
        #263747,
        #192630
    );

    color: #ffd76a;

    border: 2px solid #d5a33c;
    border-radius: 13px;

    padding: 20px 10px;

    text-align: center;

    font-size: clamp(22px, 3vw, 30px);
    font-weight: 900;

    margin-top: 15px;
}

/* NORMÁL ÁLLAPOT */

.normal-status {
    background: linear-gradient(
        135deg,
        #173e2a,
        #10291d
    );

    border: 2px solid #299b59;
    border-radius: 13px;

    padding: 23px 10px;

    text-align: center;

    color: #64e99a;

    font-size: 20px;
    font-weight: 900;
}

/* ALSÓ INFORMÁCIÓ */

.footer-info {
    text-align: center;
    color: #718096;
    font-size: 12px;
    margin-top: 25px;
}

/* MOBIL ÉS TABLET */

@media (max-width: 768px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
        padding-top: 1rem;
    }

    .stButton > button {
        min-height: 75px;
        font-size: 16px;
    }

    .figyelem-villog {
        padding: 22px 8px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# NÉZET KIVÁLASZTÁSA
# =========================================================

params = st.query_params

nezet = params.get("view", "hatul")

if nezet not in ["elol", "hatul"]:
    nezet = "hatul"


# =========================================================
# FŐ VEZÉRLŐFELÜLET
# =========================================================

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
        f"{item['ceg']} – {item['textil'].capitalize()}"
        for item in lista
    ]

    # =====================================================
    # FEJLÉC
    # =====================================================

    st.markdown("""
    <div class="logo-container">
        <div class="logo-box">VS</div>
    </div>

    <div class="main-title">
        VASALÓSOR VEZÉRLŐ
    </div>

    <div class="main-subtitle">
        INDUSTRIAL CONTROL SYSTEM
    </div>
    """, unsafe_allow_html=True)

    if nezet == "elol":

        st.caption("🟢 ELÜLSŐ KEZELŐÁLLOMÁS")

    else:

        st.caption("🔵 HÁTSÓ ELLENŐRZŐ ÁLLOMÁS")

    # =====================================================
    # AKTUÁLIS MUNKA
    # =====================================================

    with st.container(border=True):

        st.markdown(
            '<div class="section-label">'
            '🟢 AKTUÁLIS MUNKA'
            '</div>',
            unsafe_allow_html=True
        )

        if nezet == "elol":

            valasztott = st.selectbox(
                "Aktuális munka",
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
                f'<div class="current-work">'
                f'{html.escape(aktualis_nev)}'
                f'</div>',
                unsafe_allow_html=True
            )

    st.write("")

    col1, col2 = st.columns([1.5, 1])

    # =====================================================
    # ELÜLSŐ KEZELŐ
    # =====================================================

    with col1:

        if nezet == "elol":

            if not utolso:

                if st.button(
                    "🛑 UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE",
                    use_container_width=True,
                    type="primary"
                ):

                    current_state["elvalasztott_ceg"] = (
                        ceg_opciok[current_state["index"]]
                    )

                    current_state["utolso_darab"] = True

                    save_state(current_state)

                    st.rerun()

            else:

                st.markdown("""
                <div class="figyelem-villog">

                    ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE

                    <div style="
                        font-size:16px;
                        margin-top:12px;
                        color:white;
                        font-weight:600;
                    ">
                        Várakozás a hátsó nyugtázásra...
                    </div>

                </div>
                """, unsafe_allow_html=True)

                nev = html.escape(
                    current_state.get("elvalasztott_ceg", "")
                )

                st.markdown(
                    f'<div class="ceg-nev">'
                    f'📦 {nev}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # =====================================================
    # HÁTSÓ KEZELŐ
    # =====================================================

    with col2:

        if nezet == "hatul":

            if utolso:

                st.markdown("""
                <div class="figyelem-villog">

                    ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BENN!

                    <div style="
                        font-size:16px;
                        margin-top:12px;
                        color:white;
                        font-weight:600;
                    ">
                        Kérlek vedd ki és nyugtázd!
                    </div>

                </div>
                """, unsafe_allow_html=True)

                nev = html.escape(
                    current_state.get("elvalasztott_ceg", "")
                )

                st.markdown(
                    f'<div class="ceg-nev">'
                    f'📦 {nev}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # HANGJELZÉS

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

                    current_state["utolso_darab"] = False

                    save_state(current_state)

                    st.rerun()

            else:

                st.markdown("""
                <div class="normal-status">

                    🟢 NORMÁL MENETBEN

                    <div style="
                        font-size:13px;
                        margin-top:7px;
                        color:#a7d9b9;
                    ">
                        Nincs aktív riasztás
                    </div>

                </div>
                """, unsafe_allow_html=True)

    # =====================================================
    # ALSÓ INFORMÁCIÓ
    # =====================================================

    st.markdown("---")

    st.markdown(
        f"""
        <div class="footer-info">

            VASALÓSOR VEZÉRLŐ SYSTEM<br>

            PARTNEREK: {len(CEGEK)}
            &nbsp; | &nbsp;
            VÁLASZTHATÓ MUNKÁK: {len(DEFAULT_LISTA)}
            <br><br>

            {'ELÜLSŐ KEZELŐÁLLOMÁS' if nezet == 'elol' else 'HÁTSÓ ELLENŐRZŐ ÁLLOMÁS'}

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INDÍTÁS
# =========================================================

futo_nezet()
