import os
import random
from datetime import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv
 def get_weather(city):
    """
    获取城市天气信息
    :param city: 城市名称
    :return: 天气数据
    """
    url = f"https://free-api.heweather.net/s6/weather/now?location={city}&key={os.getenv('HE_WEATHER_KEY')}"
    response = requests.get(url)
    weather_data = response.json()
    weather = weather_data['HeWeather6'][0]['now']['cond_txt']
    temp = weather_data['HeWeather6'][0]['now']['tmp']
    return f"{city}今天天气: {weather}，温度: {temp}℃"
 def get_morning_quote():
    """
    获取早安心语
    :return: 早安心语
    """
    morning_quotes = ['早安，愿你拥有美好的一天。',
                      '早安，加油哦！',
                      '每天都是新的开始，早安。',
                      '早安，愿你的一天充满阳光和快乐。',
                      '早安，要记得微笑哦。']
    return random.choice(morning_quotes)
 def send_email(morning_quote, city_weather):
    """
    发送邮件
    :param morning_quote: 早安心语
    :param city_weather: 城市天气信息
    """
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = os.getenv('EMAIL_TO')
    msg['Subject'] = Header('每日早安心语推送', 'utf-8')
     text = MIMEText(f"{morning_quote}\n{city_weather}", 'plain', 'utf-8')
    msg.attach(text)
     smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
     with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
 if __name__ == '__main__':
    load_dotenv()
    city = os.getenv('CITY')
    city_weather = get_weather(city)
    morning_quote = get_morning_quote()
    send_email(morning_quote, city_weather)
    print(f"邮件发送成功！时间：{datetime.now()}")
