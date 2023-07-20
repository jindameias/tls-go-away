import json
from pprint import pprint

import requests


cookies = {
    'CoreSessionId': '01f9ec306fb638400fb0b1631dae114248efbcc21d15eb0717601',
    '_g_sign': 'gg076200dd2c28782a6ea2636b06df15',
    'MaD6Q7kRAnkBO': '5NORItSXqsePt4iautnLJg69G3Qiq1YH3whG7KJMTn3PGrCLvYWtUNcM6W74fZps99ofZhmSnu0Kn0HRYFzdBxU73NhA',
    'JSESSIONID': '110CD2DC7F6CD340B10CBEF02D6891BF',
    'MaD6Q7kRAnkBP': 'bf8rqF17tP091zgTPzIElCKNu1PqFFG6JKMMBTQyePHZ0xF9uFDpKj9Hx3FfmybiEPGb5X3gIpBpqdcH.aDBijlbtevP5nn5c_sau11mshf2d.C8ENR5GB6MHGrfyijDZD1.4mW1lxzZ45x2drTG7knibTRx6epU2pYX42anoFVteztt_hOTE._vqY7YUPJEc4krmOyV76.Z2XaOQBvosLkmMnA1qdRRINb.FR8sQgncez9jX1Sc59l2tumkRdli1RqxXMfcZPvMjmAM040f5DraQ1vk59XYbT9.LaUvhHZZEBFBvvPrEdzqYDnfECTAfUynaVo5q9wbi7fc6nEo7lJVQ9wfFyVEztOcGNrcqJv6VKot4ihKdHHNqg',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Access-Token': '1f2e348c-c549-4af4-bd89-770e7c03dd04',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'apply-Type': '4',
    'businessid': '123456789',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Transpond-Url': 'https://tls.browserleaks.com/json',

}

params = {
    'id': 1,
    'name': 'xx',
    'other': 'other'
}
txt = requests.get('http://127.0.0.1:10000/transpond', params=params, headers=headers, cookies=cookies).json()
pprint(json.loads(txt['message']))





