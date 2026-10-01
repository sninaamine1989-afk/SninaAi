import base64
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')

# استخدام نموذج مجاني قوي لتوليد الصور من النصوص (Stable Diffusion)
API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1'


@app.route('/generate', methods=['POST'])
def generate():
  try:
    task_mode = request.form.get('mode', 'text-to-video')
    prompt = request.form.get('prompt', '')

    print(f'--- تنفيذ طلب الوسائط: {prompt} ---')

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

    # إرسال الطلب لنموذج توليد الصور
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code == 200:
      # تحويل الصورة القادمة من الذكاء الاصطناعي إلى صيغة تظهر مباشرة في المتصفح
      image_bytes = response.content
      image_base64 = base64.b64encode(image_bytes).decode('utf-8')
      image_url = f'data:image/jpeg;base64,{image_base64}'

      return jsonify({
          'success': True,
          'video_url': (  # سنستخدم نفس الحقل لعرض النتيجة البصرية
              image_url
          ),
          'message': f'تم توليد الوسائط بنجاح بناءً على طلبك: "{prompt}"',
      })
    else:
      return (
          jsonify({
              'success': False,
              'error': (
                  'النموذج يحمل حالياً أو يتم تجهيزه، حاول مرة أخرى بعد قليل.'
              ),
          }),
          500,
      )

  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
