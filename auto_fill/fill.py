from datetime import datetime, timedelta
import requests
from lxml import html
import attr


_UCSA_DENTAL_URL = 'https://ucsa.org.nz/support/dental/'
_UCSA_DENTAL_FORM = 'https://ucsa.org.nz/support/dental/#ctl00_dentalform_section'


_FORM_VALUES = {
    'ctl00$dentalform$question_30$txtTextbox': 'first_name',
    'ctl00$dentalform$question_31$txtTextbox': 'last_name',
    'ctl00$dentalform$question_32$txtTextbox': 'student_id',
    'ctl00$dentalform$question_34$radioList': 'is_undergrad', # 76 or 77
    'ctl00$dentalform$question_35$radioList': 'is_domestic', # 78 or 79
    'ctl00$dentalform$question_36$txtTextbox': 'email',
    'ctl00$dentalform$question_37$txtTextbox:': 'email',
    'ctl00$dentalform$question_38$txtTextbox': 'phone',
    'ctl00$dentalform$question_39$radioList': 'clinic', # 83 or 84
    'ctl00$dentalform$question_40$txtTextbox': 'reason',
}

_FORM_REQUIRED = {
    'ctl00$dentalform$question_41$radioList': '86',  # 86
    'ctl00$dentalform$btnSubmit': 'Finish'  # Finish
}


# Request headers
_HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'x-mwapps-appid': 'EC1D38D7-D359-48D0-A60C-D8C0B8FB9DF9',
    'x-mwapps-client': 'enduserweb',
    'x-mwapps-clientversion': '1.3.3-1096,enduserweb'
}


@attr.s
class Info:
    first_name: str = attr.ib()
    last_name: str = attr.ib()
    student_id: str = attr.ib()
    is_undergrad: int = attr.ib(converter=lambda x: 76 if bool(x) else 77)
    is_domestic: int = attr.ib(converter=lambda x: 78 if bool(x) else 79)
    email: str = attr.ib()
    phone: str = attr.ib()
    clinic: int = attr.ib(converter=lambda x: 83 if bool(x) or x == 'Ilam Dental' else 86)
    reason: str = attr.ib()
        


def fill(data) -> bool:
    info = Info(data)
    post_json = _FORM_REQUIRED
    post_json.update(form_view_state())
    post_json.update({k: info.__getattribute__(v) for k, v in _FORM_VALUES.items()})
    r = requests.post(headers=_HEADERS, url=_UCSA_DENTAL_FORM, json=post_json)
    return True


def form_view_state():
    r = requests.get(headers=_HEADERS, url=_UCSA_DENTAL_URL)
    tree = html.fromstring(r.content)
    return {
        '__EVENTTARGET' : '',
        '__EVENTARGUMENT' : '',
        '__VIEWSTATE': tree.xpath("//input[@id='__VIEWSTATE']")[0].value,
        '__VIEWSTATEGENERATOR' : tree.xpath("//input[@id='__VIEWSTATEGENERATOR']")[0].value
    }


def form_exists() -> bool:
    """
    Checks if the form exists .
    :return: True if the form exist otherwise False.
    """
    r = requests.get(headers=_HEADERS, url=_UCSA_DENTAL_URL)
    tree = html.fromstring(r.content)
    items = tree.xpath("//div[@class='msl_notification']/span[@class='msl_info']")
    return len(items) == 0


def block_til_release(release) -> None:
    """
    Block until opening.
    :param release: The release time.
    """
    now = datetime.now()
    while now < release:
        now = datetime.now()


def block_till_form_exist(release, wait) -> bool:
    """
    Blocks until the den form exists until a wait time is reach at which point it is assumed the form is
    not available.
    :param release: The expected realises time of the form.
    :param wait: The maximum time to wait for the form.
    :return: True if the form exists.
    """
    has_form = False
    while not has_form and datetime.now() < release + wait:
        has_form = form_exists()
    return has_form


def fill_on_release(release, data, wait=timedelta(minutes=10)) -> bool:
    """
    Fill the form when it is released
    :param release: The time the form is released.
    :param wait: The maximum time to wait for the form.
    :return: True
    """
    block_til_release(release)
    if block_till_form_exist(release, wait):
        return fill(data)
    else:
        return False
