import datetime

def get_now() -> str:
    return datetime.datetime.now()

def get_current_time() -> str:
    return get_now().strftime("%Y-%m-%d %H:%M:%S")

def get_yesterday() -> str:
    now = get_now()
    if now.weekday() == 0:
        yesterday = now - datetime.timedelta(days=3)
        yesterday = str(yesterday).split(" ")[0]
    else:
        yesterday = now - datetime.timedelta(days=1)
        yesterday = str(yesterday).split(" ")[0]

def get_today() -> str:
    return get_now().split(" ")[0]
