import random
import string
import time
import hashlib
import requests

SECRET = 'JSBT0Cz4s3uOnp5hJ0kUdG46DqqoM5FcvpaQEAs7JCU='
USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; VOG-AL10 Build/HUAWEIVOG-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'

def get_nonce():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

def request(base_uri, method, payload={}):
    payload['activity_group_id'] = 'GP7348571626965248'
    payload['activity_id'] = '7348598865611008'
    payload['appkey'] = 'c670d0bb6cec485fab0fd1b9e0843be4'
    payload['nonce'] = get_nonce()
    payload['ts'] = int(time.time() * 1000)

    sign_str = '&'.join([f'{k}={v}' for k, v in sorted(payload.items())])
    sign_str += '&secret=' + SECRET
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    payload['sign'] = sign

    url = f'https://le3-api.game.bilibili.com/x/api/gzlj20250401/game/{base_uri}'

    if method == 'GET':
        resp = requests.get(url, params=payload, headers={
            'User-Agent': USER_AGENT,
        }, timeout=5)
    elif method == 'POST':
        resp = requests.post(url, json=payload, headers={
            'User-Agent': USER_AGENT,
        }, timeout=5)
    return resp.json()

if __name__ == '__main__':
    while True:
        # 查询次数
        # print(request('index', 'GET', {}))

        # 开始游戏，获取 token
        resp = request('start', 'POST', {})
        print(resp)
        token = resp['data']['body']['token']
        print(token)

        time.sleep(10)
        # 提交结果
        print(request('end', 'POST', {'token': token, 'rescue_number': 5}))