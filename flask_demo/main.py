# main.py
# 该服务器用于后端返回api固定数据，模拟后端服务器

# from flask_cors import *
from flask import Flask,render_template,request,Response,redirect,url_for,jsonify
import datetime
import random

#内网ip
app = Flask(__name__)





# hello world
@app.route("/")
def index():
    return "Hello World"

weather_chinese_list  = {
    "Good": "晴",
    "Sunny": "晴",
    "Cloudy": "多云",
    "Rainy": "雨",
    "Stormy": "暴风雨",
    "Extreme": "极端天气"
}
air_quality_chinese_list = {
    "Good": "良好",
    "Moderate": "中等",
    "Unhealthy": "不健康",
    "Very Unhealthy": "非常不健康",
    "Hazardous": "有害"
}

# 返回json数据,当天天气数据
@app.route("/api/get_day",methods=['GET'])
def get_day():
    date_str = request.args.get('date')
    city = request.args.get('city')

    if date_str is None or date_str == "":
        return jsonify({
            "code": 400,
            "message": "Date parameter is missing or empty."
        }), 400
    
    if city is None or city == "":
        return jsonify({
            "code": 400,
            "message": "City parameter is missing or empty."
        }), 400

    # 检查日期格式是否正确
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "code": 400,
            "message": "Invalid date format. Please use YYYY-MM-DD."
        }), 400


    temperature = random.randint(20, 30)
    humidity = random.randint(50, 80)
    night_temperature = random.randint(15, 20)
    wind_speed = 5  # 假设风速是5公里/小时
    # 随机生成天气
    weather = random.choice(["Good", "Sunny", "Cloudy", "Rainy", "Stormy", "Extreme"])
    # print(weather)
    weather=weather_chinese_list[weather]
    # print(weather)

    # 随机生成空气质量
    air_quality = random.choice(["Good", "Moderate", "Unhealthy", "Very Unhealthy", "Hazardous"])
    # print (air_quality)
    air_quality=air_quality_chinese_list[air_quality]
    # print (air_quality)
    aqi = random.randint(0, 500)
    pm2_5 = random.randint(0, 500)
    pm10 = random.randint(0, 500)
    o3 = random.randint(0, 500)

    data = {
        "code": 200,
        "data": {
            "id": 1,
            "city": city,
            "date": date_str,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "weather": weather,
            "air_quality": air_quality,
            "night_temperature": night_temperature,
            "AQI": aqi,
            "PM2.5": pm2_5,
            "PM10": pm10,
            "O3": o3
        }
    }

    return data

if __name__ == "__main__":    
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=5000,debug=True)

