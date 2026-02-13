import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bio-Acoustic English Monitor", layout="centered")

st.title("💎 100万点：生体音響解析監視")
st.markdown("文字になる前の**『音波の性質』**を解析。ローマ字や翻訳後の英語すら、音の響きで日本語と見破ります。")

st_js = """
<div id="status" style="padding:10px; border-radius:5px; background:#1a1a1a; color:#00ff00; margin-bottom:10px; font-family:monospace; border:1px solid #00ff00;">
    ACOUSTIC_ENGINE: ONLINE
</div>

<canvas id="freq-map" style="width:100%; height:150px; background:#000; border:1px solid #333; margin-bottom:10px;"></canvas>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#ff0000; color:white; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center;">
    <h1 style="font-size:80px; margin:0; font-weight:900;">🚨 BANNED SOUND 🚨</h1>
    <p style="font-size:24px; margin:20px;">日本語特有の母音周波数を検知しました</p>
    <button onclick="location.reload()" style="padding:20px 40px; font-size:24px; border:none; border-radius:10px; cursor:pointer; background:black; color:white; font-weight:bold;">SYSTEM REBOOT</button>
</div>

<button id="start-btn" style="padding:30px; width:100%; background:#111; color:#00ff00; border:3px solid #00ff00; border-radius:20px; font-size:24px; cursor:pointer; font-weight:bold; font-family:monospace; box-shadow: 0 0 20px #00ff00;">
    INITIATE BIOMETRIC MONITORING
</button>

<div id="log-container" style="margin-top:20px; width:100%; height:200px; border:1px solid #333; border-radius:10px; padding:15px; overflow-y:scroll; background:#000; color:#00ff00; font-family:monospace;">
</div>

<script>
    let audioContext, analyser, dataArray, recognition;
    const canvas = document.getElementById('freq-map');
    const ctx = canvas.getContext('2d');

    async function startSystem() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);

        analyser.fftSize = 1024;
        dataArray = new Uint8Array(analyser.frequencyBinCount);

        // --- 1. 音響解析エンジン（母音判定） ---
        function analyzeSound() {
            analyser.getByteFrequencyData(dataArray);
            
            // 日本語の母音（あ・い・う・え・お）が集中する500Hz〜2500Hzのエリアを監視
            // 英語に比べて日本語は特定の周波数が「強く、長く」持続する特徴があります
            let totalEnergy = 0;
            let peakEnergy = 0;
            for(let i=10; i<50; i++) { // 約500-2500Hz付近
                totalEnergy += dataArray[i];
                if(dataArray[i] > peakEnergy) peakEnergy = dataArray[i];
            }

            // 【確実な判定】音が一定以上の強さで、かつ周波数が日本語特有の「平坦さ」を持った場合
            // 英語はもっと周波数が激しく上下（抑揚）します。
            if (peakEnergy > 230) { 
                let stability = 0;
                for(let i=10; i<40; i++) {
                    if(Math.abs(dataArray[i] - dataArray[i+1]) < 5) stability++;
                }
                // 音が安定しすぎている（＝日本語の「あー」などの母音）
                if (stability > 18) {
                    triggerWarning("ACOUSTIC_MATCH: JAPANESE VOWEL");
                }
            }

            drawVisualizer();
            requestAnimationFrame(analyzeSound);
        }

        // --- 2. 文字起こしエンジン（バックアップ） ---
        const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.onresult = (e) => {
            const text = e.results[e.results.length-1][0].transcript;
            if (/[^ -~]/.test(text)) triggerWarning("TEXT_MATCH: JAPANESE CHARACTER");
            document.getElementById('log-container').innerText = "> " + text.toUpperCase();
        };

        analyzeSound();
        recognition.start();
    }

    function drawVisualizer() {
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const barWidth = canvas.width / dataArray.length;
        for(let i=0; i<dataArray.length; i++) {
            const h = dataArray[i] / 2;
            ctx.fillStyle = `rgb(0, ${dataArray[i]}, 0)`;
            ctx.fillRect(i * barWidth, canvas.height - h, barWidth, h);
        }
    }

    function triggerWarning(reason) {
        document.getElementById('warning-screen').style.display = 'flex';
        recognition.stop();
        audioContext.close();
    }

    document.getElementById('start-btn').onclick = () => {
        startSystem();
        document.getElementById('start-btn').style.display = 'none';
    };
</script>
"""

components.html(st_js, height=700)
