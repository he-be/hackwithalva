"""Webアプリケーション"""
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import settings

# LM Studio (OpenAI互換) クライアント設定
client = OpenAI(
    base_url=settings.OPENAI_BASE_URL,
    api_key=settings.OPENAI_API_KEY
)

# チャット履歴（サーバー起動中は維持）
chat_history = [
    {"role": "system", "content": settings.SYSTEM_INSTRUCTION}
]

app = Flask(__name__)

@app.route('/')
def index():
    """メインページ表示"""
    config = {
        'typewriter_delay': settings.TYPEWRITER_DELAY_MS,
        'avatar_name': settings.AVATAR_NAME,
        'avatar_full_name': settings.AVATAR_FULL_NAME,
        'mouth_animation_interval': settings.MOUTH_ANIMATION_INTERVAL_MS,
        'beep_frequency': settings.BEEP_FREQUENCY_HZ,
        'beep_duration': settings.BEEP_DURATION_MS,
        'beep_volume': settings.BEEP_VOLUME,
        'beep_volume_end': settings.BEEP_VOLUME_END,
        'avatar_image_idle': settings.AVATAR_IMAGE_IDLE,
        'avatar_image_talk': settings.AVATAR_IMAGE_TALK
    }
    return render_template('index.html', config=config)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """ユーザー入力を受信しAI応答を返す"""
    message = request.json['message']

    # ユーザーメッセージを履歴に追加
    chat_history.append({"role": "user", "content": message})

    # LM Studioへチャット補完をリクエスト
    completion = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=chat_history,
    )

    ai_text = completion.choices[0].message.content

    # アシスタント応答を履歴に追加
    chat_history.append({"role": "assistant", "content": ai_text})

    return jsonify({'response': ai_text})

if __name__ == '__main__':
    app.run(debug=settings.DEBUG_MODE, port=settings.SERVER_PORT)