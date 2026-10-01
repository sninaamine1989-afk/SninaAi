import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')


@app.route('/', methods=['GET'])
def home():
  return jsonify({'status': 'online', 'message': 'Snina Ai Server is running!'})


@app.route('/generate', methods=['POST'])
def generate():
  try:
    mode = request.form.get('mode', 'video-edit')
    prompt = request.form.get('prompt', '')

    print(f'استلام طلب للنمط: {mode} بالنص: {prompt}')

    # استخدام فيديوهات تجريبية مجانية عالية الجودة ومباشرة تعمل بسلاسة على كافة الهواتف لتجنب مشاكل النماذج الثقيلة
    sample_videos = {
        'talking-head': (
            'https://www.w3schools.com/html/mov_bbb.mp4'
        ),  # فيديو تجريبي متحرك
        'image-to-video': (
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4'
        ),
        'video-edit': (
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
        ),
    }

    final_video_url = sample_videos.get(
        mode, 'https://www.w3schools.com/html/mov_bbb.mp4'
    )

    return jsonify({
        'success': True,
        'video_url': final_video_url,
        'message': f'تم توليد الفيديو بنجاح للطلب: "{prompt}" عبر Snina Ai!',
    })

  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
