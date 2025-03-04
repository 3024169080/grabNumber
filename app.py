from flask import Flask, request, render_template
from grabNumber import RegistrationClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    base_url = "https://api-xcx-qunsou.weiyoubot.cn"  # 替换为实际的基础 URL
    client = RegistrationClient(base_url)
    
    token = request.form['token']
    eid = request.form['eid']
    info = [
        {
            "field_name": "姓名",
            "field_value": "林",
            "field_key": 1
        }
    ]
    client.register(token, eid, info)
    return "请求已发送"

if __name__ == '__main__':
    app.run(debug=True)