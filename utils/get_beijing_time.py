import pytz
import datetime


def get_beijing_time_pytz():
    # 获取UTC时间
    utc_now = datetime.datetime.now(pytz.utc)
    # 转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_now = utc_now.astimezone(beijing_tz)
    beijing_now = beijing_now.strftime("%Y-%m-%d %H:%M:%S")
    print("beijing_now", beijing_now)
    return beijing_now


if __name__ == '__main__':
    get_beijing_time_pytz()

