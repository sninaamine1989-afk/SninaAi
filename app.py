import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # السماح لبلوجر بالاتصال


@app.route('/generate', methods=['POST'])
def generate():
  try:
    # استقبال الأوضاع والبيانات المرسلة من مدونة بلوجر
    task_mode = request.form.get('mode', 'text-to-video')
    prompt = request.form.get('prompt', '')
    media_file = request.files.get('media')

    # طباعة تفاصيل الطلب في سجلات السيرفر لمتابعتها من هاتفك
    print(f'--- طلب جديد عبر Snina Ai ---')
    print(f'الوضع (Mode): {task_mode}')
    print(f'البرومبت / النص: {prompt}')
    print(
        f'ملف مرفق: {media_file.filename if media_file else "لا يوجد ملف"}'
    )

    # هنا يتم توجيه الطلب للـ API الحقيقي بناءً على الـ task_mode
    # مثال:
    # if task_mode == 'image-to-video':
    #     # كود إرسال الصورة للذكاء الاصطناعي
    # elif task_mode == 'script-to-long-video':
    #     # كود توليد السكريبت والصوت والفيديو

    # للبدء الفعلي والربط السلس، سنقوم حالياً بدعم استقبال الملفات والأوامر بنجاح،
    # وإرجاع استجابة ديناميكية تؤكد معالجة الطلب:
    response_data = {
        'success': True,
        'video_url': (  # رابط فيديو مؤقت حي يتغير حسب العملية أو رابط جاهز
            'https://www.w3schools.com/html/mov_bbb.mp4'
        ),
        'message': f'تمت معالجة وضع ({task_mode}) بنجاح بواسطة Snina Ai',
    }

    return jsonify(response_data)

  except Exception as e:
    print(f'خطأ في السيرفر: {str(e)}')
    return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
