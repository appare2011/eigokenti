import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Pitch Monitor", layout="centered")

st.title("🛡️ 成功事例ベース：ピッチ分散AI監視")
st.write("文字起こし機能は使いません。ピッチ（音の高さ）の動的な変化で言語を特定します。")

st_js = """
<div id="status" style="padding:15px; border-radius:10px; background:#000; color:#00ff00; margin-bottom:15px; font-family:monospace; border:1px solid #00ff00;">
    AI_STATUS: ANALYZING_PITCH_DYNAMICS
</div>

<div style="background:#111; padding:20px; border-radius:10px; border:1px solid #333; margin-bottom:15px;">
    <div style="color:#888; font-size:12px; margin-bottom:10px; font-family:monospace;">PITCH_VARIATION_SCORE (ENGLISH_INDICATOR)</div>
    <div style="width:100%; height:40px; background:#222; border-radius:20px; overflow:hidden; border: 2px solid #444;">
        <div id="score-bar" style="width:50%; height:100%; background:linear-gradient(90deg, #ff0000, #00ff00); transition: width 0.1s;"></div>
    </div>
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#000; color:#ff0000; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; border: 25px solid #ff0000;">
    <h1 style="font-size:70px; margin:0; font-family:Impact;">🚨 INVALID DYNAMICS 🚨</h1>
    <p id="alert-reason" style="font-size:24px; margin:20px; color:#fff; font-family:monospace;"></p>
    <button onclick="location.reload()" style="padding:25px 50px; font-size:24px; cursor:pointer; background:#ff0000; color:#fff; border:none; border-radius:10px; font-weight:bold;">REBOOT ENGINE</button>
</div>

<button id="start-btn" style="padding:30px; width:100%; background:#000; color:#00ff00; border:2px solid #00ff00; border-radius:20px; font-size:26px; cursor:pointer; font-weight:bold; font-family:monospace;">
    ACTIVATE PITCH AI
</button>

<script>
    let audioCtx, analyser, processor;
    let englishScore = 50;
    let prevPitch = 0;

    async function initAI() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        const source = audioCtx.createMediaStreamSource(stream);
        
        processor = audioCtx.createScriptProcessor(2048, 1, 1);
        source.connect(analyser);
        analyser.connect(processor);
        processor.connect(audioCtx.destination);

        document.getElementById('start-btn').style.display = 'none';

        processor.onaudioprocess = function(e) {
            const buffer = e.inputBuffer.getChannelData(0);
            
            // --- オートコリレーションによる簡易ピッチ検出 ---
            let sum = 0;
            for(let i=0; i<buffer.length; i++) sum += buffer[i]*buffer[i];
            let rms = Math.sqrt(sum/buffer.length);
            
            if (rms > 0.02) { // 発声中
                // ピッチの変化（動き）を計測
                let currentPitch = detectPitch(buffer);
                let diff = Math.abs(currentPitch - prevPitch);
                
                // 成功しているスクリプトの閾値：
                // 英語は文中でピッチが大きく動く。日本語や雑音は一定になりやすい。
                if (diff > 2 && diff < 50) { 
                    englishScore += 2; // 英語らしい動き
                } else {
                    englishScore -= 1.5; // 日本語的な平坦さ
                }
                prevPitch = currentPitch;
            } else {
                englishScore *= 0.99; // 静寂
            }

            englishScore = Math.max(0, Math.min(100, englishScore));
            document.getElementById('score-bar').style.width = englishScore + "%";

            if (englishScore <= 0) {
                triggerWarning("DETECTED: FLAT_PITCH_PATTERN (JAPANESE/NOISE)");
            }
        };
    }

    // 基本周波数(F0)を推定する関数
    function detectPitch(buffer) {
        let maxCorr = -1;
        let bestLag = -1;
        for (let lag = 20; lag < 200; lag++) {
            let corr = 0;
            for (let i = 0; i < buffer.length - lag; i++) {
                corr += buffer[i] * buffer[i + lag];
            }
            if (corr > maxCorr) {
                maxCorr = corr;
                bestLag = lag;
            }
        }
        return 44100 / bestLag;
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
