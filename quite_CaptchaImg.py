# 项目名称：LBBapi_study
# 作者：dig2pen
# 说明：本项目仅供学习与研究使用，请勿用于商业或非法用途。因使用本项目产生的任何后果由使用者自行承担。


import base64
import json
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
import requests
from ddddocr import DdddOcr
import os

# 绕过定位图像验证码，爬取其中的防伪码。
# 读num.txt中的防伪码，将该二维码正确的防伪码保存到 ok.txt 中。


# ========== 快代理隧道配置 ==========
KDL_TUNNEL = "<快代理的域名:端口>"
KDL_USERNAME = "<快代理用户名>"
KDL_PASSWORD = "<快代理密码>"

proxies = {
    "http": f"http://{KDL_USERNAME}:{KDL_PASSWORD}@{KDL_TUNNEL}",
    "https": f"http://{KDL_USERNAME}:{KDL_PASSWORD}@{KDL_TUNNEL}"
}

# ========== 终止控制 ==========
exit_event = threading.Event()

# ========== 工具函数 ==========

def base64_to_bytes(base64_str):
    if base64_str.startswith('data:image'):
        base64_str = base64_str.split(',', 1)[1]
    return base64.b64decode(base64_str)

def calculate_slide_distance(bg_base64, gap_base64):
    ocr = DdddOcr(det=False, ocr=False, show_ad=False)
    return ocr.slide_match(base64_to_bytes(gap_base64), base64_to_bytes(bg_base64))['target'][0]

def __ease_out_expo(sep):
    return 1 if sep == 1 else 1 - pow(2, -10 * sep)

def get_slide_track(distance):
    slide_track = [{"x": random.randint(-50, -10), "y": random.randint(-50, -10), "t": 0}, {"x": 0, "y": 0, "t": 0}]
    count = 30 + int(distance / 2)
    t = random.randint(50, 100)
    _x = 0
    for i in range(count):
        x = round(__ease_out_expo(i / count) * distance)
        t += random.randint(10, 20)
        if x == _x:
            continue
        slide_track.append({"x": x, "y": 0, "t": t})
        _x = x
    slide_track.append(slide_track[-1])
    return slide_track

def calculate_end_time(tracks):
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(milliseconds=tracks[-1]["t"] if tracks else 0)
    return start_time.isoformat(timespec='milliseconds').replace('+00:00', 'Z'), end_time.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

# ========== 主处理函数 ==========

def process_code(code):
    cookies = {
        'user_track_id': 'mvlaxvkk_07491612535f4882a0f207da00e04c3c',
        'request_source': '4',
    }

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://fwsy.popmart.com',
        'referer': f'https://fwsy.popmart.com/a?f={code}&t=&channel=service',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    }

    for _ in range(3):
        if exit_event.is_set():
            return

        print(f"[→] 正在处理 {code} | 使用快代理隧道进行请求")

        try:
            res = requests.post(
                "https://fwsy.popmart.com/a/c/v2/api/Fwcode/FwcodeQuery",
                json={"Fwcode": code},
                headers=headers,
                cookies=cookies,
                proxies=proxies,
                timeout=15,
                verify=False
            ).json()

            data = res.get("Data", {})
            if "Status" in data and data["Status"] == 1:
                print(f"[⚠️] 第一阶段响应出现 Status=1，写入 ok.txt 并终止")
                with open("ok.txt", "a", encoding="utf-8") as f:
                    f.write(code + "\n")
                exit_event.set()
                return

            if "CaptchaId" not in data:
                print(f"[×] 无效响应：{res}")
                return

            if exit_event.is_set():
                return

            distance = int(calculate_slide_distance(data["CaptchaImg"], data["CaptchaSliderImg"]) * 0.48) - 2
            if exit_event.is_set():
                return

            tracks = get_slide_track(distance)
            start_time, end_time = calculate_end_time(tracks)

            payload = {
                "Fwcode": code,
                "CaptchaId": data["CaptchaId"],
                "Track": {
                    "backgroundImageWidth": 268,
                    "backgroundImageHeight": 167,
                    "sliderImageWidth": 53,
                    "sliderImageHeight": 167,
                    "startTime": start_time,
                    "endTime": end_time,
                    "tracks": tracks
                }
            }

            result = requests.post(
                "https://fwsy.popmart.com/a/c/v2/api/Fwcode/FwcodeQuery",
                data=json.dumps(payload),
                headers=headers,
                cookies=cookies,
                proxies=proxies,
                timeout=15,
                verify=False
            ).json()

            print(f"[结果] {code}: {result}")

            if "Data" in result and isinstance(result["Data"], dict):
                if "Status" in result["Data"] and result["Data"]["Status"] == 1:
                    print(f"[⚠️] 第二阶段响应出现 Status=1，写入 ok.txt 并终止")
                    with open("ok.txt", "a", encoding="utf-8") as f:
                        f.write(code + "\n")
                    exit_event.set()
                    return

            if result.get("ReqCode") == 200:
                with open("true/num.txt", "a", encoding="utf-8") as f:
                    f.write(code + "\n")
                return

        except Exception as e:
            print(f"[!] 请求异常：{e}")
        time.sleep(1)

# ========== 主函数入口 ==========

def main():

    msg = """
        ===============================
        # 项目名称：LBBapi_study
        # 作者：dig2pen
        # 说明：本源码仅供学习研究使用
        # 禁止用于商业用途与非法活动
        # 因使用本项目产生的任何后果由使用者自行承担
        ===============================
        """
    print(msg)

    try:
        with open("num.txt", "r", encoding="utf-8") as f:
            codes = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] 无法读取 num.txt: {e}")
        return

    if not codes:
        print("[!] num.txt 为空")
        return

    os.makedirs("true", exist_ok=True)

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_code, code) for code in codes]
        try:
            for future in as_completed(futures):
                if exit_event.is_set():
                    print("[✓] 检测到终止信号，尝试取消剩余任务")
                    break
        finally:
            for f in futures:
                f.cancel()

if __name__ == "__main__":
    main()
