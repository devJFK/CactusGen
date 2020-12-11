from models.enums.response_type import ResponseType
from time import sleep
import requests

import traceback

class TwoCaptcha():
    def __init__(self, apiKey, captchaKey, captchaURL):
        self.apiKey = apiKey
        self.captchaKey = captchaKey
        self.captchaURL = captchaURL
        self.captchaResponse = None

    def solveCaptcha(self):
        try:
            req = requests.session()
            req.verify = False
            startReq = req.get(f'https://2captcha.com/in.php?key={self.apiKey}&method=userrecaptcha&googlekey={self.captchaKey}&pageurl={self.captchaURL}&json=1')
            request = startReq.json()['request']
            if 'status":1' in startReq.text:
                sleep(5)
                while True:
                    checkReq = req.get(f'https://2captcha.com/res.php?key={self.apiKey}&action=get&id={request}&json=1')
                    if 'status":1' in checkReq.text:
                        self.captchaResponse = checkReq.json()['request']
                        return self.captchaResponse
                    if 'ERROR_CAPTCHA_UNSOLVABLE' in checkReq.text:
                        return ResponseType.BANNED
            else:
                return ResponseType.FAILURE
        except:
            return ResponseType.BANNED

