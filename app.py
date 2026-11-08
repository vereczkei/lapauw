import streamlit as st
import json
import os

st.set_page_config(page_title="Vasalósor Vezérlő", layout="wide")

DATA_FILE = "vasalosor_allapot.json"

def load_state():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
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
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=4)

params = st.query_params
nezet = params.get("view", "hatul")

state = load_state()
idx = state["index"]
lista = state["lista"]
utolso = state["utolso_darab"]

st.markdown("""
    <style>
    @keyframes villog {
        0% { opacity: 1; }
        50% { opacity: 0.2; }
        100% { opacity: 1; }
    }
    .figyelem-villog {
        animation: villog 0.8s infinite;
        background-color: #000000;
        color: #FFD700;
        border: 4px solid #FFD700;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
    }
    .aktualis-doboz {
        background-color: #1e1e1e;
        border: 3px solid #28a745;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 Vasalósor Vezérlő")

if not lista:
    st.warning("Nincs aktív feladat.")
    st.stop()

akt_elem = lista[idx % len(lista)]

# --- ZÖLD KERETES AKTUÁLIS MUNKA KIJELZÉS ÉS VÁLTÁS ---
with st.container():
    st.markdown(f"""
        <div class="aktualis-doboz">
            <p style="color: #28a745; font-size: 18px; margin: 0; font-weight: bold;">🟢 AKTUÁLIS MUNKA:</p>
            <p style="color: #ffffff; font-size: 36px; margin: 10px 0 0 0; font-weight: bold;">{akt_elem['ceg']} - {akt_elem['textil'].upper()}</p>
        </div>
    """, unsafe_allow_html=True)

# Gombok a munkák független váltásához elöl/hátul bárhol
col_v1, col_v2 = st.columns(2)
with col_v1:
    if st.button("⬅️ Előző Munka", use_container_width=True):
        state["index"] = (idx - 1) % len(lista)
        save_state(state)
        st.rerun()
with col_v2:
    if st.button("Következő Munka ➡️", use_container_width=True):
        state["index"] = (idx + 1) % len(lista)
        save_state(state)
        st.rerun()

st.write("---")

# --- NÉZETEK SZERETI LOGIKA ---
if nezet == "elol":
    if not utolso:
        if st.button("🛑 UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE", use_container_width=True, type="primary"):
            state["utolso_darab"] = True
            save_state(state)
            st.rerun()
    else:
        st.markdown("""
            <div class="figyelem-villog">
                ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE<br><span style="font-size:16px; color:#fff;">Várakozás a hátsó nyugtázásra...</span>
            </div>
        """, unsafe_allow_html=True)

elif nezet == "hatul":
    if utolso:
        st.markdown("""
            <div class="figyelem-villog">
                ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BENN!<br><span style="font-size:16px; color:#fff;">Kérlek vedd ki és nyugtázd!</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Hang lejátszás HTML5 audióval
        st.markdown("""
            <audio id="riasztas" autoplay loop>
                <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
            </audio>
            <script>
                var aud = document.getElementById("riasztas");
                if(aud) { aud.play().catch(e => console.log("Blocked")); }
            </script>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("✅ KIVÉVE / TOVÁBB A KÖVETKEZŐRE", use_container_width=True, type="primary"):
            state["index"] = (idx + 1) % len(lista)
            state["utolso_darab"] = False
            save_state(state)
            st.rerun()
    else:
        st.markdown("""
            <div style="background-color: #222; color: #FFD700; border: 2px solid #FFD700; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 18px;">
                🟡 Állapot: Normál menetben
            </div>
        """, unsafe_allow_html=True)

# Automatikus háttérfrissítés (1 másodpercenként lekéri a legfrissebb állását a fájlnak)
st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 1000);
    </script>
""", unsafe_allow_html=True)
