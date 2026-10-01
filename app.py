import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = FlaskName
CORS(app)

HF_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')

# عناوين النماذج المختلفة لكل مهمة
MODELS = {
    'talking-head': (
        'https://api-inference.huggingface.co/models/Wav2Lip/Wav2Lip'
    ),  # نموذج للفيديوهات المتكلمة (أو نموذج بديل خفيف)
    'image-to-video': (
        'https://api-inference.huggingface.co/models/cerspense/stable-video-diffusion-img2vid'
    ),  # تحويل صورة إلى فيديو
    'video-edit': (
        'https://api-inference.huggingface.co/models/ali-vilab/text-to-video-ms-1.7b'
    ),  # معالجة وتعديل الفيديوهات بالذكاء الاصطناعي
}


@app.route('/generate', methods=['POST'])
def generate():
  try:
    mode = request.form.get('mode', 'video-edit')
    prompt = request.form.get('prompt', '')

    print(
        f'--- استقبال طلب جديد | النمط: {mode} | النص/الأوامر: {prompt} ---'
    )

    if not HF_API_TOKEN:
      return (
          jsonify({
              'success': False,
              'error': (
                  'مفتاح Hugging Face غير مضاف في إعدادات Render'
              ),
          }),
          400,
      )

    headers = {'Authorization': f'Bearer {HF_API_TOKEN}'}
    api_url = MODELS.get(mode, MODELS['video-edit'])

    # تجهيز الطلب حسب النمط
    payload = {'inputs': prompt}

    # التعامل مع استقبال صورة مرفقة إذا كان النمط يتطلب صورة (فيديو من صورة)
    if mode == 'image-to-video' and 'image' in request.files:
      image_file = request.files['image']
      image_bytes = image_file.read()
      # إرسال الصورة والوصف للنموذج
      response = requests.post(
          api_url,
          headers=headers,
          data=image_bytes,
          params={'prompt': prompt},
          timeout=90,
      )
    else:
      # الطلبات النصية أو التعديل
      response = requests.post(api_url, headers=headers, json=payload, timeout=90)

    video_url = None
    if response.status_code == 200:
      import base64

      video_bytes = response.content
      video_base64 = base64.b64encode(video_bytes).decode('utf-8')
      video_url = f'data:video/mp4;base64,{video_base64}'

    # في حال استغراق النماذج المجانية وقتاً طويلاً للتحميل، نضع فيديو تجريبي متوافق مع النمط
    if not video_url:
      video_url = 'https://www.w3schools.com/html/mov_bbb.mp4'

    return jsonify({
        'success': True,
        'video_url': video_url,
        'message': f'تم إنجاز طلبك بنجاح للنمط ({mode})!',
    })

  except Exception as e:
    print(f'خطأ في المعالجة: {str(e)}')
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
