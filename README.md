# LBBapi_study
本项目仅供学习与研究使用，请勿用于商业或非法用途。因使用本项目产生的任何后果由使用者自行承担。


模块一：滑动验证码破解 + 防伪码识别  
文件：quite_CaptchaImg.py  
功能：  
1.读取 num.txt 中的防伪码编号（如：256376393828）  
2.通过接口提交后获得图像验证码（背景图+滑块）  
3.使用 ddddocr 模拟滑动识别，构造滑动轨迹 + 时间戳  
4.验证成功后写入 ok.txt 或 true/num.txt  

  
模块二：条码遍历与验证  
文件：quite_BarcodeQueryAgent.py  
功能：  
1.读取 id.txt 中的条码编号（如：256376393xxx）  
2.向接口 BarcodeQueryAgent 发送验证请求  
3.验证结果符合预期的成功结果保存至 true/id.txt  

  
<img width="1176" height="493" alt="图片" src="https://github.com/user-attachments/assets/11a72078-241a-4ae0-a6ac-1ee344fdea4d" />
