from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time

lines = []
    # Открываем файл на чтение
with open('input.txt', 'r') as file:
        # Читаем строки из файла и добавляем их в список
    for line in file:
        lines.append(line.strip())  # Удаляем пробельные символы из начала и конца строки
print(lines)

def main(url):
    with sync_playwright() as p:
        # Запускаем браузер с прокси
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        stealth_sync(page)
        page.goto(url)
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    for url in lines:
        main(url=url)

