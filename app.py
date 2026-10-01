import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# جلب مفتاح Hugging Face المجاني من متغيرات البيئة في Render
HF_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')

# استخدام نموذج مجاني سريع لتوليد النصوص، الأفكار، أو السكريبتات
API_URL = (
    'https://api-inference.huggingface.co/models/google/flan-t5-large'  # نموذج مجاني
)


@app.route('/generate', methods=['POST'])
def generate():
  try:
    task_mode = request.form.get('mode', 'text-to-video')
    prompt = request.form.get('prompt', '')

    print(f'--- تنفيذ مهمة عبر Hugging Face: {task_mode} ---')
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

    # إرسال الطلب إلى نموذج Hugging Face المجاني
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    # استخراج النتيجة النصية أو الرد الذكي
    generated_text = 'تمت المعالجة بنجاح'
    if isinstance(result, list) and len(result) > 0:
      generated_text = result[0].get('generated_text', str(result))
    elif isinstance(result, dict) and 'generated_text' in result:
      generated_text = result['generated_text']

    # إرجاع النتيجة لعرضها على منصة Snina Ai في مدونتك
    return jsonify({
        'success': True,
        'video_url': (  # رابط فيديو توضيحي مؤقت لعرض النتيجة ريثما نطور عارض الوسائط
            'https://www.w3schools.com/html/mov_bbb.mp4'
        ),
        'message': generated_text,
    })

  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
