import streamlit as st
import whisper
import os

# ページ設定
st.set_page_config(page_title="リアルタイム英語監視", layout="centered")

st.title("🔴 英語オンリー監視中")

# 1. AIモデルの準備（読み込み状況を表示）
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

with st.sidebar:
    st.write("AI準備状況:")
    model = load_model()
    st.success("AI Ready!")

# 2. 警告メッセージの設定
warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

st.write("---")

# 3. 録音と判定（ここがメイン）
# st.audio_inputは「話し終わって1秒」で自動的にデータを送ります
audio_data = st.audio_input("マイクをオンにして英語を話してください")

# 結果を出すための「専用スペース」をあらかじめ確保
display_area = st.empty()

if audio_data:
    # 判定中は「...」と出す
    display_area.info("AIがあなたの声を聴いています...")
    
    temp_file = "temp_voice.wav"
    try:
        with open(temp_file, "wb") as f:
            f.write(audio_data.getbuffer())
        
        # Whisper AIで解析
        result = model.transcribe(temp_file)
        lang = result['language']
        text = result['text'].strip()

        if text:
            if lang == 'ja':
                # 【ここが重要】日本語なら画面を真っ赤にして警告を出す
                display_area.error(f"❌ 日本語を検知: 「{text}」")
                st.markdown(f"<h1 style='text-align: center; color: red; font-size: 80px;'>{warning_msg}</h1>", unsafe_allow_html=True)
                st.toast(warning_msg, icon="⚠️")
            else:
                # 英語なら緑色で出す
                display_area.success(f"✅ English OK: {text}")
                st.balloons() # 英語なら風船を飛ばして褒める
        else:
            display_area.warning("声が聞き取れませんでした。もう少しはっきり話してみて！")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

st.divider()
st.caption("※話し終わった後、1秒くらい黙ると自動で判定が始まります。")
