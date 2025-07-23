# 读取 true/id.txt，每行拼接成完整URL后写入 true/url.txt

input_file = "../id.txt"
output_file = "url.txt"
base_url = "https://fwsy.popmart.com/a?f="

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()  # 去除换行和空白
        if line:  # 跳过空行
            url = base_url + line
            fout.write(url + "\n")

print("已完成 URL 拼接并写入 true/url.txt")
