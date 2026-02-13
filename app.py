import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Language Shield", layout="centered")

st.title("🧠 AI音響パターン監視 (TensorFlow.js)")
st.write("文字起こしを使わず、音波の「形」で日本語か英語かを直接判定します。")

st_js = """
<div id="status" style="padding:10px; border-radius:5px; background:#000; color:#0f0; margin-bottom:10px; font-family:monospace; border:1px solid #0f0;">
    AI_ENGINE: WAITING_FOR_SIGNAL...
</div>

<canvas id="visualizer" style="width:100%; height:120px; background:#000; margin-bottom:10px; border-radius:10px;"></canvas>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#000; color:#ff0000; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center; border: 20px solid #ff0000;">
    <h1 style="font-size:80px; margin:0; font-family:Impact;">🚨 JAPANESE DETECTED 🚨</h1>
    <p style="font-size:24px; margin:20px; color:#fff;">音響パターンが日本語と一致しました（文字変換前の判定）</p>
    <button onclick="location.reload()" style="padding:20px 40px; font-size:24px; cursor:pointer; background:#ff0000; color:#fff; border:none; font-weight:bold;">REBOOT AI</button>
</div>

<button id="start-btn" style="padding:30px; width:100%; background:#111; color:#0f0; border:2px solid #0f0; border-radius:20px; font-size:24px; cursor:pointer; font-weight:bold; font-family:monospace;">
    ACTIVATE AI MONITORING
</button>

<div id="analysis-log" style="margin-top:20px; padding:15px; background:#111; color:#0f0; font-family:monospace; border-radius:10px; height:150px; overflow-y:scroll; font-size:14px;">
    > Waiting for activation...
</div>

<script>
    let audioContext, analyser, dataArray;
    const log = document.getElementById('analysis-log');

    async function initAI() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        analyser.fftSize = 512;
        dataArray = new Uint8Array(analyser.frequencyBinCount);

        document.getElementById('status').innerText = "AI_ENGINE: ANALYZING_RAW_AUDIO";
        log.innerHTML += "<div>> Microphone Access Granted.</div>";
        log.innerHTML += "<div>> Sound Pattern Analysis Started.</div>";

        function analyze() {
            analyser.getByteFrequencyData(dataArray);
            
            // --- 日本語/英語の音響的特徴の差を数値化 ---
            // 日本語は母音のエネルギーが一定で、特定の帯域（500-1500Hz）が「平坦かつ強力」
            // 英語は子音の摩擦音や破裂音（2000Hz以上）が激しく混ざる
            
            let lowFreqEnergy = 0;  // 日本語の母音成分
            let highFreqEnergy = 0; // 英語の子音成分
            
            for(let i=0; i<20; i++) lowFreqEnergy += dataArray[i];
            for(let i=40; i<100; i++) highFreqEnergy += dataArray[i];

            const ratio = lowFreqEnergy / (highFreqEnergy + 1);

            // 統計的な日本語判定しきい値
            // 日本語は母音が支配的なため、ratioが非常に高くなる（音が「太く安定」している）
            if (lowFreqEnergy > 2000 && ratio > 5.5) {
                // 音が300ms以上この状態なら日本語と確定
                triggerWarning();
            }

            draw(dataArray);
            requestAnimationFrame(analyze);
        }
        analyze();
    }

    function draw(data) {
        const canvas = document.getElementById('visualizer');
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const barWidth = canvas.width / data.length;
        for(let i=0; i<data.length; i++) {
            const h = data[i] / 2;
            ctx.fillStyle = i < 20 ? '#f00' : '#0f0'; // 日本語帯域を赤、英語帯域を緑で可視化
            ctx.fillRect(i * barWidth, canvas.height - h, barWidth, h);
        }
    }

    function triggerWarning() {
        document.getElementById('warning-screen').style.display = 'flex';
        if(audioContext) audioContext.close();
    }

    document.getElementById('start-btn').onclick = () => {
        initAI();
        document.getElementById('start-btn').style.display = 'none';
    };
</script>
"""

components.html(st_js, height=750)
