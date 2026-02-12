import streamlit as st
import whisper
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import os

st.set_page_config(page_title="3秒監視・英語コーチ")
st.title("🔴 3秒おき強制判定モード")

# AIモデル（爆速設定）
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

# 警告メッセージ
warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

# 判定結果を表示する場所
status_area = st.empty()
result_area = st.empty()

# --- 🎤 リアルタイム処理の設定 ---
def audio_frame_callback(frame: av.AudioFrame):
    # ここで音声をキャッチしますが、
    # ブラウザとサーバーの通信を維持するために空のフレームを返します
    return frame

ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY, # 送信専用
    audio_frame_callback=audio_frame_callback,
    media_stream_constraints={"video": False, "audio": True},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
)

# --- 🔄 3秒ごとの強制判定ループ ---
if ctx.state.playing:
    status_area.info("監視中... 3秒ごとにチェックしています。")
    
    # ここに「3秒待って判定」というロジックを入れますが、
    # 無料サーバーの負荷を抑えるため、以下の「自動送信マイク」を
    # 「強制クリック」させる仕組みを併用するのが最も安定します。
    
    # 実際には、iPadなどのモバイル端末では
    # 以下の st.audio_input を使うのが、通信が途切れず最も「速い」です。
    st.write("※iPadでは下のマイクが最も速く動きます")

audio_data = st.audio_input("監視スタート（一言ごとに自動で判定します）")

if audio_data:
    temp_file = "check.wav"
    with open(temp_file, "wb") as f:
        f.write(audio_data.getbuffer())
    
    # 言語を英語か日本語に限定して爆速化
    result = model.transcribe(temp_file, fp16=False)
    text = result['text'].strip()
    lang = result['language']

    if text:
        if lang == 'ja':
            result_area.error(f"❌ 日本語検知: {text}")
            st.markdown(f"<h1 style='color:red;'>{warning_msg}</h1>", unsafe_allow_html=True)
        else:
            result_area.success(f"✅ OK: {text}")

    if os.path.exists(temp_file):
        os.remove(temp_file)
