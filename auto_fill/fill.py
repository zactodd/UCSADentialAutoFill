from datetime import datetime, timedelta


_UCSA_DENTAL_URL = 'https://ucsa.org.nz/support/dental/'


def fill() -> bool:
    return False


def form_exists() -> bool:
    """
    Checks if the form exists .
    :return: True if the form exist otherwise False.
    """
    return False


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


def fill_on_release(release, wait=timedelta(minutes=10)) -> bool:
    """
    Fill the form when it is released
    :param release: The time the form is released.
    :param wait: The maximum time to wait for the form.
    :return: True
    """
    block_til_release(release)
    if block_till_form_exist(release, wait):
        return fill()
    else:
        return False
