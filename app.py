import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/generate', methods=['POST'])
def generate():
  try:
    task_mode = request.form.get('mode', 'text-to-video')
    prompt = request.form.get('prompt', '')
    media_file = request.files.get('media')

    print(
        f'الوضع المطلوب: {task_mode} | البرومبت: {prompt} | ملف مرفق: {bool(media_file)}'
    )

    # رابط تجريبي تفاعلي مؤقت للتأكد من ربط الواجهة
    result_video_url = 'https://www.w3schools.com/html/mov_bbb.mp4'

    return jsonify({'success': True, 'video_url': result_video_url})

  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
