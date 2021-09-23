import os
import sys
import json
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
PUSH_KEY = os.getenv("PUSH_KEY")

fudan_daily_url = "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily"
login_url = "https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fzlapp.fudan.edu.cn%2Fa_fudanzlapp%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fzlapp.fudan.edu.cn%252Fsite%252Fncov%252FfudanDaily%26from%3Dwap"
get_info_url = "https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info"
save_log_url = "https://zlapp.fudan.edu.cn/wap/log/save-log"
save_url = "https://zlapp.fudan.edu.cn/ncov/wap/fudan/save"


def get_session(_login_info):
    _session = requests.Session()
    _session.headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/WIFI Language/zh_CN miniProgram"

    _response = _session.get(login_url)
    soup = BeautifulSoup(_response.text, "lxml")
    inputs = soup.find_all("input")
    for i in inputs:
        if i.get("name") and i.get("name") not in ["username", "password", "captchaResponse"]:
            _login_info[i.get("name")] = i.get("value")
    _session.post(login_url, data=_login_info)

    _session.headers["Origin"] = "https://zlapp.fudan.edu.cn"
    _session.headers["Referer"] = fudan_daily_url
    return _session


def get_historical_info(_session):
    response = session.get(get_info_url)
    return json.loads(response.text)["d"]


def get_today_date():
    _tz = timezone(+timedelta(hours=8))
    return datetime.now(_tz).strftime("%Y%m%d")


def save_log(_session):
    _data = {
        "appkey": "ncov",
        "url": fudan_daily_url,
        "timestamp": int(time.time())
    }
    _data["signature"] = hashlib.md5((_data["appkey"] + str(_data["timestamp"]) + _data["url"]).encode()).hexdigest()
    _session.post(save_log_url, data=_data)


def get_payload(_historical_info):
    _payload = _historical_info["info"]
    if "jrdqjcqk" in _payload:
        _payload.pop("jrdqjcqk")
    if "jrdqtlqk" in _payload:
        _payload.pop("jrdqtlqk")

    _payload.update({
        "ismoved": 0,
        "number": _historical_info["uinfo"]["role"]["number"],
        "realname": _historical_info["uinfo"]["realname"],
        "sfhbtl": 0,
        "sfjcgrq": 0
    })

    if not _payload["area"]:
        _payload.update({
            "area": _historical_info["oldInfo"]["area"],
            "city": _historical_info["oldInfo"]["city"],
            "province": _historical_info["oldInfo"]["province"]
        })

    return _payload


def get_payload_str(_payload):
    _ = _payload.copy()
    _["geo_api_info"] = json.loads(_["geo_api_info"])
    return json.dumps(_, ensure_ascii=False)


def save(_session, _payload):
    return _session.post(save_url, data=_payload)


def notify(_title, _message=None):
    if not PUSH_KEY:
        print("未配置PUSH_KEY！")
        return

    if not _message:
        _message = _title

    print(_title)
    print(_message)

    _response = requests.post(f"https://sc.ftqq.com/{PUSH_KEY}.send", {"text": _title, "desp": _message})

    if _response.status_code == 200:
        print(f"发送通知状态：{_response.content.decode('utf-8')}")
    else:
        print(f"发送通知失败：{_response.status_code}")


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        notify("请正确配置用户名和密码！")
        sys.exit()

    login_info = {
        "username": USERNAME,
        "password": PASSWORD
    }

    try:
        session = get_session(login_info)
        historical_info = get_historical_info(session)
        save_log(session)

        payload = get_payload(historical_info)
        payload_str = get_payload_str(payload)
        # print(payload_str)

        if payload.get("date") == get_today_date():
            notify(f"今日已打卡：{payload.get('area')}", f"今日已打卡：{payload_str}")
            sys.exit()

        time.sleep(5)
        response = save(session, payload)

        if response.status_code == 200 and response.text == '{"e":0,"m":"操作成功","d":{}}':
            notify(f"打卡成功：{payload.get('area')}", payload_str)
        else:
            notify("打卡失败，请手动打卡", response.text)

    except Exception as e:
        notify("打卡失败，请手动打卡", str(e))
