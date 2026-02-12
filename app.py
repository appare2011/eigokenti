import streamlit as st
import whisper
import os

st.title("🗣️ 英語オンリー・チェッカー")
st.write("日本語を話すとカウントが増えちゃうよ！")

# データの初期化
if 'count' not in st.session_state:
    st.session_state.count = 0

# モデルの読み込み
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

# 音声ファイルのアップロード（Web版は録音ファイルをアップするのが一番簡単）
audio_file = st.audio_input("マイクボタンを押して英語で話してみてね")

if audio_file:
    # 一時保存
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.read())
    
    # AIで判定
    result = model.transcribe("temp_audio.wav")
    lang = result['language']
    text = result['text']

    if lang == 'ja':
        st.session_state.count += 1
        st.error(f"❌ 日本語を検知: 「{text}」")
        st.warning("⚠️ 英語を話してください！")
    else:
        st.success(f"✅ English OK: {text}")

st.divider()
st.header(f"📊 日本語を話した回数: {st.session_state.count} 回")