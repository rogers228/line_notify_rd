# 用於測試的 notify
# 發佈到我自己的群組 不會影響到現有的群組

import os
import requests
import config

class Line():
    def __init__(self):
        self.token = config.sys_self_token

    def post_data(self, message):
        try:
            url = "https://notify-api.line.me/api/notify"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            payload = {
                'message': message
            }
            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload
            )
            if response.status_code == 200:
                print(f"Success -> {response.text}")

        except Exception as _:
            print(_)

    def post_data2(self, message, imgfile=''):
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

if __name__ == '__main__':
    test2()
    print('ok')
