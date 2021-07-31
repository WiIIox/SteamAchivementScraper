from openpyxl import Workbook
from requests import get
from bs4 import BeautifulSoup
from datetime import *
from time import strptime

url = str(input("Input a URL, example:\n\nhttps://steamcommunity.com/id/willox25565/stats/271590/?tab=achievements\n\nURL here: "))

page = get(url)
soup = BeautifulSoup(page.text, "html.parser")
achivements_raw = soup.find_all("div", {"class" : "achieveRow"})

wb = Workbook()
ws = wb.active
ws.append(["Achivement", "Description", "Unlocked"])
ws.column_dimensions["A"].width, ws.column_dimensions["B"].width, ws.column_dimensions["C"].width = 35, 120, 20

def trans(text):
    date, time = text.split("@")
    time = str(datetime.strptime(time, ' %I:%M%p').time())[:-3]
    date = f"{date.split()[0].zfill(2)}.{str(strptime(date.split()[1].replace(',', ''),'%b').tm_mon).zfill(2)}.{date.split()[2] if len(date.split()) == 3 else datetime.today().year}"
    return f"{date} {time}"

achivements = {}

for achivement in achivements_raw:

    name = achivement.find("h3", {"class" : "ellipsis"}).text.strip()
    description = achivement.find("h5").text.strip()
    unlock_time = achivement.find("div", {"class" : "achieveUnlockTime"})
    unlock_time = trans(unlock_time.text.replace("Unlocked", "").strip()) if unlock_time else "Not unlocked yet"

    achivements[name] = (description, unlock_time)

achivements = dict(sorted(achivements.items(), key=lambda item: datetime.strptime(item[1][1], "%d.%m.%Y %H:%M")))

for achivement in achivements:
    ws.append([achivement, achivements[achivement][0], achivements[achivement][1]])

wb.save(f"{url.split('/')[6]}_achivements_{url.split('/')[4]}.xlsx")
