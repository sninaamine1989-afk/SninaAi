import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')
API_URL = 'https://api-inference.huggingface.co/models/google/flan-t5-large'


@app.route('/generate', methods=['POST'])
def generate():
  try:
    task_mode = request.form.get('mode', 'text-to-video')
    prompt = request.form.get('prompt', '')

    print(f'--- تنفيذ مهمة: {task_mode} ---')
    print(f'المدخلات: {prompt}')

    if not HF_API_TOKEN:
      return (
          jsonify({
              'success': False,
              'error': (
                  'مفتاح Hugging Face غير موجود في إعدادات Render'
              ),
          }),
          400,
      )

    headers = {'Authorization': f'Bearer {HF_API_TOKEN}'}
    payload = {'inputs': prompt}

    generated_text = (
        f'تم استقبال طلبك بنجاح وتمت معالجة الفكرة: "{prompt}" عبر Snina Ai!'
    )

    try:
      response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
      if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
          generated_text = result[0].get('generated_text', generated_text)
        elif isinstance(result, dict) and 'generated_text' in result:
          generated_text = result['generated_text']
    except Exception as api_err:
      print(f'تنبيه اتصال خارجي: {api_err}')
      # الاستمرار بشكل طبيعي دون توقف السيرفر

    return jsonify({
        'success': True,
        'video_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
        'message': generated_text,
    })

  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
