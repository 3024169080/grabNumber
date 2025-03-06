from flask import Flask, request, render_template, jsonify
from grabNumber import RegistrationClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details', methods=['GET'])
def details():
    token = request.args.get('token')
    eid = request.args.get('eid')
    base_url = "https://api-xcx-qunsou.weiyoubot.cn"  # 替换为实际的基础 URL
    client = RegistrationClient(base_url)
    item_details = client.get_item_details(token, eid)
    if item_details:
        return jsonify(item_details)
    else:
        return jsonify({"error": "获取项目参数失败"}), 400

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
    response = client.register(token, eid, info)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)