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
        font-size: 28px;
        font-weight: bold;
    }
    div.stSelectbox {
        padding-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

@st.fragment(run_every=1)
def futo_nezet():
    current_state = load_state()
    idx = current_state["index"]
    lista = current_state["lista"]
    utolso = current_state["utolso_darab"]
    
    st.title("🏭 Vasalósor Vezérlő")

    if not lista:
        st.warning("Nincs aktív feladat.")
        return

    ceg_opciok = [f"{item['ceg']} {item['textil']}" for item in lista]

    # --- ZÖLD KERETES DOBOZ (Aktuális munka) ---
    with st.container(border=True):
        st.markdown('<p style="color: #28a745; font-size: 22px; font-weight: bold; margin: 0;">🟢 AKTUÁLIS MUNKA:</p>', unsafe_allow_html=True)
        valasztott_aktualis_str = st.selectbox(
            "Aktuális", 
            ceg_opciok, 
            index=idx, 
            key="select_aktualis", 
            label_visibility="collapsed"
        )
    
    uj_idx = ceg_opciok.index(valasztott_aktualis_str)
    if uj_idx != idx:
        current_state["index"] = uj_idx
        save_state(current_state)
        st.rerun()

    st.write("---")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        if nezet == "elol":
            if not utolso:
                if st.button("🛑 UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE", use_container_width=True, type="primary"):
                    current_state["utolso_darab"] = True
                    save_state(current_state)
                    st.rerun()
            else:
                st.markdown("""
                    <div class="figyelem-villog">
                        ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BEKÜLDVE<br><span style="font-size:16px;">Várakozás a hátsó nyugtázásra...</span>
                    </div>
                """, unsafe_allow_html=True)
        
        elif nezet == "hatul":
            if utolso:
                st.markdown("""
                    <div class="figyelem-villog">
                        ⚠️ UTOLSÓ DARAB / ELVÁLASZTÓ BENN!<br><span style="font-size:16px;">Kérlek vedd ki és nyugtázd!</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Biztosított audio elem loop-pal és JS lejátszási kényszerítéssel
                st.markdown("""
                    <audio id="riasztas-hang" autoplay loop>
                        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                    </audio>
                    <script>
                        var audio = document.getElementById("riasztas-hang");
                        if (audio) {
                            audio.play().catch(function(error) {
                                console.log("Autoplay blocked, waiting for interaction");
                            });
                        }
                    </script>
                """, unsafe_allow_html=True)
                
                st.write("")
                if st.button("✅ KIVÉVE / TOVÁBB A KÖVETKEZŐRE", use_container_width=True, type="primary"):
                    current_state["index"] = (current_state["index"] + 1) % len(current_state["lista"])
                    current_state["utolso_darab"] = False
                    save_state(current_state)
                    st.rerun()
            else:
                st.markdown("""
                    <div style="background-color: #222; color: #FFD700; border: 2px solid #FFD700; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 18px;">
                        🟡 Állapot: Normál menetben
                    </div>
                """, unsafe_allow_html=True)

futo_nezet()
