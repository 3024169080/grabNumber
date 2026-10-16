import hashlib
import random
import string
import time
import requests
import json

class Color:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    BOLD = '\033[1m'

def log_time():
    return time.strftime('%H:%M:%S', time.localtime())

def pretty_print_json(data, indent=2):
    return json.dumps(data, ensure_ascii=False, indent=indent)

class RegistrationClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _get_session(self):
        return self.session

    def generate_signature(self, token: str, eid: str):
        def random_key(length=4):
            chars = string.ascii_letters + string.digits
            return ''.join(random.choice(chars) for _ in range(length))

        T = random_key() + token[:2]
        I = hashlib.md5(eid.encode()).hexdigest()
        b = str(int(time.time() * 1000))
        M = T + hashlib.md5((I + b + "qwrq2w").encode()).hexdigest()
        return M

    def get_item_details(self, token: str, eid: str):
        url = f'{self.base_url}/xcx/enroll/v2/item_detail?eid={eid}&access_token={token}'
        session = self._get_session()
        
        print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}get_item_details{Color.RESET} 开始请求...")
        start_time = time.time()
        response = session.get(url, timeout=10)
        elapsed = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            print(f"{Color.GREEN}[{log_time()}] {Color.BOLD}get_item_details{Color.RESET} 请求成功 {Color.CYAN}[{elapsed:.2f}ms]{Color.RESET}")
            print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}get_item_details{Color.RESET} 响应数据:")
            print(f"{Color.RESET}{pretty_print_json(result)}")
            return result
        else:
            print(f"{Color.RED}[{log_time()}] {Color.BOLD}get_item_details{Color.RESET} 请求失败 {Color.CYAN}[{elapsed:.2f}ms]{Color.RESET}")
            print(f"{Color.RED}[{log_time()}] {Color.BOLD}get_item_details{Color.RESET} 状态码: {response.status_code}, 响应: {response.text}")
            return None

    def submit_registration(self, token: str, eid: str, info: list, items: list):
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
        
        print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} 开始请求...")
        print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} URL: {url}")
        print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} 参数:")
        print(f"{Color.RESET}{pretty_print_json(data)}")
        
        session = self._get_session()
        start_time = time.time()
        response = session.post(url, json=data, timeout=10)
        elapsed = (time.time() - start_time) * 1000
        
        print(f"{Color.GREEN}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} 请求完成 {Color.CYAN}[{elapsed:.2f}ms]{Color.RESET}")
        print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} 状态码: {response.status_code}")
        
        try:
            result = response.json()
            print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} 响应数据:")
            print(f"{Color.RESET}{pretty_print_json(result)}")
        except:
            print(f"{Color.BLUE}[{log_time()}] {Color.BOLD}submit_registration{Color.RESET} 响应文本: {response.text}")
            result = {"status": response.status_code, "text": response.text}
            
        return result

    def register(self, token: str, eid: str, info: list):
        print(f"\n{'='*60}")
        print(f"{Color.YELLOW}[{log_time()}] {Color.BOLD}register{Color.RESET} 开始执行")
        print(f"{'='*60}\n")
        
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
            
            after_details_time = time.time()
            time.sleep(1)
            before_submit_time = time.time()
            interval = (before_submit_time - after_details_time) * 1000
            
            print(f"\n{'-'*60}")
            print(f"{Color.YELLOW}[{log_time()}] {Color.BOLD}register{Color.RESET} 等待间隔: {Color.CYAN}{interval:.2f}ms{Color.RESET}")
            print(f"{'-'*60}\n")
            
            result = self.submit_registration(token, eid, info, items)
            
            print(f"\n{'='*60}")
            print(f"{Color.YELLOW}[{log_time()}] {Color.BOLD}register{Color.RESET} 执行完成")
            print(f"{'='*60}\n")
            
            return result
        else:
            print(f"{Color.RED}[{log_time()}] {Color.BOLD}register{Color.RESET} 获取项目参数失败或项目参数不完整")
            return {"error": "获取项目参数失败或项目参数不完整"}