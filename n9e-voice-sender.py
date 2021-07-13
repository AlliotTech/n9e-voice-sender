#!/usr/bin/env python3
# coding=utf-8

from flask import Flask, request
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

server = Flask(__name__)

# 阿里云access key
KEY = ''
SECRET = ''
REGION = 'cn-shenzhen'
# 语音模板（阿里云后台获取）
TTSCODE = 'TTS_123213321'

def ali_send_voice(phone_number, message):
    """
    调用阿里云拨打电话
    """
    _client = AcsClient(KEY, SECRET, REGION)
    _request = CommonRequest()
    _request.set_accept_format('json')
    _request.set_domain('dyvmsapi.aliyuncs.com')
    _request.set_method('POST')
    _request.set_protocol_type('https')
    _request.set_version('2017-05-25')
    _request.set_action_name('SingleCallByTts')
    _request.add_query_param('Volume', "100")
    _request.add_query_param('Speed', "-450")
    _request.add_query_param('PlayTimes', "3")

    _request.add_query_param('CalledNumber', phone_number)
    _request.add_query_param('TtsCode', TTSCODE)
    _request.add_query_param('TtsParam', f"""{{\"message\":\"{message}\"}}""")

    response = _client.do_action_with_exception(_request)
    return str(response, encoding='utf-8')


def generate_message_for_n9e(message):
    """
    提取告警消息体中的告警策略名称、设备IP，优化组合后返回，供语音使用(语音不支持.)
    :param message:
    :return:
    """
    if str(message).split('\n')[0].split('：')[0] != '级别状态':
        name = str(message).split('\n')[2].split('：')[1]
        device = str(message).split('\n')[3].split('：')[1].replace('.', '点，').replace('0', '零').replace('1', '妖').replace('2', '二').replace('3', '三').replace('4', '四').replace('5', '五').replace('6', '六').replace('7', '七').replace('8', '八').replace('9', '九')
    else:
        name = str(message).split('\n')[1].split('：')[1]
        device = str(message).split('\n')[2].split('：')[1].replace('.', '点，').replace('0', '零').replace('1', '妖').replace('2', '二').replace('3', '三').replace('4', '四').replace('5', '五').replace('6', '六').replace('7', '七').replace('8', '八').replace('9', '九')
    return name + '。' + 'IP地址为。' + device


@server.route('/aliyun/voice', methods=['GET', 'POST'])
def voice():
    if request.method == 'GET':
        return {'tos': ['phone_number'], 'subject': '', 'content': 'voice_content'}
    req = request.json
    message = generate_message_for_n9e(req['content'])

    for i in (req['tos']):
        print(i, message)
    return 'success'


if __name__ == '__main__':
    server.run(debug=True)
