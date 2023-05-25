import datetime as dt

def getTimeFromHrAndMin(hr: int, min: int) -> str:
    pre = ""
    post = ""
    specifyer = ""
    NUM_NAMES = {
        0:"twaalf",
        1:"één",
        2:"twee",
        3:"drie",
        4:"vier",
        5:"vijf",
        6:"zes",
        7:"zeven",
        8:"acht",
        9:"negen",
        10:"tien",
        11:"elf",
        12:"twaalf",
        13:"dertien",
        14:"veertien",
        15:"kwart",
        16:"zestien",
        17:"zeventien",
        18:"achttien",
        19:"negentien",
        20:"twintig",
    }
    if hr == 0 and min == 0: return "Het is middernacht."
    if min == 0 and hr > 0: post = " uur"

    if min == 0:
        pre = ""
    elif min == 30:
        pre = " half"
        hr += 1
    elif min < 20: 
        pre = f" {NUM_NAMES[min]} over"
    elif min > 40: 
        pre = f" {NUM_NAMES[60-min]} voor"
        hr += 1
    elif min > 30:
        pre = f" {NUM_NAMES[min-30]} over half"
        hr += 1
    elif min < 30:
        pre = f" {NUM_NAMES[30-min]} voor half"
        hr += 1

    if hr >= 12 and hr <= 17: specifyer = " 's middags"
    elif hr < 12 and hr >= 5: specifyer = " 's ochtends"
    elif hr > 17 and hr <= 23: specifyer = " 's avonds"
    elif hr >= 0 and hr < 5: specifyer = " 's nachts"

    if hr == 24: hr = 0
    if hr > 12: hr -= 12

    return f"Het is{pre} {NUM_NAMES[hr]}{post}{specifyer}."

def getCurrentTimeInDutch() -> str:
    currentTime = dt.datetime.now()
    return getTimeFromHrAndMin(currentTime.hour, currentTime.minute)