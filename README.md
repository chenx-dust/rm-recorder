# RoboMaster 直播录制工具

本项目提供了录制 RoboMaster 官网直播的功能，可录制操作手视角。

## 使用方式

```sh
git clone https://github.com/chenx-dust/rm-recorder.git
cd rm-recorder
pip3 install pyav
python3 ./main.py
```

## 配置参数

`rm-recorder/config.py`

```python
SCHEDULE_URL = ''           # 赛事计划 API
LIVE_INFO_URL = ''          # 赛事推流 API

ZONE_ID = '498'             # 赛区设置

MAIN_VIEW_RECORD = False    # 是否录制主视角
RESOLUTION = 'high'         # 分辨率 high(1080p) middle(720p) low(540p)

CHECK_TIME = 1.             # 比赛检查间隔 (s)
```

## 鸣谢

RoboMaster 组委会

哈尔滨工业大学（深圳） 南工骁鹰机器人队
