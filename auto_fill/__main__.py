from datetime import datetime
from fill import fill_on_release


if __name__ == "__main__":

    # Do not run if not monday.
    if datetime.now().weekday() != 0:
        exit()

    # Release time
    release = datetime.now().replace(hour=8, minute=30, second=0)

    assert fill_on_release(release), 'Form failed to fill.'
    print('Form filled')


