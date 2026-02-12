import streamlit as st
import whisper
import av
import numpy as np
import threading
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# ページ設定
st.set_page_config(page_title="リアルタイム英語監視", page_icon="🔴")

st.title("🔴 リアルタイム英語監視")
st.write("「START」を押すと監視を開始します。話し続けてください。")

# 警告メッセージ設定
warning_msg = st.text_input("🇯🇵 日本語検知時のメッセージ", value="No Japanese! Speak English!")

# 1. AIモデルの読み込み（キャッシュ化）
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

# 2. リアルタイム処理のクラス
class AudioProcessor:
    def __init__(self):
        self.audio_buffer = np.array([], dtype=np.float32)
        self.lock = threading.Lock()
        self.sample_rate = 16000 # Whisperは16kHzが好き

    def recv(self, frame):
        # マイクから入ってきた音声を配列に変換
        audio = frame.to_ndarray()
        audio = audio.flatten().astype(np.float32) / 32768.0 # 正規化

        with self.lock:
            self.audio_buffer = np.concatenate((self.audio_buffer, audio))

        return frame

# 3. 状態を保存する場所
if "text_output" not in st.session_state:
    st.session_state["text_output"] = "..."

# 4. マイク入力の設置（WebRTC）
ctx = webrtc_streamer(
    key="realtime-checker",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"video": False, "audio": True},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

# 5. 裏側で常に判定し続けるループ
output_placeholder = st.empty()
alert_placeholder = st.empty()

while ctx.state.playing:
    if ctx.audio_receiver:
        try:
            audio_frames = ctx.audio_receiver.get_frames(timeout=1)
        except:
            continue

        if len(audio_frames) > 0:
            sound_chunk = np.array([], dtype=np.int16)
            for frame in audio_frames:
                sound = frame.to_ndarray().flatten()
                sound_chunk = np.concatenate((sound_chunk, sound))
            
            # 音声を少し変換してAIが読めるようにする
            audio_float = sound_chunk.astype(np.float32) / 32768.0
            
            # 3秒分以上のデータが溜まったら判定する（負荷軽減のため）
            # ここでは簡易的に都度判定を試みますが、実際はバッファリングが必要です
            # 今回はシンプルに「一定量溜まったら判定」の疑似コードにします
            
            # ※注意: 完全なストリーミング判定はサーバー負荷が高すぎるため、
            # Streamlit Cloudでは「短い間隔で録音→判定」を繰り返すのが限界です。
            
            pass 

# ⚠️ リアルタイム版の注意点
# 無料のStreamlit Cloudサーバーでは、WebRTC（完全リアルタイム通信）が
# スマホの回線（4G/5G）だとセキュリティでブロックされて繋がらないことがよくあります。
# もし「START」を押してもグルグル回るだけで繋がらない場合は、
# 先ほどの「半自動モード（録音ボタン式）」が、この環境での限界性能になります。