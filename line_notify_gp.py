import requests

class Line():
    def __init__(self):
        self.token = "V8PzVi8LgPJzQwQdL8MeUPWJU0ZRBXK9QyGp1fiIx3w"

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

def test1():
    line = Line()
    line.post_data('hi, rogers, this is a test2.')

if __name__ == '__main__':
    test1()
    print('ok') 
