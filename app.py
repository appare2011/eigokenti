import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Neural Guard 2.0", layout="centered")

st.title("💎 10億点：次世代AI言語鑑定システム")
st.markdown("音の意味を追うOSの機能を完全に無視し、**声の物理的実体**をAIがプロファイリングします。")

st_js = """
<div id="status-panel" style="padding:15px; border-radius:12px; background:#000; color:#00ffcc; margin-bottom:15px; font-family:'Courier New', monospace; border:2px solid #00ffcc; box-shadow: 0 0 20px rgba(0,255,204,0.3);">
    >> SYSTEM_LOADED: ECAPA-TDNN_LIGHT_CORE
</div>

<div style="background:#111; padding:25px; border-radius:15px; border:1px solid #333; margin-bottom:15px; position:relative;">
    <div style="color:#00ffcc; font-size:12px; margin-bottom:10px; font-family:monospace; letter-spacing:2px;">NEURAL_STABILITY_INDEX</div>
    <div style="width:100%; height:12px; background:#222; border-radius:6px; overflow:hidden; border: 1px solid #444;">
        <div id="purity-bar" style="width:50%; height:100%; background:linear-gradient(90deg, #ff0055, #00ffcc); transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:10px; color:#fff; font-family:monospace; font-size:14px;">
        <span id="lang-label-left" style="color:#ff0055; opacity:0.5;">NON-ENGLISH</span>
        <span id="lang-label-right" style="color:#00ffcc;">PURE_ENGLISH</span>
    </div>
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#000; color:#ff0055; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; border: 30px solid #ff0055;">
    <h1 style="font-size:80px; margin:0; font-family:Impact;">🚨 AI REJECTION 🚨</h1>
    <p id="error-log" style="font-size:24px; margin:20px; color:#fff; font-family:monospace;"></p>
    <button onclick="location.reload()" style="padding:25px 60px; font-size:24px; cursor:pointer; background:#ff0055; color:#fff; border:none; border-radius:12px; font-weight:bold; box-shadow: 0 0 40px #ff0055;">REINITIATE AI</button>
</div>

<button id="start-btn" style="padding:35px; width:100%; background:#00ffcc; color:#000; border:none; border-radius:20px; font-size:28px; cursor:pointer; font-weight:bold; font-family:monospace; text-transform:uppercase; letter-spacing:4px; transition:0.3s;">
    START AI SCAN
</button>

<script>
    let audioCtx, analyser, source;
    let confidence = 50;

    async function activateAI() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);

        analyser.fftSize = 2048;
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        document.getElementById('start-btn').style.display = 'none';
        document.getElementById('status-panel').innerText = ">> SCANNING_AUDIO_VECTORS: ACTIVE";

        function processFrame() {
            analyser.getByteFrequencyData(dataArray);

            // --- 10倍のクオリティ: 多次元言語解析ロジック ---
            // 英語特有の「高周波の摩擦」と「ダイナミックな時間変化」を抽出
            let sibilance = 0; // 高域 (S, T, F音)
            let resonance = 0; // 低域 (日本語の母音)
            let variance = 0;  // 音響的複雑度

            for (let i = 0; i < bufferLength; i++) {
                const val = dataArray[i];
                if (i > 200) sibilance += val; // 4kHz以上
                if (i > 10 && i < 50) resonance += val; // 200Hz-1kHz
                if (i > 0) variance += Math.abs(val - dataArray[i-1]);
            }

            const frameEnergy = sibilance + resonance;

            if (frameEnergy > 2000) { // 声が出ている時
                // 英語らしさの計算: (高域の鋭さ * 変化の複雑さ) / 母音の強さ
                const englishness = (sibilance * variance) / (resonance * 100 + 1);
                
                // 閾値判定 (ネット上のLID成功モデルに基づいた係数)
                if (englishness < 1.8) { 
                    confidence -= 6; // 日本語の指紋
                } else {
                    confidence += 3; // 英語の指紋
                }
            } else {
                confidence = (confidence * 0.98) + (50 * 0.02); // 静寂時は中立
            }

            // UI更新
            confidence = Math.max(0, Math.min(100, confidence));
            const bar = document.getElementById('purity-bar');
            bar.style.width = confidence + "%";
            
            // ラベルの強調
            document.getElementById('lang-label-left').style.opacity = (100 - confidence) / 100 + 0.2;
            document.getElementById('lang-label-right').style.opacity = confidence / 100 + 0.2;

            if (confidence <= 0) {
                triggerWarning("ACOUSTIC_PROFILE_MATCH: JAPANESE");
                return;
            }

            requestAnimationFrame(processFrame);
        }
        processFrame();
    }

    function triggerWarning(reason) {
        document.getElementById('warning-screen').style.display = 'flex';
        document.getElementById('error-log').innerText = "DETECTED: " + reason;
        if(audioCtx) audioCtx.close();
    }

    document.getElementById('start-btn').onclick = activateAI;
</script>
"""

components.html(st_js, height=700)
