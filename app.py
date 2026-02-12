import streamlit as st
import whisper
import os

# 📱 スマホで見やすくする設定
st.set_page_config(page_title="英語チェッカー", page_icon="🗣️", layout="centered")

# --- 🛠️ 1. 設定エリア ---
st.title("🗣️ 英語オンリー・アプリ")

# 警告メッセージの入力欄（デフォルト値を設定）
warning_msg = st.text_input(
    "🇯🇵 日本語を検知した時のセリフ",
    value="No Japanese! Speak English!",
    placeholder="例：罰金100万円！"
)

st.write("---")

# --- 🧠 2. AIの準備（キャッシュ機能で高速化） ---
# スマホ・タブレットで重くならないよう、一度読み込んだら記憶させます
@st.cache_resource
def load_model():
    # 最も軽量で高速な 'tiny' モデルを使用
    return whisper.load_model("tiny")

# モデル読み込み中はスピナーを表示
with st.spinner("AIを準備しています..."):
    model = load_model()

# --- 🎤 3. 録音と判定 ---
# audio_inputはスマホのブラウザでも動作が安定しています
audio_file = st.audio_input("マイクボタンを押して話してください")

if audio_file:
    # 判定中の表示
    with st.spinner('判定中...'):
        temp_filename = "temp_audio.wav"
        
        try:
            # 音声データを一時ファイルとして保存
            with open(temp_filename, "wb") as f:
                f.write(audio_file.getbuffer())
            
            # ファイルが正しく保存されたか確認してからAIに渡す
            if os.path.exists(temp_filename):
                # AIによる文字起こしと判定
                result = model.transcribe(temp_filename)
                lang = result['language']
                text = result['text'].strip()

                # 何も喋っていない（ノイズだけ）の場合は無視
                if text:
                    if lang == 'ja':
                        # 🇯🇵 日本語の場合
                        st.error(f"❌ Detected Japanese: 「{text}」")
                        # 入力されたメッセージを大きく表示
                        st.markdown(f"# 📢 {warning_msg}")
                        # スマホ画面下にも通知
                        st.toast(warning_msg, icon="⚠️")
                    else:
                        # 🇺🇸 英語の場合
                        st.success(f"✅ English OK: {text}")
                        st.toast("Good Job!", icon="👍")
                else:
                    st.info("声が小さすぎるか、聞き取れませんでした。")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            
        finally:
            # 🧹 お掃除処理：使い終わったファイルは必ず消す
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

st.divider()
st.caption("※スマホの場合、マナーモードを解除すると音が拾いやすくなります。")