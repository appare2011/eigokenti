import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="極限爆速・英語監視", layout="centered")

st.title("⚡️ 0.1秒判定・リアルタイム監視")
st.write("ブラウザ内で判定するため、通信待ちがありません。")

# 警告メッセージの設定
warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

# --- JavaScript / HTML エンジン ---
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

    if (!('webkitSpeechRecognition' in window) && !('speechRecognition' in window)) {{
        statusDiv.innerText = "エラー: お使いのブラウザは音声認識に対応していません。SafariかChromeを使ってください。";
    }} else {{
        const SpeechRecognition = window.webkitSpeechRecognition || window.speechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;      // 連続して認識
        recognition.interimResults = true;  // 喋っている途中でも結果を出す
        recognition.lang = 'ja-JP';         // 日本語を検知するために日本語モード

        recognition.onstart = () => {{
            statusDiv.innerText = "状態: ⚡️ リアルタイム監視中...";
            statusDiv.style.background = "#e1f5fe";
            startBtn.innerText = "🛑 監視を止める";
            startBtn.style.background = "#333";
        }};

        recognition.onresult = (event) => {{
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                if (event.results[i].isFinal || event.results[i][0].confidence > 0.1) {{
                    interimTranscript += event.results[i][0].transcript;
                }}
            }}

            if (interimTranscript.length > 0) {{
                // 日本語特有の文字（ひらがな・カタカナ）が含まれているかチェック
                if (/[ぁ-んァ-ヶ]/.test(interimTranscript)) {{
                    showWarning(interimTranscript);
                }}
            }}
        }};

        recognition.onerror = (event) => {{
            statusDiv.innerText = "エラーが発生しました: " + event.error;
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
        // 判定が出た後、少しだけ停止してリセット（連続警告を防ぐ）
        setTimeout(() => {{ 
            if(recognition) recognition.stop();
        }}, 500);
    }}

    function hideWarning() {{
        warningScreen.style.display = 'none';
        recognition.start(); // 監視を再開
    }}
</script>
"""

# HTMLコンポーネントを埋め込み
components.html(st_js, height=500)

st.divider()
st.info("【使い方】\n1. 「監視スタート」を押す\n2. マイクの使用を「許可」する\n3. 日本語を喋った瞬間に画面が赤くなります！")
