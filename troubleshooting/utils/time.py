from datetime import datetime

def getCurrentDateTime():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def getCurrentTime():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M')

def getCurrentDate():
    now = datetime.now()
    return now.strftime('%Y-%m-%d')
