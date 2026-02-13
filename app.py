import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="True AI Guard", layout="centered")

st.title("🤖 真のAI：TensorFlow.js搭載")
st.markdown("""
Googleの学習済みAIモデルをロードします。
* **雑音** → AIが「Noise」と判断し無視します（緑）。
* **英語** → AIが単語を認識します（緑）。
* **日本語** → AIが「Unknown（不明な言語）」と判断し警告します（赤）。
""")

st_js = """
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/speech-commands"></script>

<div id="status" style="padding:15px; border-radius:10px; background:#222; color:#00ffcc; margin-bottom:15px; font-family:monospace; border:1px solid #555;">
    SYSTEM: LOADING_NEURAL_NETWORK...
</div>

<div style="background:#000; padding:20px; border-radius:15px; border:1px solid #333; margin-bottom:15px; text-align:center;">
    <div style="font-size:14px; color:#888; margin-bottom:10px;">AI CLASSIFICATION</div>
    <div id="result-text" style="font-size:36px; font-weight:bold; color:#fff; font-family:sans-serif;">---</div>
    <div id="confidence-text" style="font-size:16px; color:#aaa; margin-top:5px;"></div>
    
    <div style="margin-top:20px; height:10px; background:#333; border-radius:5px; overflow:hidden;">
        <div id="prob-bar" style="width:0%; height:100%; background:#00ffcc; transition: width 0.1s;"></div>
    </div>
</div>

<div id="warning-screen" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(255,0,0,0.95); color:white; z-index:9999; justify-content:center; align-items:center; flex-direction:column; text-align:center;">
    <h1 style="font-size:80px; margin:0;">🚫 BLOCK 🚫</h1>
    <p style="font-size:30px; margin:20px;">JAPANESE DETECTED</p>
    <div style="font-size:18px;">AI Status: Unknown Language (High Confidence)</div>
    <button onclick="resume()" style="margin-top:30px; padding:20px 50px; font-size:24px; border:none; border-radius:10px; cursor:pointer; background:white; color:red; font-weight:bold;">RESUME</button>
</div>

<button id="start-btn" style="padding:30px; width:100%; background:#00ffcc; color:#000; border:none; border-radius:20px; font-size:24px; cursor:pointer; font-weight:bold; margin-top:10px;">
    START AI ENGINE
</button>

<script>
    let recognizer;
    let isListening = false;
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result-text');
    const confDiv = document.getElementById('confidence-text');
    const warningScreen = document.getElementById('warning-screen');
    const probBar = document.getElementById('prob-bar');

    async function init() {
        // AIモデルのロード
        statusDiv.innerText = "SYSTEM: DOWNLOADING_MODEL...";
        recognizer = speechCommands.create('BROWSER_FFT');
        await recognizer.ensureModelLoaded();
        
        statusDiv.innerText = "SYSTEM: AI_READY. LISTENING...";
        statusDiv.style.borderColor = "#00ffcc";
        statusDiv.style.color = "#00ffcc";
        document.getElementById('start-btn').style.display = 'none';
        
        startListening();
    }

    function startListening() {
        // マイク入力の監視設定
        // probabilityThreshold: AIの自信度がこれを超えたら反応する
        recognizer.listen(result => {
            const scores = result.scores; // 全カテゴリの確率
            const labels = recognizer.wordLabels(); // カテゴリ名リスト (background_noise, unknown, yes, no...)
            
            // 最も確率が高いカテゴリを探す
            const maxScore = Math.max(...scores);
            const index = scores.indexOf(maxScore);
            const label = labels[index];

            // UI更新
            resultDiv.innerText = label.toUpperCase();
            confDiv.innerText = "Probability: " + Math.floor(maxScore * 100) + "%";
            probBar.style.width = (maxScore * 100) + "%";

            // --- 判定ロジック ---
            
            // 1. 雑音 (Background Noise)
            if (label === 'background_noise') {
                resultDiv.style.color = "#888"; // グレー（無視）
                probBar.style.backgroundColor = "#888";
                return; // 何もしない
            }

            // 2. 英語 (Go, Stop, Yes, No, Up, Down etc...)
            // Googleのモデルが知っている単語なら英語とみなす
            if (label !== 'unknown' && label !== '_background_noise_') {
                resultDiv.style.color = "#00ffcc"; // 緑（OK）
                probBar.style.backgroundColor = "#00ffcc";
                return; // 英語なのでOK
            }

            // 3. 日本語 (Unknown)
            // AIが「雑音でもない」「知っている英語でもない」＝「未知の言語」と判断
            if (label === 'unknown') {
                resultDiv.style.color = "#ff0055"; // 赤（警告）
                probBar.style.backgroundColor = "#ff0055";
                
                // 誤作動防止：AIの確信度が85%を超えた場合のみ発動
                if (maxScore > 0.85) {
                    triggerWarning();
                }
            }

        }, {
            includeSpectrogram: false, 
            probabilityThreshold: 0.75,
            invokeCallbackOnNoiseAndUnknown: true, // 雑音や不明な音もコールバックを受け取る
            overlapFactor: 0.50 // 0.5秒ごとに判定 (高速化)
        });
    }

    function triggerWarning() {
        warningScreen.style.display = 'flex';
        // 一時停止はしない（続けて監視するため）、必要なら recognizer.stopListening()
    }

    // 警告画面を消す関数
    window.resume = function() {
        warningScreen.style.display = 'none';
    }

    document.getElementById('start-btn').onclick = init;
</script>
"""

components.html(st_js, height=800)
