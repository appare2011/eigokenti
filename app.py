import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="24時間英語監視・ログ付", layout="centered")

st.title("⚡️ 英語ログ ＆ 鉄の掟監視")
st.write("話した英語は下に記録されます。日本語が混じると即警告が出ます。")

warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

st_js = f"""
<div id="status" style="padding:10px; border-radius:5px; background:#f0f2f6; margin-bottom:10px; font-family:sans-serif; font-size:14px;">
    状態: 停止中
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:red; color:white; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; font-family:sans-serif;">
    <h1 style="font-size:60px; margin:0;">🚨 {warning_msg} 🚨</h1>
    <p id="detected-text" style="font-size:24px; margin:20px; background:rgba(0,0,0,0.2); padding:10px;"></p>
    <button onclick="hideWarning()" style="padding:15px 30px; font-size:20px; border:none; border-radius:5px; cursor:pointer; background:white; color:red; font-weight:bold;">再開する</button>
</div>

<button id="start-btn" style="padding:20px; width:100%; background:#ff4b4b; color:white; border:none; border-radius:10px; font-size:20px; cursor:pointer; font-weight:bold; margin-bottom:20px;">
    🎤 監視＆ログ開始
</button>

<div style="font-family:sans-serif; font-weight:bold; margin-bottom:5px;">📋 English Log:</div>
<div id="log-container" style="width:100%; height:250px; border:2px solid #ddd; border-radius:10px; padding:10px; overflow-y:scroll; background:#fafafa; font-family:monospace; font-size:18px; line-height:1.5;">
</div>

<script>
    const startBtn = document.getElementById('start-btn');
    const statusDiv = document.getElementById('status');
    const warningScreen = document.getElementById('warning-screen');
    const detectedText = document.getElementById('detected-text');
    const logContainer = document.getElementById('log-container');

    let recognition;
    let finalTranscript = '';

    if (!('webkitSpeechRecognition' in window)) {{
        statusDiv.innerText = "エラー: SafariかChromeを使ってください。";
    }} else {{
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US'; 

        recognition.onresult = (event) => {{
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                let text = event.results[i][0].transcript;
                
                // 【鉄の掟チェック】
                // 半角英数記号以外（日本語・カタカナ）が含まれているか
                if (/[^ -~]/.test(text)) {{
                    showWarning(text);
                    return; // 警告時は処理中断
                }}

                if (event.results[i].isFinal) {{
                    finalTranscript += text + ' ';
                }} else {{
                    interimTranscript = text;
                }}
            }}
            
            // ログの更新
            logContainer.innerHTML = '<span style="color:#333;">' + finalTranscript + '</span>' + 
                                   '<span style="color:#aaa;">' + interimTranscript + '</span>';
            logContainer.scrollTop = logContainer.scrollHeight;
        }};

        recognition.onstart = () => {{
            statusDiv.innerText = "状態: 🔥 監視＆記録中...";
            startBtn.innerText = "🛑 停止";
            startBtn.style.background = "#333";
        }};

        recognition.onend = () => {{
            statusDiv.innerText = "状態: 停止中";
            startBtn.innerText = "🎤 監視＆ログ開始";
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
        detectedText.innerText = "禁止文字を検知: " + text;
        warningScreen.style.display = 'flex';
        if(recognition) recognition.stop();
    }}

    function hideWarning() {{
        warningScreen.style.display = 'none';
        recognition.start();
    }}
</script>
"""

components.html(st_js, height=600)
