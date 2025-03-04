import hashlib
import random
import string
import time
import requests  # 添加 requests 库

class RegistrationClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def generate_signature(self, token: str, eid: str):
        '''
        生成提交报名时需要的签名
        Args:
            token: 用户登录凭证
            eid: 活动ID

        Returns: 签名字符串
        '''
        def random_key(length=4):
            chars = string.ascii_letters + string.digits
            return ''.join(random.choice(chars) for _ in range(length))

        T = random_key() + token[:2]
        I = hashlib.md5(eid.encode()).hexdigest()
        b = str(int(time.time() * 1000))
        M = T + hashlib.md5((I + b + "qwrq2w").encode()).hexdigest()
        return M

    def get_item_details(self, token: str, eid: str):
        '''
        获取项目参数
        Args:
            token: 用户登录凭证
            eid: 活动ID

        Returns: 项目参数的字典
        '''
        url = f'{self.base_url}/xcx/enroll/v2/item_detail?eid={eid}&access_token={token}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("获取项目参数失败:", response.status_code, response.text)
            return None

    def submit_registration(self, token: str, eid: str, info: list, items: list):
        '''
        抢号
        Args:
            token: 用户登录凭证
            eid: 活动ID
            info: 报名信息
            items: 物品相关信息

        Returns: None
        '''
        url = f'{self.base_url}/xcx/enroll/v5/enroll'
        data = {
            "access_token": token,
            "eid": eid,
            "info": info,
            "on_behalf": 0,
            "items": items,
            "referer": "",
            "fee_type": "",
            "from": "xcx",
            "_a": self.generate_signature(token, eid),
            "_s": int(time.time() * 1000)
        }
        print("调用接口的 URL:", url)
        print("调用接口的参数:", data)
        
        # 发送 POST 请求
        response = requests.post(url, json=data)
        print("响应状态码:", response.status_code)
        print("响应内容:", response.json())

    def register(self, token: str, eid: str, info: list):
        '''
        获取项目参数并提交注册
        Args:
            token: 用户登录凭证
            eid: 活动ID
            info: 报名信息

        Returns: None
        '''
        item_details = self.get_item_details(token, eid)
        if item_details and "items" in item_details["data"]:
            timespan = item_details["data"]["items"][0]["timespan"][0]
            items = [
                {
                    "key": item_details["data"]["items"][0]["key"],
                    "count": 1,
                    "date": timespan["date"],
                    "start": timespan["start"],
                    "end": timespan["end"]
                }
            ]
            self.submit_registration(token, eid, info, items)
        else:
            print("获取项目参数失败或项目参数不完整")