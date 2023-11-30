

"""import fitz

def insert_fullname_into_pdf(pdf_path, data, output_path):
    doc = fitz.open(pdf_path)
    new_doc = fitz.open()
    '''
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        fonts = page.get_fonts()
        for font in fonts:
            print(font)'''
    for page in doc:
        text = page.get_text("text")
        new_page = new_doc.new_page()
        for item, key in data.items():
            text = text.replace(item, str(key))
        new_page.insert_text((50, 72), text, fontsize=12, fontname="Arial", fontfile='C:\\Windows\\Fonts\\ariali.ttf')

    new_doc.save(output_path)

pdf_path = "car.pdf"  # Путь к исходному PDF-документу
output_path = 'dogovor.pdf'

insert_fullname_into_pdf(pdf_path, data, output_path)"""

'''from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



def create_contract_with_name(full_name):
    # Загрузите кириллический шрифт
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c = canvas.Canvas("contract.pdf", pagesize=letter)
    c.setFont("Arial", 12)
    c.drawString(100, 500, "Договор между " + full_name + " и компанией")
    c.save()

# Передайте ФИО, которое должно быть вставлено в PDF-документ
user_full_name = "Иванов Иван Иванович"
create_contract_with_name(user_full_name)'''

"""import os
import string

from twilio.rest import Client
from datetime import datetime, timedelta
import random

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC16c3d5dd0a72e4a1ff09ec7e5e3e47e5'
auth_token = 'c081849fd9b88b2fa9c1e7aa27dfcc9e'
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+447360537609',
                     to='+79233777746'
                 )

print(message.sid)


def code():
    code = ''.join(random.choices(string.digits, k=6))
    current_time = datetime.now()
    print(current_time)
    expired_time = current_time + timedelta(seconds=10)
    print(expired_time)

    return code, expired_time


code_f = code()
code_ver = code_f[0]
expired_time = code_f[1]
print(code_ver)
input_code = input()
if datetime.now() <= expired_time and input_code == code_ver:
    print('Успешно')
elif datetime.now()>= expired_time:
    print('срок истек')
else:
    print('Неверный код')"""




import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from datetime import datetime
import pyautogui
import pygetwindow as gw
import time
import threading
import schedule
import os

vk_session = vk_api.VkApi(token='YOUR_VK_API_TOKEN')  # Replace with your VK API token
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
upload = VkUpload(vk_session)

image_path1 = "C:\\Users\\bratX\\Desktop\\screenshot1.png"
image_path2 = "C:\\Users\\bratX\\Desktop\\screenshot2.png"


def make_screenshot(path, app_name):
    try:
        app_win = gw.getWindowsWithTitle(app_name)[0]
    except (IndexError, gw.PyGetWindowException):
        print(f"Не удалось найти окно с названием '{app_name}'")
        return False

    if not app_win.isMaximized:
        app_win.maximize()

    app_win.activate()
    time.sleep(2)

    screenshot = pyautogui.screenshot(region=(app_win.left, app_win.top, app_win.width, app_win.height))
    screenshot.save(path)

    if app_win.isActive:
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)

    return True


def send_photo(chat_id, app_name, path):
    if not make_screenshot(path, app_name):
        print(f"Не удалось создать скриншот окна '{app_name}'")
        return

    time.sleep(2)

    photo_info = upload.photo_messages(path)[0]
    photo_id = photo_info['id']
    owner_id = photo_info['owner_id']

    attachment = f"photo{owner_id}_{photo_id}"
    vk.messages.send(
        chat_id=chat_id,
        message=f"{app_name}: {datetime.now().strftime('%dДень.%mмесяц %H:%M')}",
        attachment=attachment,
        random_id=0
    )

    if os.path.exists(path):
        os.remove(path)


def send_screenshots(chat_id):
    send_photo(chat_id, 'Discord', image_path1)
    send_photo(chat_id, 'Google Chrome', image_path2)


def scheduled_job(chat_id):
    send_screenshots(chat_id)


def main_loop():
    global longpoll
    while True:
        schedule.run_pending()
        time.sleep(1)

        for event in longpoll.listen():
            try:
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if event.text.lower() == "время":
                            send_screenshots(event.chat_id)

            except Exception as e:
                print(e)
                # Повторное подключение при разрыве соединения
                vk_session = vk_api.VkApi(token='YOUR_VK_API_TOKEN')
                longpoll = VkLongPoll(vk_session)
                send_screenshots(event.chat_id)
                print(f'vk_session: {vk_session} longpoll: {longpoll} send_screenshots: {send_screenshots(event.chat_id)}')

def run_threaded(job_func, chat_id):
    job_func(chat_id)


if __name__ == "__main__":
    chat_id = 43

    for i in range(24):
        schedule.every().day.at(f"{str(i).zfill(2)}:00").do(run_threaded, scheduled_job, chat_id)

    main_loop()
