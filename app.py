import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Language Neural Shield", layout="centered")

st.title("🧠 100点：AIニューラル言語判定")
st.markdown("OSの翻訳機能をバイパスし、**音の響き**から英語か日本語かを直接AIが鑑定します。")

st_js = """
<div id="status" style="padding:15px; border-radius:10px; background:#000; color:#00e5ff; margin-bottom:15px; font-family:monospace; border:1px solid #00e5ff; box-shadow: 0 0 10px #00e5ff;">
    AI_ENGINE: NEURAL_MONITORING_READY
</div>

<div style="background:#111; padding:20px; border-radius:10px; border:1px solid #333; margin-bottom:15px;">
    <div style="color:#888; font-size:12px; margin-bottom:10px; font-family:monospace;">REALTIME_PROBABILITY_SCAN</div>
    <div style="width:100%; height:40px; background:#222; border-radius:20px; overflow:hidden; border: 2px solid #333;">
        <div id="prob-bar" style="width:0%; height:100%; background:linear-gradient(90deg, #ff0055, #00ff00); transition: width 0.1s;"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:5px; color:#fff; font-family:monospace; font-size:12px;">
        <span>NON-ENGLISH</span>
        <span>ENGLISH_PURITY</span>
    </div>
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#000; color:#ff0055; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; border: 20px solid #ff0055;">
    <h1 style="font-size:80px; margin:0; font-family:Impact;">🚨 JP_SIGNAL_DETECTED 🚨</h1>
    <p id="alert-reason" style="font-size:24px; margin:20px; color:#fff; font-family:monospace;"></p>
    <button onclick="location.reload()" style="padding:25px 50px; font-size:24px; cursor:pointer; background:#ff0055; color:#fff; border:none; border-radius:10px; font-weight:bold;">SYSTEM_REBOOT</button>
</div>

<button id="start-btn" style="padding:30px; width:100%; background:#111; color:#00e5ff; border:2px solid #00e5ff; border-radius:20px; font-size:26px; cursor:pointer; font-weight:bold; font-family:monospace; box-shadow: 0 0 20px rgba(0,229,255,0.3);">
    ACTIVATE NEURAL SCANNER
</button>

<script>
    let audioCtx, analyser, dataArray, source;
    let englishScore = 50;

    async function initAI() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        
        analyser.fftSize = 2048;
        dataArray = new Uint8Array(analyser.frequencyBinCount);

        document.getElementById('status').innerText = "AI_STATUS: DIRECT_WAVEFORM_ANALYSIS";
        document.getElementById('start-btn').style.display = 'none';

        function scan() {
            analyser.getByteFrequencyData(dataArray);

            // --- AI判定アルゴリズム (Language Fingerprinting) ---
            // 英語は高い摩擦音(S,T,F)と、音のピッチの激しい上下移動が特徴。
            // 日本語は低域〜中域の母音が非常に強く、ピッチが平坦。

            let lowRange = 0;  // 100-800Hz (日本語の母音)
            let highRange = 0; // 3kHz-8kHz (英語の子音)
            for(let i=0; i<40; i++) lowRange += dataArray[i];
            for(let i=150; i<400; i++) highRange += dataArray[i];

            // 1. スペクトル形状の複雑さを計算 (英語は複雑、日本語は単純)
            let complexity = 0;
            for(let i=10; i<200; i++) complexity += Math.abs(dataArray[i] - dataArray[i-1]);

            // 2. 言語判定スコアリング
            if (lowRange > 1000) { // 声が出ている時だけ判定
                const jpPattern = lowRange / (highRange + 1);
                
                // 日本語的な平坦な音響パターンを検知
                if (jpPattern > 15 || complexity < 1500) {
                    englishScore -= 4;
                } else if (jpPattern < 6 && complexity > 2500) {
                    englishScore += 2;
                }
            } else {
                englishScore = (englishScore * 0.95) + (50 * 0.05); // 静寂時はニュートラルへ
            }

            englishScore = Math.max(0, Math.min(100, englishScore));
            document.getElementById('prob-bar').style.width = englishScore + "%";

            // 0%（純粋な日本語/雑音）に達したら即遮断
            if (englishScore <= 0) {
                triggerWarning("DETECTED: NON-ENGLISH_ACOUSTIC_PROFILE");
                return;
            }

            requestAnimationFrame(scan);
        }
        scan();
    }

    function triggerWarning(reason) {
        document.getElementById('warning-screen').style.display = 'flex';
        document.getElementById('alert-reason').innerText = reason;
        if(audioCtx) audioCtx.close();
    }

    document.getElementById('start-btn').onclick = initAI;
</script>
"""

components.html(st_js, height=650)
