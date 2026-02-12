import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="極限爆速・英語監視", layout="centered")

st.title("⚡️ 0.1秒判定・リアルタイム監視")
st.write("英語はスルーし、日本語が混ざった瞬間に警告を出します。")

warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

# --- JavaScript エンジン (英語・日本語 両対応版) ---
st_js = f"""
<div id="status" style="padding:10px; border-radius:5px; background:#f0f2f6; margin-bottom:10px; font-family:sans-serif;">
    状態: 停止中
</div>
<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:red; color:white; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; font-family:sans-serif;">
    <h1 style="font-size:60px; margin:0;">🚨 {warning_msg} 🚨</h1>
    <p id="detected-text" style="font-size:24px; margin:20px;"></p>
    <button onclick="hideWarning()" style="padding:15px 30px; font-size:20px; border:none; border-radius:5px; cursor:pointer;">閉じる</button>
</div>

<button id="start-btn" style="padding:20px; width:100%; background:#ff4b4b; color:white; border:none; border-radius:10px; font-size:20px; cursor:pointer; font-weight:bold;">
    🎤 監視スタート
</button>

<script>
    const startBtn = document.getElementById('start-btn');
    const statusDiv = document.getElementById('status');
    const warningScreen = document.getElementById('warning-screen');
    const detectedText = document.getElementById('detected-text');

    let recognition;

    if (!('webkitSpeechRecognition' in window)) {{
        statusDiv.innerText = "エラー: SafariかChromeを使ってください。";
    }} else {{
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        
        // ★ここが重要：ブラウザの言語を「自動」に近づけるため、あえて設定を工夫します
        // iPad/iPhoneの場合、システムの言語設定に引きずられることがあるため、
        // 日本語文字が含まれているかどうかのチェックを強化します。
        recognition.lang = 'en-US'; 

        recognition.onstart = () => {{
            statusDiv.innerText = "状態: ⚡️ リアルタイム監視中...";
            startBtn.innerText = "🛑 監視を止める";
            startBtn.style.background = "#333";
        }};

        recognition.onresult = (event) => {{
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                interimTranscript += event.results[i][0].transcript;
            }}

            if (interimTranscript.length > 0) {{
                // 【判定ロジック】ひらがな・カタカナが1文字でも入ったらアウト
                if (/[ぁ-んァ-ヶ]/.test(interimTranscript)) {{
                    showWarning(interimTranscript);
                }}
            }}
        }};

        recognition.onend = () => {{
            statusDiv.innerText = "状態: 停止中";
            startBtn.innerText = "🎤 監視スタート";
            startBtn.style.background = "#ff4b4b";
        }};
    }}

    startBtn.onclick = () => {{
        if (statusDiv.innerText.includes("停止中")) {{
            recognition.start();
        }} else {{
            recognition.stop();
        }}
    }};

    function showWarning(text) {{
        detectedText.innerText = "検知内容: " + text;
        warningScreen.style.display = 'flex';
        if(recognition) recognition.stop();
    }}

    function hideWarning() {{
        warningScreen.style.display = 'none';
        recognition.start();
    }}
</script>
"""

components.html(st_js, height=500)
