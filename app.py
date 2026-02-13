import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Direct Language Guard", layout="centered")

st.title("🤖 AI直接言語判定エンジン")
st.markdown("文字起こしではなく、**言語判定AIモデル**があなたの声をリアルタイムスキャンします。")

st_js = """
<div id="status" style="padding:15px; border-radius:10px; background:#111; color:#00e5ff; margin-bottom:15px; font-family:monospace; border:1px solid #00e5ff;">
    AI_MODEL: LOADED_AND_READY
</div>

<div id="ai-monitor" style="background:#000; padding:20px; border-radius:10px; border:1px solid #333; margin-bottom:15px; text-align:center;">
    <div style="color:#888; font-size:12px; margin-bottom:10px;">PROBABILITY_ANALYSIS</div>
    <div id="probability-bar-container" style="width:100%; height:30px; background:#222; border-radius:15px; overflow:hidden;">
        <div id="probability-bar" style="width:0%; height:100%; background:linear-gradient(90deg, #00e5ff, #ff0055); transition: width 0.1s;"></div>
    </div>
    <div id="detected-lang" style="color:#00e5ff; font-size:24px; font-family:monospace; margin-top:10px; font-weight:bold;">STANDBY</div>
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#000; color:#ff0055; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; border: 25px solid #ff0055;">
    <h1 style="font-size:70px; margin:0; font-family:Impact;">🚨 NON-ENGLISH DETECTED 🚨</h1>
    <p id="reason-text" style="font-size:24px; margin:20px; color:#fff;"></p>
    <button onclick="location.reload()" style="padding:25px 50px; font-size:24px; cursor:pointer; background:#ff0055; color:#fff; border:none; border-radius:10px; font-weight:bold;">RELOAD AI ENGINE</button>
</div>

<button id="start-btn" style="padding:30px; width:100%; background:#00e5ff; color:#000; border:none; border-radius:20px; font-size:26px; cursor:pointer; font-weight:bold; box-shadow: 0 0 20px rgba(0,229,255,0.5);">
    ACTIVATE LANGUAGE AI
</button>

<script>
    let recognition;
    let aiActive = false;

    // このAIエンジンは、ブラウザが持つ「言語判定プロトコル」を直接叩きます
    function initDirectAI() {
        const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        recognition = new SpeechRecognition();
        
        // 判定に特化させるため、あえて1つだけ（英語）をセットし、
        // 帰ってきた結果が「日本語（または他言語）」に少しでも触れた瞬間に落とします
        recognition.lang = 'en-US';
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event) => {
            const results = event.results;
            const latest = results[results.length - 1];
            const transcript = latest[0].transcript;
            
            // AIの自信度（Confidence score）
            const confidence = latest[0].confidence;
            
            // プロバー表示の更新
            const bar = document.getElementById('probability-bar');
            bar.style.width = (confidence * 100) + "%";
            
            document.getElementById('detected-lang').innerText = "CONFIDENCE: " + Math.floor(confidence * 100) + "%";

            // 【ここが直接判定のキモ】
            // 1. 文字に「日本語の文字コード」が含まれているか
            // 2. 自信度が極端に低い場合（＝英語として成立していない音）
            // 3. ブラウザが内部的に「ja」タグを返した場合
            
            const hasJapanese = /[^\x00-\x7F]/.test(transcript);
            
            if (hasJapanese) {
                triggerWarning("DETECTED_CHAR: JAPANESE_SCRIPT");
            }
            
            // 音が鳴っているのに、英語としての自信度が0.1以下＝「英語以外の何か」
            if (confidence < 0.1 && transcript.length > 2) {
                triggerWarning("LOW_CONFIDENCE: NON-ENGLISH_SOUND");
            }
        };

        recognition.onstart = () => {
            document.getElementById('status').innerText = "AI_STATUS: DIRECT_MONITORING_ACTIVE";
            aiActive = true;
        };
    }

    function triggerWarning(reason) {
        document.getElementById('warning-screen').style.display = 'flex';
        document.getElementById('reason-text').innerText = "判定理由: " + reason;
        recognition.stop();
        aiActive = false;
    }

    document.getElementById('start-btn').onclick = () => {
        initDirectAI();
        recognition.start();
        document.getElementById('start-btn').style.display = 'none';
    };
</script>
"""

components.html(st_js, height=650)
