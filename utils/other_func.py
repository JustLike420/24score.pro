# - *- coding: utf- 8 - *-
import csv
import re
import requests
from aiogram import Dispatcher
from bs4 import BeautifulSoup
from data.config import admins
from loader import bot

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '_ym_d=1649015182; _ym_uid=1649015182161139046; PHPSESSID=73camdjqhurm2tivktifb9p1n7; _gid=GA1.2.2129621727.1650751535; _ym_isad=1; _ga=GA1.1.1544845135.1649015182; _ga_NJHWL0WP7F=GS1.1.1650753703.20.1.1650755754.0',
    'Host': 'old.24score.pro',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0'

}

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_ID = '135r3A_Zskwwa1Ct3hmCb4M_YZ0hTSpxp4yqfvfS2MqQ'


# Уведомление и проверка обновления при запуске скрипта
async def on_startup_notify(dp: Dispatcher):
    if len(admins) >= 1:
        await send_all_admin(f"<b>✅ Бот был успешно запущен</b>")


# Рассылка сообщения всем администраторам
async def send_all_admin(message, markup=None, not_me=0):
    if markup is None:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, disable_web_page_preview=True)
            except:
                pass
    else:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass


# парсинг меню для выбора турнира
def get_menu(sport):
    if sport == 'hockey':
        url = 'https://old.24score.pro/ice_hockey/'
    elif sport == 'football':
        url = 'https://old.24score.pro/'
    elif sport == 'basketball':
        url = 'https://old.24score.pro/basketball/'
    link_list = {
    }
    tournament_title = ''
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    country_table = soup.find('ul', class_='countries').find_all('li')
    for tournament in country_table:
        if tournament.has_attr('title'):
            tournament_title = tournament.text.strip()
            link_list[tournament_title] = []
        else:
            link_list[tournament_title].append(
                tournament.text + ' | ' + 'https://old.24score.pro' + tournament.find('a').get('href'))
    return link_list


async def parse_table(url, name_tour):
    r = requests.get(url,
                     headers=headers)
    print(url)
    src = r.text
    soup = BeautifulSoup(src, 'lxml')
    name_tour1 = soup.find('div', class_='select_row').text.split('.')[1]
    script_text = soup.find_all('script')[2].text
    reg = re.findall(r'data: {\"data_key\" : \"(\w*)\"', script_text)[0]

    req = requests.get(f'https://old.24score.pro/backend/load_page_data.php?data_key={reg}', headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    table = soup.find('div', id='fulllist_0').find_all('tr')
    tour = ''
    all_data = []
    for tr in table:
        tds = tr.find_all('td')
        line = []

        for td in tds:
            line.append(td.text.strip())
        if len(line) > 0:
            if 'Тур' in line[0]:
                tour = line[0].replace('Тур ', '')

            elif line[0] != 'Сокращенный список матчей' and line[1] != '1':
                line.insert(0, tour)
                line.insert(0, '')
                line[4] = ' '.join(line[4].split())
                line[5] = ' '.join(line[5].split())
                print(line[:6])
                all_data.append(line[:6])
    all_data.reverse()
    all_data[0][0] = name_tour1
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(
            all_data
        )


creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
API = build('sheets', 'v4', credentials=creds)


def find_sheet_id_by_name(sheet_name):
    sheets_with_properties = API \
        .spreadsheets() \
        .get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties') \
        .execute() \
        .get('sheets')
    for sheet in sheets_with_properties:
        if 'title' in sheet['properties'].keys():
            if sheet['properties']['title'] == sheet_name:
                return sheet['properties']['sheetId']


def push_csv_to_gsheet(sheet_id, worksheet_name, column=0):
    with open('data.csv', 'r', encoding='utf-8') as csv_file:
        csvContents = csv_file.read()
    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": sheet_id,
                    "rowIndex": "0",
                    "columnIndex": f"{column}",
                },
                "data": csvContents,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }
    # if worksheet_name == 'Hockey':
    #     range1 = "'Hockey'!A1:K1500"
    # elif worksheet_name == 'Football':
    #     range1 = "'Football'!A1:N1500"
    # else:
    #     range1 = ''
    # request1 = API.spreadsheets().values().clear(
    #     spreadsheetId=SPREADSHEET_ID,
    # ).execute()
    # print(request1)
    request = API.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body)
    response = request.execute()
    return response


def parse_today(sport):
    if sport == 'hockey':
        url = 'https://old.24score.pro/ice_hockey/'
    elif sport == 'football':
        url = 'https://old.24score.pro/'
    elif sport == 'basketball':
        url = 'https://old.24score.pro/basketball/'
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    champs = soup.find_all('th', class_='champheader')
    champs_list = []
    for champ in champs:
        champs_list.append(champ.text + " | " + champ.find('a').get('href'))

    return champs_list


def get_date_time(url):
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    section = soup.find('select', class_='sel_season').find_all('option')
    times = []
    for sec in section:
        times.append(sec.text)
    return times
