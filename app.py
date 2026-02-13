import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ironclad English Coach", layout="centered")

st.title("🚀 120万点：鉄壁の英語監視")
st.markdown("綴り、音の並び、単語の長さから**「日本語の気配」**を完全に遮断します。")

warning_msg = st.text_input("🇯🇵 警告メッセージ", value="SYSTEM ERROR: NON-ENGLISH DETECTED!")

st_js = f"""
<div id="status" style="padding:10px; border-radius:5px; background:#f0f2f6; margin-bottom:10px; font-family:sans-serif; font-size:14px; font-weight:bold;">
    STATUS: ONLINE
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#000; color:#ff0000; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center;">
    <h1 style="font-size:50px; margin:0; border:5px solid #ff0000; padding:20px;">{warning_msg}</h1>
    <p id="detected-text" style="font-size:24px; margin:20px; font-family:monospace; color:#fff;"></p>
    <button onclick="hideWarning()" style="padding:20px 40px; font-size:24px; border:none; border-radius:10px; cursor:pointer; background:#ff0000; color:#fff; font-weight:bold;">RESTART SYSTEM</button>
</div>

<button id="start-btn" style="padding:25px; width:100%; background:#222; color:#00ff00; border:2px solid #00ff00; border-radius:15px; font-size:22px; cursor:pointer; font-family:monospace; font-weight:bold; box-shadow: 0 0 10px #00ff00;">
    INITIATE ENGLISH-ONLY PROTOCOL
</button>

<div style="margin-top:20px; font-weight:bold; color:#00ff00; font-family:monospace;">> LIVE_FEED:</div>
<div id="log-container" style="width:100%; height:300px; border:1px solid #00ff00; border-radius:10px; padding:15px; overflow-y:scroll; background:#000; font-family:'Courier New', monospace; font-size:20px; line-height:1.4; color:#00ff00;">
</div>

<script>
    const startBtn = document.getElementById('start-btn');
    const statusDiv = document.getElementById('status');
    const warningScreen = document.getElementById('warning-screen');
    const detectedText = document.getElementById('detected-text');
    const logContainer = document.getElementById('log-container');

    let recognition;

    function initRecognition() {{
        const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {{
            let interimText = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                let text = event.results[i][0].transcript;
                
                // 【120万点の監視ロジック】
                // 1. 非英字（かな・漢字）
                const hasJp = /[^ -~]/.test(text);
                
                // 2. ローマ字特有の綴り（連続するn, m, rや特定の母音パターン）
                const hasRomajiPattern = /nni|mme|tti|ssi|rru|hha|nno|ssu|kku|[aiueo]{{3,}}/i.test(text);
                
                // 3. 異常な単語の長さ（スペースなしで12文字以上は、ローマ字変換の疑い）
                const words = text.split(' ');
                const hasLongWord = words.some(w => w.length > 12);

                if (hasJp || hasRomajiPattern || hasLongWord) {{
                    triggerWarning(text);
                    return;
                }}

                if (event.results[i].isFinal) {{
                    logContainer.innerHTML += '<div>> ' + text.toUpperCase() + '</div>';
                }} else {{
                    interimText = text;
                }}
            }}
            logContainer.scrollTop = logContainer.scrollHeight;
        }};

        recognition.onstart = () => {{
            statusDiv.innerText = "STATUS: ACTIVE_FILTERING";
            statusDiv.style.color = "#00ff00";
            startBtn.innerText = "TERMINATE SESSION";
            startBtn.style.boxShadow = "0 0 20px #ff0000";
            startBtn.style.color = "#ff0000";
            startBtn.style.borderColor = "#ff0000";
        }};

        recognition.onend = () => {{
            if (warningScreen.style.display !== 'flex') {{
                statusDiv.innerText = "STATUS: IDLE";
                statusDiv.style.color = "#222";
                startBtn.innerText = "INITIATE ENGLISH-ONLY PROTOCOL";
                startBtn.style.boxShadow = "0 0 10px #00ff00";
                startBtn.style.color = "#00ff00";
                startBtn.style.borderColor = "#00ff00";
            }}
        }};
    }}

    function triggerWarning(text) {{
        detectedText.innerText = "SECURITY BREACH: " + text;
        warningScreen.style.display = 'flex';
        recognition.stop();
    }}

    function hideWarning() {{
        warningScreen.style.display = 'none';
        recognition.start();
    }}

    startBtn.onclick = () => {{
        if (!recognition) initRecognition();
        if (statusDiv.innerText.includes("IDLE") || statusDiv.innerText.includes("ONLINE")) {{
            recognition.start();
        }} else {{
            recognition.stop();
        }}
    }};
</script>
"""

components.html(st_js, height=750)
