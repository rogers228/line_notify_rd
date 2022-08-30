# 用於測試的 notify
# 發佈到我自己的群組 不會影響到現有的群組

import os
import requests
import config

class Line():
    def __init__(self):
        self.token = config.sys_self_token

    def post_data(self, message, imgfile=''):
        try:
            url = "https://notify-api.line.me/api/notify"
            headers = {'Authorization': f'Bearer {self.token}'}
            payload = {'message':       message}
            files = {}
            if imgfile != '':
                files = { 'imageFile': open(os.path.join(config.image_path, imgfile), 'rb') }
            response = requests.request('POST', url, headers=headers, data=payload, files =files) # send
            if response.status_code == 200:
                print(f"Success -> {response.text}")
        except Exception as _:
            print(_)

def test1():
    line = Line()
    line.post_data('hi, rogers, this is a test3.')

def test2():
    line = Line()
    # line.post_data2('hi, rogers, this is a test7.', 'goodjob01.jpg')
    line.post_data2('hi, rogers, this is a test8.', 'comeon01.jpg')
    # line.post_data2('hi, rogers, this is a test6.')

def test3():
    line = Line()
    t = '發圖這條路\n'
    t += '1.先發也不行(單據版次不符)\n'
    t += '2.沒發也不行(尺寸變更過了)\n'
    t += '3.手改簽名圖記得發行品保\n'
    t += '4.結案後正式發行(千萬不要忘記)\n'
    t += '5.太久未結主動提醒\n'
    t += '6.發行要登記(常說沒收到)\n'
    t += '7.在途發行要通知採購備註SFT'

    line.post_data(t, 'release01.jpg')

def test4():
    line = Line()
    line.post_data('小幫手提醒你，改圖已超過規定時間', 'bomb01.jpg')

if __name__ == '__main__':
    test4()
    print('ok')
