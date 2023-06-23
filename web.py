from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='templates')
# /predict에서 업로드 폴더 설정할 때 쓰임
app.config['UPLOAD_FOLDER'] = './web/static/images/img'

# main page
@app.route('/')
def index():
    return render_template('1_index.html'), 200

# project introduce page
@app.route('/pjintro')
def pjintro():
    return render_template('2_pjintro.html'), 200

# model introduce page
@app.route('/mdintro')
def mdintro():
    return render_template('3_mdintro.html'), 200

# model development page
@app.route('/develop')
def develop():
    return render_template('4_develop.html'), 200

# service page
@app.route('/service')
def service():
    return render_template('5_service.html'), 200

# remind page
@app.route('/remind')
def remind():
    return render_template('6_remind.html'), 200

# CCTV 스트림 페이지
from CCTV import save_stream, get_all_cctv_names # CCTV 모듈에서 save_stream, get_all_cctv_names 함수를 가져옴

# '/cctv' 경로를 처리하는 함수
@app.route('/cctv', methods=['GET', 'POST'])  # 이 경로는 GET 및 POST 메서드를 모두 처리
def cctv():
    cctvnames = get_all_cctv_names()  # 모든 CCTV 이름을 가져옴
    selected_cctvnames = []  # 선택된 CCTV 이름들을 저장할 리스트
    
    if request.method == 'POST':  # 요청 메서드가 POST인 경우
        selected_cctvnames = request.form.getlist('cctvname')  # 선택한 CCTV 이름 받아오기
        time = int(request.form['time'])  # form 데이터에서 시간 값을 가져옴 (정수로 변환)
        
        for cctv_name in selected_cctvnames:
            save_stream(cctv_name, time, f"{cctv_name}_cctv.mp4") # CCTV 스트림을 지정된 시간 동안 저장
              
        # 'cctv.html' 템플릿을 렌더링하여 응답으로 반환. CCTV 이름과 시간을 템플릿에 전달
        return render_template('cctv.html', cctvnames=cctvnames, selected_cctvname=selected_cctvnames), 200
    else:  # 요청 메서드가 GET인 경우
        cctvnames = get_all_cctv_names()  # 모든 CCTV 이름을 가져옴
        
        # 'cctv.html' 템플릿을 렌더링하여 응답으로 반환. CCTV 이름 목록을 템플릿에 전달
        return render_template('cctv.html', cctvnames=cctvnames), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)
