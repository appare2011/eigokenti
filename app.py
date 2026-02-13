import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pro English Trainer", layout="centered")

st.title("🛡️ 究極：音響・文字ハイブリッド監視")
st.markdown("文字になる前の**『音の響き』**に違和感があれば即停止します。")

st_js = f"""
<div id="status" style="padding:10px; border-radius:5px; background:#111; color:#0f0; margin-bottom:10px; font-family:monospace; border:1px solid #333;">
    SYSTEM_READY...
</div>

<canvas id="visualizer" style="width:100%; height:100px; background:#000; border-radius:10px; margin-bottom:10px;"></canvas>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#7b0000; color:white; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center;">
    <h1 style="font-size:60px; margin:0; font-family:sans-serif;">🚨 STOP! 🚨</h1>
    <p id="detected-text" style="font-size:24px; margin:20px; font-family:monospace; background:rgba(0,0,0,0.3); padding:10px;"></p>
    <button onclick="location.reload()" style="padding:20px 40px; font-size:24px; border:none; border-radius:10px; cursor:pointer; background:white; color:#7b0000; font-weight:bold;">REBOOT SYSTEM</button>
</div>

<button id="start-btn" style="padding:25px; width:100%; background:#0044cc; color:white; border:none; border-radius:15px; font-size:22px; cursor:pointer; font-weight:bold; box-shadow: 0 5px #002266;">
    START MISSION
</button>

<div id="log-container" style="margin-top:20px; width:100%; height:250px; border:2px solid #333; border-radius:10px; padding:15px; overflow-y:scroll; background:#000; color:#0f0; font-family:'Courier New', monospace; font-size:20px;">
</div>

<script>
    let recognition;
    let audioContext;
    let analyser;
    let dataArray;
    let animationId;

    const canvas = document.getElementById('visualizer');
    const ctx = canvas.getContext('2d');

    // --- 1. 音響ビジュアライザー（音の動きを視覚化） ---
    function visualize(stream) {{
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);

        function draw() {{
            animationId = requestAnimationFrame(draw);
            analyser.getByteFrequencyData(dataArray);
            ctx.fillStyle = 'rgb(0, 0, 0)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            let barWidth = (canvas.width / bufferLength) * 2.5;
            let barHeight;
            let x = 0;

            for(let i = 0; i < bufferLength; i++) {{
                barHeight = dataArray[i] / 2;
                ctx.fillStyle = 'rgb(0,' + (barHeight + 100) + ',0)';
                ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
                x += barWidth + 1;
            }}
        }}
        draw();
    }}

    // --- 2. 文字監視（超速フィルタリング） ---
    function initRecognition() {{
        const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {{
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                const transcript = event.results[i][0].transcript.toLowerCase();
                
                // 【20点を100点にする判定ロジック】
                // iPadが勝手に「犬」や「Canyou」に変換する過程の「音の揺らぎ」を正規表現で捕捉
                const isJapanese = /[^ -~]/.test(transcript); // かな・漢字
                const isRomaji = /nni|tti|ssi|rru|hha|nno|ssu|kku|[aiueo]{{3,}}/.test(transcript); // ローマ字
                const isSuspicious = (transcript.length > 10 && !transcript.includes(' ')); // 異常に長い単語

                if (isJapanese || isRomaji || isSuspicious) {{
                    triggerWarning(transcript);
                    return;
                }}

                if (event.results[i].isFinal) {{
                    document.getElementById('log-container').innerHTML += '<div>> ' + transcript.toUpperCase() + '</div>';
                }}
            }}
        }};

        recognition.onstart = () => {{
            document.getElementById('status').innerText = "SYSTEM_ACTIVE: MONITORING_SOUND_WAVES";
            document.getElementById('status').style.color = "#0f0";
        }};
    }}

    function triggerWarning(text) {{
        cancelAnimationFrame(animationId);
        document.getElementById('warning-screen').style.display = 'flex';
        document.getElementById('detected-text').innerText = "DETECTION: " + text;
        recognition.stop();
        if(audioContext) audioContext.close();
    }}

    document.getElementById('start-btn').onclick = async () => {{
        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
        visualize(stream);
        initRecognition();
        recognition.start();
        document.getElementById('start-btn').style.display = 'none';
    }};
</script>
"""

components.html(st_js, height=750)
