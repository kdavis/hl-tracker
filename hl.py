import requests
import re
from bs4 import BeautifulSoup


class HargreavesLansdown():
    LOGIN_FORM = "https://online.hl.co.uk/my-accounts/login-step-one"
    LOGIN_STEP_TWO = "https://online.hl.co.uk/my-accounts/login-step-two"
    MY_ACCOUNTS = "https://online.hl.co.uk/my-accounts"
    LOGIN_SUCCESS = False

    def __init__(
        self,
        username: str,
        password: str,
        secureNumber: str,
        dateOfBirth: str
    ):
        self.username = username
        self.password = password
        self.secureNumber = secureNumber
        self.dateOfBirth = dateOfBirth
        self.session = requests.session()

    def parse_token(self, data):
        matches = re.search(
            '<input type="hidden" name="hl_vt" value="([0-9]+)"\/>',
            data
        )
        if matches:
            return matches.group(1)
        return None

    def get_token(self):
        req = self.session.get(self.LOGIN_FORM)
        return self.parse_token(req.content.decode("utf-8"))

    def get_secure_numbers(self, data):
        matches = re.findall('name="secure-number\[([0-9]+?)\]".*?title=".*?([0-9]+).*?"', data, re.S | re.M)
        print(matches)
        return matches

    def login(self):
        login_attempt = self.session.post(self.LOGIN_FORM, data={
            "hl_vt": self.get_token(),
            "username": self.username,
            "date-of-birth": self.dateOfBirth,
            "remember-me": ""
        })
        numbers = self.get_secure_numbers(login_attempt.content.decode("utf-8"))

        dataset = {
            "hl_vt": self.parse_token(login_attempt.content.decode("utf-8")),
            "online-password-verification": self.password,
            "date-of-birth": self.dateOfBirth,
            "submit": "Log+in"
        }

        for i in numbers:
            dataset[f"secure-number[{i[0]}]"] = int(self.secureNumber[int(i[1])-1])

        next_section = self.session.post(
            self.LOGIN_STEP_TWO,
            data=dataset,
            allow_redirects=False
        )
        if next_section.status_code == 302:
            self.LOGIN_SUCCESS = True

    def get_values(self):
        fund_values = self.session.get(self.MY_ACCOUNTS)
        self.fund_values = fund_values

        rows = BeautifulSoup(fund_values.content.decode("utf-8")).find("table", attrs={"class": "accounts-table"}).find("tbody").find_all("tr")
        for row in rows:
            new_set = row.select("td a")
            name = new_set[0].text.strip()
            value = re.sub(r'[^0-9\.]', '', new_set[1].text.strip())

            yield {
                "name": name,
                "value": value
            }

    def is_logged_in(self):
        return self.LOGIN_SUCCESS
