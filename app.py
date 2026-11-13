
import streamlit as st
import json
import os
import html
from pathlib import Path
import streamlit.components.v1 as components

# ==========================================
# ALAPBEÁLLÍTÁSOK
# ==========================================

st.set_page_config(
    page_title="Vasalósor vezérlő",
    page_icon="🧺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / "vasalosor_allapot.json"
LOGO_FILE = BASE_DIR / "logo.webp"

# ==========================================
# PARTNEREK
# ==========================================

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

CSAK_LEPEDO = ["Stories", "La Rouge"]

DEFAULT_LISTA = []

for ceg in CEGEK:
    if ceg in CSAK_LEPEDO:
        DEFAULT_LISTA.append(f"{ceg} – Lepedő")
    else:
        DEFAULT_LISTA.append(f"{ceg} – Paplan")
        DEFAULT_LISTA.append(f"{ceg} – Lepedő")


# ==========================================
# ÁLLAPOTKEZELÉS
# ==========================================

def alap_allapot():
    return {
        "index": 0,
        "utolso_darab": False,
        "elvalasztott_ceg": "",
        "riasztas_id": 0,
        "lista": DEFAULT_LISTA
    }


def save_state(state):
    try:
        temp_file = str(STATE_FILE) + ".tmp"

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(
                state,
                f,
                ensure_ascii=False,
                indent=4
            )

        os.replace(temp_file, STATE_FILE)

    except Exception as e:
        st.error(f"Mentési hiba: {e}")


def load_state():
    state = alap_allapot()

    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                old_state = json.load(f)

            if isinstance(old_state, dict):
                state.update(old_state)

    except Exception:
        pass

    state["lista"] = DEFAULT_LISTA

    try:
        state["index"] = int(state.get("index", 0))
    except (ValueError, TypeError):
        state["index"] = 0

    state["index"] = max(
        0,
        min(state["index"], len(DEFAULT_LISTA) - 1)
    )

    state["utolso_darab"] = bool(
        state.get("utolso_darab", False)
    )

    state["elvalasztott_ceg"] = str(
        state.get("elvalasztott_ceg", "")
    )

    try:
        state["riasztas_id"] = int(
            state.get("riasztas_id", 0)
        )
    except (ValueError, TypeError):
        state["riasztas_id"] = 0

    return state


# ==========================================
# MEGJELENÉS
# ==========================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top,
            #26313a 0%,
            #111820 55%,
            #090d12 100%
        );
    color: #f2f4f5;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1000px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

footer,
#MainMenu {
    visibility: hidden;
}

/* Álló tablet képernyő */

html, body, .stApp {
    min-height: 100%;
}

/* Görgetés engedélyezése érintőképernyőn */

div[data-baseweb="popover"] {
    max-height: 65vh !important;
}

div[data-baseweb="popover"] [role="listbox"],
div[data-baseweb="menu"] {
    max-height: 65vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    -webkit-overflow-scrolling: touch !important;
    overscroll-behavior-y: contain !important;
    touch-action: pan-y !important;
}

div[data-baseweb="popover"] [role="option"],
div[data-baseweb="menu"] [role="option"] {
    touch-action: pan-y !important;
    min-height: 48px !important;
}

/* Logó */

div[data-testid="stImage"] img {
    width: 60% !important;
    height: auto !important;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

/* Címek */

.main-title {
    text-align: center;
    font-size: clamp(25px, 4vw, 38px);
    font-weight: 900;
    letter-spacing: 2px;
    color: #f0bd55;
    margin-top: 12px;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #9ba9b5;
    font-size: 13px;
    letter-spacing: 3px;
    margin-bottom: 30px;
}

/* Állapotjelzések */

.status-normal {
    text-align: center;
    color: #8be0a8;
    font-size: 20px;
    font-weight: 800;
    padding: 20px 5px;
    letter-spacing: 1px;
}

.wait-message {
    text-align: center;
    color: #9bd9ad;
    font-size: 17px;
    font-weight: 700;
    padding: 18px 5px;
}

.status-alert {
    text-align: center;
    color: #ff6262;
    font-size: clamp(25px, 5vw, 42px);
    font-weight: 900;
    padding: 15px 5px;
    animation: villogas 1s infinite;
}

@keyframes villogas {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

/* Munka neve */

.work-label {
    text-align: center;
    color: #aeb9c3;
    font-size: 15px;
    letter-spacing: 2px;
    margin-top: 20px;
}

.work-name {
    text-align: center;
    color: #f0bd55;
    font-size: clamp(24px, 5vw, 42px);
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* Legördülő menü */

div[data-testid="stSelectbox"] label {
    color: #f0bd55 !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    margin-bottom: 10px !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #263541 !important;
    border: 2px solid #d9ad50 !important;
    border-radius: 13px !important;
    min-height: 65px !important;
    color: #ffffff !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

div[data-testid="stSelectbox"] svg {
    fill: #f0bd55 !important;
}

/* Gombok */

.stButton > button {
    width: 100%;
    min-height: 68px;
    border-radius: 13px;
    border: none;
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 1px;
    transition: 0.2s;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #dba83f,
        #f2cb72
    );
    color: #171b20;
}

.stButton > button[kind="primary"]:hover {
    background: #ffdc8a;
    color: #111820;
    transform: scale(1.01);
}

.stButton > button:not([kind="primary"]) {
    background: #263641;
    color: #ffffff;
    border: 1px solid #536574;
}

.stButton > button:not([kind="primary"]):hover {
    background: #344957;
    border-color: #e0b65c;
}

/* Riasztási keret */

.alert-box {
    background: #301d20;
    border: 2px solid #d94c52;
    border-radius: 16px;
    padding: 22px 12px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 0 18px rgba(220, 65, 65, 0.16);
}

.alert-box .work-label {
    color: #ffaaaa;
    margin-top: 0;
}

.alert-box .work-name {
    color: #ffffff;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# BILLENTYŰZET LETILTÁSA A SELECTBOXNÁL
# ==========================================

components.html("""
<script>
(function () {
    try {
        const doc = window.parent.document;

        function billentyuzetTiltas() {
            const mezok = doc.querySelectorAll(
                'div[data-testid="stSelectbox"] input'
            );

            mezok.forEach(function (mezo) {
                if (!mezo.hasAttribute("readonly")) {
                    mezo.setAttribute("readonly", "readonly");
                }

                mezo.setAttribute("inputmode", "none");
                mezo.setAttribute("autocomplete", "off");
                mezo.setAttribute("autocorrect", "off");
                mezo.setAttribute("spellcheck", "false");
            });
        }

        billentyuzetTiltas();

        const observer = new MutationObserver(function () {
            billentyuzetTiltas();
        });

        observer.observe(doc.documentElement, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ["readonly"]
        });

    } catch (error) {
        console.warn(
            "Billentyűzet tiltása nem sikerült:",
            error
        );
    }
})();
</script>
""", height=0)


# ==========================================
# KÖZÖS LOGÓ
# ==========================================

def logo_megjelenites():

    bal, kozep, jobb = st.columns([1, 3, 1])

    with kozep:
        if LOGO_FILE.exists():
            st.image(str(LOGO_FILE))
        else:
            st.markdown(
                '<div class="main-title">VASALÓSOR</div>',
                unsafe_allow_html=True
            )


def cim_megjelenites():
    st.markdown(
        '<div class="main-title">VASALÓSOR VEZÉRLŐ</div>',
        unsafe_allow_html=True
    )


# ==========================================
# ELÜLSŐ KEZELŐÁLLOMÁS
# ==========================================

def elso_nezet():

    state = load_state()

    logo_megjelenites()
    cim_megjelenites()

    st.markdown(
        '<div class="sub-title">ELÜLSŐ KEZELŐÁLLOMÁS</div>',
        unsafe_allow_html=True
    )

    if state["utolso_darab"]:
        st.markdown(
            '<div class="wait-message">'
            'A hátulsó kezelőállomás nyugtázására vár.'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-normal">🟢 NORMÁL MENETBEN</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="work-label">AKTUÁLIS MUNKA</div>',
        unsafe_allow_html=True
    )

    if "aktualis_selectbox" not in st.session_state:
        st.session_state["aktualis_selectbox"] = DEFAULT_LISTA[
            state["index"]
        ]

    selected = st.selectbox(
        "Kérlek válassz!",
        DEFAULT_LISTA,
        key="aktualis_selectbox"
    )

    selected_index = DEFAULT_LISTA.index(selected)

    if selected_index != state["index"]:
        state["index"] = selected_index
        save_state(state)

    st.markdown(
        f'<div class="work-name">{html.escape(selected)}</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "🔔  UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE",
        type="primary",
        use_container_width=True
    ):

        state["elvalasztott_ceg"] = selected
        state["utolso_darab"] = True
        state["riasztas_id"] = state.get("riasztas_id", 0) + 1

        save_state(state)
        st.rerun()


# ==========================================
# HÁTSÓ KEZELŐÁLLOMÁS
# ==========================================

def hatso_nezet():

    state = load_state()

    logo_megjelenites()
    cim_megjelenites()

    st.markdown(
        '<div class="sub-title">HÁTSÓ KEZELŐÁLLOMÁS</div>',
        unsafe_allow_html=True
    )

    aktualis_munka = DEFAULT_LISTA[state["index"]]

    st.markdown(
        '<div class="work-label">KÖVETKEZŐ AKTUÁLIS MUNKA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="work-name">{html.escape(aktualis_munka)}</div>',
        unsafe_allow_html=True
    )

    if state["utolso_darab"]:

        st.markdown(
            '<div class="status-alert">'
            '⚠ ELVÁLASZTÓ ÉRKEZETT ⚠'
            '</div>',
            unsafe_allow_html=True
        )

        bekuldott_munka = html.escape(
            state["elvalasztott_ceg"]
        )

        st.markdown(
            f"""
            <div class="alert-box">
                <div class="work-label">
                    ELVÁLASZTÓ BEKÜLDVE
                </div>
                <div class="work-name">
                    {bekuldott_munka}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Automatikus, ismétlődő hangjelzés.

        components.html("""
            <audio autoplay loop>
                <source
                    src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"
                    type="audio/mpeg">
            </audio>
        """, height=0)

        if st.button(
            "✓  KIVÉVE / NYUGTÁZÁS",
            type="primary",
            use_container_width=True
        ):

            state["utolso_darab"] = False
            state["elvalasztott_ceg"] = ""

            save_state(state)
            st.rerun()

    else:

        st.markdown(
            '<div class="status-normal">🟢 NORMÁL MENETBEN</div>',
            unsafe_allow_html=True
        )


# ==========================================
# TELJES KÉPERNYŐ IKON
# ==========================================

components.html("""
<script>
(function () {
    try {
        const parentDoc = window.parent.document;
        const parentWindow = window.parent;

        function fullscreenGomb() {
            let button = parentDoc.getElementById(
                "vasalosor-fullscreen-button"
            );

            if (!button) {
                button = parentDoc.createElement("button");
                button.id = "vasalosor-fullscreen-button";
                button.type = "button";
                button.innerHTML = "⛶";
                button.title = "Teljes képernyő be / ki";

                button.style.cssText = `
                    position: fixed;
                    left: 12px;
                    bottom: calc(12px + env(safe-area-inset-bottom));
                    width: 42px;
                    height: 42px;
                    border-radius: 50%;
                    border: 1px solid rgba(220,190,120,0.45);
                    background: rgba(28,39,49,0.88);
                    color: #e8bd62;
                    font-size: 25px;
                    line-height: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 2147483647;
                    cursor: pointer;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.35);
                    -webkit-tap-highlight-color: transparent;
                `;

                parentDoc.body.appendChild(button);

                button.addEventListener("click", async function () {
                    try {
                        if (!parentDoc.fullscreenElement) {
                            await parentDoc.documentElement.requestFullscreen();
                        } else {
                            await parentDoc.exitFullscreen();
                        }
                    } catch (error) {
                        console.warn("Fullscreen nem érhető el:", error);
                    }
                });

                parentDoc.addEventListener("fullscreenchange", function () {
                    button.innerHTML = "⛶";

                    button.title = parentDoc.fullscreenElement
                        ? "Kilépés a teljes képernyőből"
                        : "Teljes képernyő bekapcsolása";
                });
            }
        }

        fullscreenGomb();

    } catch (error) {
        console.warn("A teljes képernyős ikon nem telepíthető:", error);
    }
})();
</script>
""", height=0)


# ==========================================
# AUTOMATIKUS FRISSÍTÉS
# ==========================================

@st.fragment(run_every=1)
def futo_nezet():

    view = st.query_params.get("view", "elol")

    if view == "hatul":
        hatso_nezet()
    else:
        elso_nezet()


futo_nezet()
