# 生成所有以25637639开头的4位后缀数字组合，并保存到id.txt
prefix = "495367726481"

with open("num.txt", "w") as f:
    for i in range(10000):  # 从0000到9999
        number = prefix + f"{i:04d}"  # 补齐为4位
        f.write(number + "\n")

print("共生成 10000 个号码，已保存到 num.txt 文件中。")
