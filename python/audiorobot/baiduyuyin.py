# coding: utf8

# @Author: 郭 璞
# @File: baiduyuyin.py                                                                 
# @Time: 2017/5/11                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 借助百度语音识别接口实现本地语音解析

import pyaudio
import wave
import requests
import json

class BaiDuYuYin(object):

    def __init__(self):
        # get the token
        self.token = self.gettoken()

    def gettoken(self):
        try:
            apiKey = "Ll0c53MSac6GBOtpg22ZSGAU"
            secretKey = "44c8af396038a24e34936227d4a19dc2"

            auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
            response = requests.get(url=auth_url)
            jsondata = response.text
            return json.loads(jsondata)['access_token']
        except Exception as e:
            raise Exception("Cannot get the token, the reason is {}".format(e))

    def parse(self, wavefile='local.wav'):
        """
        返回音频文件对应的文本内容。
        注意返回的是列表类型的数据，待会处理的时候要格外的小心。
        :param wavefile:
        :return:
        """
        try:
            fp = wave.open(wavefile, 'rb')
            # 已经录好音的音频片段内容
            nframes = fp.getnframes()
            filelength = nframes * 2
            audiodata = fp.readframes(nframes)

            # 百度语音接口的产品ID
            cuid = '7519663'
            server_url = 'http://vop.baidu.com/server_api' + '?cuid={}&token={}'.format(cuid, self.token)
            headers = {
                'Content-Type': 'audio/pcm; rete=8000',
                'Content-Length': '{}'.format(filelength),
            }

            response = requests.post(url=server_url, headers=headers, data=audiodata)
            print(response.text)
            data = json.loads(response.text)
            if data['err_msg'] == 'success.':
                return data['result']
            else:
                return '你说的啥啊，听不清听不清！'
        except Exception as e:
            raise Exception("Parsing wave file failed. The reason is {}".format(e))

if __name__ == '__main__':
    yuyinclient = BaiDuYuYin()
    result = yuyinclient.parse(wavefile='local.wav')
    print(result)