import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("menu_text, link_text, expected_url", [
    ("Решения", "Финансы", "https://servicepipe.ru/finance"),
    ("Решения", "Ритейл", "https://servicepipe.ru/retail"),
    ("Решения", "Маркетинг", "https://servicepipe.ru/marketing"),
    ("Решения", "Защита веб-приложений и API", "https://servicepipe.ru/web"),
    ("Решения", "Защита IT-инфраструктуры", "https://servicepipe.ru/network"),
    ("Решения", "Тестирование безопасности", "https://servicepipe.ru/audit"),
    ("Технологии", "Servicepipe FlowCollector", "https://servicepipe.ru/flowcollector"),
    ("Технологии", "Servicepipe DosGate", "https://servicepipe.ru/dosgate"),
    ("Технологии", "Servicepipe Cybert", "https://servicepipe.ru/cybert"),
    ("Продукты", "Web DDoS Protection", "https://servicepipe.ru/web/ddos-protection"),
    ("Продукты", "Bot Protection", "https://servicepipe.ru/web/bot-protection"),
    ("Продукты", "BotChecks (Free)", "https://servicepipe.ru/web/bot-checks"),
    ("Продукты", "WAF", "https://servicepipe.ru/web/waf"),
    ("Продукты", "Network DDoS Protection", "https://servicepipe.ru/network/ip-transit"),
    ("Продукты", "Cloud Firewall", "https://servicepipe.ru/network/cloud-firewall"),
    ("Продукты", "Secondary DNS", "https://servicepipe.ru/network/slave-dns"),
    ("Продукты", "Stress-test", "https://servicepipe.ru/audit/stress-test"),
    ("О компании", "История", "https://servicepipe.ru/about"),
    ("О компании", "Карьера", "https://servicepipe.ru/career"),
    ("О компании", "Контакты", "https://servicepipe.ru/contacts"),
    ("О компании", "Пресс-центр", "https://servicepipe.ru/press-center"),
    ("О компании", "Почему мы", "https://servicepipe.ru/why-servicepipe"),
    ("О компании", "Партнёрам", "https://servicepipe.ru/partners"),
    ("Личный кабинет", "Личный кабинет", "https://control.servicepipe.ru/signin"),
])
def test_navigation(menu_text, link_text, expected_url):
    with sync_playwright() as p:
        # Запуск браузера (запуск для Chromium и Firefox)
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=False, slow_mo=500)
            page = browser.new_page(viewport={"width": 1024, "height": 768})  # Установка разрешения

            # Переход на главную страницу
            print("Открываем главную страницу...")
            page.goto("https://servicepipe.ru", wait_until="domcontentloaded")

            # Проверка заголовка страницы
            assert "Servicepipe" in page.title(), "Главная страница не загрузилась"
            print(f"Заголовок страницы: {page.title()}")

            # Открытие сэндвич-меню для мобильного вида (если оно скрыто)
            print("Ожидание кнопки сэндвич-меню...")
            page.wait_for_selector('button[aria-label="show menu"]', timeout=30000)
            page.locator('button[aria-label="show menu"]').click()

            # Ожидание кнопки меню
            print(f"Ожидание кнопки меню '{menu_text}'...")
            page.wait_for_selector(f'button:has-text("{menu_text}")', timeout=30000)

            # Прокрутка и клик по кнопке меню
            button = page.locator(f'button:has-text("{menu_text}")')
            button.scroll_into_view_if_needed()
            button.click()

            # Ожидание ссылки в меню
            print(f"Ожидание ссылки '{link_text}'...")
            page.wait_for_selector(f'a:has-text("{link_text}")', timeout=30000)
            page.click(f'a:has-text("{link_text}")')

            # Ожидание загрузки новой страницы
            print(f"Ожидание загрузки страницы {expected_url}...")
            page.wait_for_load_state('load', timeout=60000)  # Увеличиваем таймаут до 60 секунд
            assert page.url == expected_url, f"Ожидаемый URL {expected_url}, но получен {page.url}"

            # Переход обратно на главную страницу
            print("Переход на главную страницу...")
            page.goto("https://servicepipe.ru", wait_until="domcontentloaded")

            # Проверка возвращения на главную страницу
            print("Проверка загрузки главной страницы...")
            assert page.url.rstrip('/') == "https://servicepipe.ru", f"Не удалось вернуться на главную страницу. Текущий URL: {page.url}"

            # Закрытие браузера
            browser.close()
