# n9e-voice-sender
适用于夜莺(n9e)监控系统的语音发送器   


修改 `/home/n9e/etc/rdb.yml` 中如下字段：
``` 
sms:
    # two choice: shell|api
    way: api
    worker: 10
    api: http://127.0.0.1:5000/aliyun/voice
```
重启 rdb 模块即可。
（之所以使用sms是因为 夜莺本身的 voice 回调只有策略名，sms 则会完整的给出告警详情）

接受人在夜莺中配置手机号。


```
# python3
# 依赖：
aliyun-python-sdk-core==2.13.30
Flask==1.1.2
```
