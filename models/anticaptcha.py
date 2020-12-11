from anticaptchaofficial.recaptchav2proxyless import *
from models.enums.response_type import ResponseType
from time import sleep
import requests

import traceback

class AntiCaptcha():
    def __init__(self, apiKey, captchaKey, captchaURL):
        self.apiKey = apiKey
        self.captchaKey = captchaKey
        self.captchaURL = captchaURL
        self.captchaResponse = None

    def solveCaptcha(self):
        solver = recaptchaV2Proxyless()
        solver.set_key(self.apiKey)
        solver.set_website_url(self.captchaURL)
        solver.set_website_key(self.captchaKey)

        g_response = solver.solve_and_return_solution()

        if g_response != 0:
            return g_response
        
        return ResponseType.BANNED

