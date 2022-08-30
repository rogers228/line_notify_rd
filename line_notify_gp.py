import os
import requests
import config

class Line():
    def __init__(self):
        self.token = config.sys_token
    
    # 新增圖片功能
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
    line.post_data('hi, rogers, this is a test2.')

if __name__ == '__main__':
    test1()
    print('ok')
