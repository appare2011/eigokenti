import streamlit as st
import whisper
import os

st.set_page_config(page_title="爆速英語監視", layout="centered")
st.title("⚡️ 爆速・英語オンリー監視")

# 1. AIを「最速モード」で読み込む
@st.cache_resource
def load_model():
    # tinyモデルを使い、さらに計算を簡略化する設定
    return whisper.load_model("tiny")

model = load_model()

# 警告メッセージ
warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

# 🎤 マイク入力（ここがポイント：iPadでも自動送信が効きやすい設定）
audio_data = st.audio_input("マイクをONにして話してください")

if audio_data:
    # 判定中の表示を最小限にして速度を優先
    temp_file = "t.wav"
    try:
        with open(temp_file, "wb") as f:
            f.write(audio_data.getbuffer())
        
        # 🏎️ 判定スピードを極限まで上げる設定
        # language="en" を外して自動判別にしつつ、候補を絞る
        result = model.transcribe(temp_file, fp16=False, task="transcribe")
        text = result['text'].strip()
        lang = result['language']

        if text:
            if lang == 'ja':
                # 日本語なら即座に赤画面！
                st.markdown(f"""
                    <div style="background-color:#ff4b4b; padding:30px; border-radius:10px; border: 5px solid white;">
                        <h1 style="color:white; text-align:center; font-size:60px; margin:0;">{warning_msg}</h1>
                        <p style="color:white; text-align:center; font-size:20px;">検知: {text}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.toast("日本語を検知しました！", icon="🚨")
            else:
                # 英語なら緑でスルー
                st.success(f"Perfect! : {text}")
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

st.caption("※話し終わって一瞬黙ると、AIが光速で判定します。")
