# main.py
# 该服务器用于前端展示页面

# from flask_cors import *
from flask import Flask,render_template,request,Response,redirect,url_for,jsonify
from datetime import datetime, timedelta
import random
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
from ronglian_sms_sdk import SmsSDK
import json



#内网ip
app = Flask(__name__)

WEATHER_DAY_API_URL="http://127.0.0.1:5000/api/get_day"

# 此处Config可在其他地方定义，然后此处读取
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# 你喜欢用的任一短信
accId = '主账号ID'
accToken = '主账号TOKEN'
appId = '应用ID'






# 获取当周的天气数据
@app.route("/get_week")
def get_week():
    city="普洱"
    now = datetime.now()
    weekday = now.weekday()
    start_of_week = now - timedelta(days=weekday)
    week_dates = [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    # print("当前周日期列表：")
    # for date_str in week_dates:
        # print(date_str)
    
    # 构造请求获取当周天气数据
    weather_data_list = []
    for date_str in week_dates:
        params = {
            "date": date_str,
            "city":city
        }
        response = requests.get(WEATHER_DAY_API_URL, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            # print("1111",weather_data)
            day_weather=weather_data["data"]
            weather_data_list.append(day_weather)
        else:
            print("请求失败")
    print("天气数据列表：")
    for weather_data in weather_data_list:
        print(weather_data)
    air_list = []
    date_list = []
    humidity_list = []
    temperature_list = []
    weather_list = []
    wind_speed_list = []
    night_temperature_list = []
    aqi_list = []
    pm2_5_list = []
    pm10_list = []
    o3_list=[]

    
    # 遍历天气数据列表
    for day_weather in weather_data_list:
        # 提取每天的天气信息并添加到相应的列表中
        air_list.append(day_weather['air_quality'])
        date_list.append(day_weather['date'])
        humidity_list.append(day_weather['humidity'])
        temperature_list.append(day_weather['temperature'])
        weather_list.append(day_weather['weather'])
        wind_speed_list.append(day_weather['wind_speed'])
        night_temperature_list.append(day_weather['night_temperature'])
        aqi_list.append(day_weather['AQI'])
        pm2_5_list.append(day_weather['PM2.5'])
        pm10_list.append(day_weather['PM10'])
        o3_list.append(day_weather['O3'])




    # 将列表作为上下文传递给模板
    context = {
        'air_list': air_list,
        'date_list': date_list,
        'humidity_list': humidity_list,
        'temperature_list': temperature_list,
        'weather_list': weather_list,
        'wind_speed_list': wind_speed_list,
        'night_temperature_list': night_temperature_list,
        'city':city,
        'aqi_list':aqi_list,
        'pm2_5_list':pm2_5_list,
        'pm10_list':pm10_list,
        'o3_list':o3_list
    }
    
    return render_template("week.html", **context)

# 获取后3天的天气数据
@app.route("/get_after")
def get_after():
    now = datetime.now()
    # 计算后三天的日期
    after_dates = [(now + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 4)]
    weather_data_list = []
    for date_str in after_dates:
        params = {
            "date": date_str,
            "city":"普洱"
        }
        response = requests.get(WEATHER_DAY_API_URL, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            day_weather=weather_data["data"]
            weather_data_list.append(day_weather)
        else:
            print("请求失败")
    print("天气数据列表：")
    for weather_data in weather_data_list:
        print(weather_data)
    # 初始化列表来存储后三天的天气信息
    air_list = []
    date_list = []
    humidity_list = []
    temperature_list = []
    weather_list = []
    wind_speed_list = []
    night_temperature_list = []
    aqi_list = []
    pm2_5_list = []
    pm10_list = []
    o3_list=[]
    
    # 遍历天气数据列表
    for day_weather in weather_data_list:
        # 提取每天的天气信息并添加到相应的列表中
        air_list.append(day_weather['air_quality'])
        date_list.append(day_weather['date'])
        humidity_list.append(day_weather['humidity'])
        temperature_list.append(day_weather['temperature'])
        weather_list.append(day_weather['weather'])
        wind_speed_list.append(day_weather['wind_speed'])
        night_temperature_list.append(day_weather['night_temperature'])
        aqi_list.append(day_weather['aqi'])
        pm2_5_list.append(day_weather['pm2_5'])
        pm10_list.append(day_weather['pm10'])
        o3_list.append(day_weather['o3'])
    
    # 将列表作为上下文传递给模板
    context = {
        'air_list': air_list,
        'date_list': date_list,
        'humidity_list': humidity_list,
        'temperature_list': temperature_list,
        'weather_list': weather_list,
        'wind_speed_list': wind_speed_list,
        'night_temperature_list': night_temperature_list
    }
    
    return render_template("after.html", **context)
    

# 创建一个后台调度器
scheduler = BackgroundScheduler()
# 定时任务，该任务每天凌晨0点执行一次
def weather_reminder():
    # 获取今天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    # 构造请求获取今天的天气数据
    params = {
        "date": today,
        "city":"普洱"
    }
    response = requests.get(WEATHER_DAY_API_URL, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        day_weather=weather_data["data"]
        print("今天的天气数据：")
        print(day_weather)
    else:
        print("请求失败")
    # 对当天的天气和空气质量进行判断
    # TODO 此处可以自定义天气提醒逻辑，例如添加关键词判断，读取用户数据库去判断提醒 
    reminder_weather=["Stormy", "Extreme","Very Unhealthy", "Hazardous"]
    reminder_temperature={"min":0,"max":10}
    reminder_humidity={"min":0,"max":30}
    reminder_wind_speed={"min":0,"max":10}
    strList=[]
    if day_weather['air_quality'] in reminder_weather or day_weather['weather'] in reminder_weather:
        str="今天天气不好，注意出行安全！"
        strList.append(str)
    if day_weather['temperature']<reminder_temperature["min"]:
        str="今天温度较低，注意保暖！"
        strList.append(str)
    if day_weather['temperature']>reminder_temperature["max"]:
        str="今天温度较高，注意防暑！"
        strList.append(str)
    # TODO 每条都可以补充，懒得特地写了。
    print(str)
    # for s in strList:
    #     # 提醒每一条信息
    #     # TODO 拿用户信息，提醒用户
    #     msg = Message('Hello', sender='yourId@gmail.com', recipients=['id1@gmail.com'])
    #     msg.body = s
    #     mail.send(msg)
    #     # 或者配置了电话提醒的，可以调用电话提醒接口
    #     # TODO 获取用户手机号
    #     mobile="手机号"
    #     try:
    #         ccp = CCP()
    #         # 这里是定义的短信模板，传入s之后，发送短信
    #         result = ccp.send_message(mobile, (s), 1)
    #     except Exception as e:
    #         return jsonify(errmsg='发送异常')

scheduler.add_job(weather_reminder, 'cron', hour=0, minute=0)



if __name__ == "__main__":    
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=7000,debug=True)




class CCP(object):
    """发送短信的单例类"""
    # _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.sdk = SmsSDK(accId, accToken, appId)
        return cls._instance
    
    def send_message(self, mobile, datas, tid):
        sdk = self._instance.sdk
        resp = sdk.sendMessage(tid, mobile, datas)
        result = json.loads(resp)
        if result['statusCode'] == '000000':
            return 0
        else:
            return -1
