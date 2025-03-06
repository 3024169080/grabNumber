from grabNumber import RegistrationClient
def trigger_register():
    base_url = "https://api-xcx-qunsou.weiyoubot.cn"  # 替换为实际的基础 URL
    client = RegistrationClient(base_url)
    
    token = "6c92edd683f04904b0250d85751f1749"  # 替换为实际的 token
    eid = "67c94c7c6cbec7797aa1bf74"  # 替换为实际的 eid
    info = [
        {
            "field_name": "姓名",
            "field_value": "林",
            "field_key": 1
        }
    ]
    client.register(token, eid, info)
    print("请求已发送")

trigger_register()