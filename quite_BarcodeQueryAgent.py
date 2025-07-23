# 项目名称：LBBapi_study
# 作者：dig2pen
# 说明：本项目仅供学习与研究使用，请勿用于商业或非法用途。因使用本项目产生的任何后果由使用者自行承担。


import requests
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


# 调用id.txt中的id号去遍历存在的url码，例如25637639xxxx中，https://xxxxx.com/a?f=256376390181存在，则可以遍历出该f的参数。
# 将最终存在的id值自动保存到 true\id.txt 中。

# ========== 快代理隧道配置 ==========
KDL_TUNNEL = "<快代理的域名:端口>"
KDL_USERNAME = "<快代理用户名>"
KDL_PASSWORD = "<快代理密码>"

PROXIES = {
    "http": f"http://{KDL_USERNAME}:{KDL_PASSWORD}@{KDL_TUNNEL}",
    "https": f"http://{KDL_USERNAME}:{KDL_PASSWORD}@{KDL_TUNNEL}"
}

# ========== 接口配置 ==========
TARGET_URL = "https://fwsy.popmart.com/a/api/Fwcode/BarcodeQueryAgent"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/json",
    "Origin": "https://fwsy.popmart.com",
    "Referer": "https://fwsy.popmart.com/a?f=256376393828"
}

MAX_WORKERS = 5
lock = threading.Lock()

# ========== 工具函数 ==========
def get_current_ip():
    try:
        res = requests.get("https://api.ipify.org", timeout=5, proxies=PROXIES)
        return res.text.strip()
    except Exception:
        return None

# ========== 核心工作函数 ==========
def verify_barcode(barcode):
    while True:
        ip = get_current_ip()
        print(f"[IP] 当前代理 IP: {ip or '获取失败'}")

        data = {"Barcode": barcode}
        try:
            response = requests.post(TARGET_URL, headers=HEADERS, json=data, proxies=PROXIES, timeout=10)
            res_json = response.json()

            print(f"[+] Barcode: {barcode}")
            print(f"    Response: {res_json}\n")

            if (
                res_json.get("Code") == 1 and
                res_json.get("Message") == "提交成功" and
                res_json.get("Data", {}).get("State") == 20
            ):
                with lock:
                    with open("true/id.txt", "a", encoding="utf-8") as tf:
                        tf.write(barcode + "\n")
                print(f"[✓] 成功保存: {barcode}")
                return
            else:
                print(f"[×] 条码验证未通过: {barcode}，继续尝试...")
        except Exception as e:
            print(f"[×] 请求失败：{barcode} -> {e}")

        print("[i] 等待 3 秒后重试...")
        time.sleep(3)

# ========== 主程序 ==========
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

    os.makedirs("true", exist_ok=True)

    try:
        with open("id.txt", "r", encoding="utf-8") as f:
            barcodes = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] 读取 id.txt 文件失败: {e}")
        return

    if not barcodes:
        print("[!] id.txt 中无条码数据")
        return

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(verify_barcode, barcode) for barcode in barcodes]
        for _ in as_completed(futures):
            pass  # 可加入异常收集等逻辑

    print("[✓] 所有条码处理完成")

if __name__ == "__main__":
    main()
