from tkinter import *  # Импортируем все
from tkinter import ttk  # Библиотека для создания виджетов
from tkinter import messagebox as mb  # Для всплывающих информационных окон
import requests  # библиотека для работы с HTTP запросами для API CoinGecko
import datetime  # для работы с датой и временем
import time  # для работы с датой и временем


def update_b_label(event):
    # Получаем полное название базовой валюты из словаря и обновляем метку, когда пользователь выбирает валюту из выпадающего меню
    code = base_combobox.get()
    name = base_options[code]
    b_label.config(text=name)


def update_t_label(event):
    # Получаем полное название криптовалюты из словаря и обновляем метку, когда пользователь выбирает валюту из выпадающего меню
    code = target_combobox.get()
    name = crypto_options[code]
    t_label.config(text=name)


def exchange():
    # Получаем данные от и отправляем информацию в всплывающее информационное окно, когда пользователь нажимает кнопку "КУРС ОБМЕНА"
    curry = target_combobox.get()
    basic = base_combobox.get()

    if curry and basic:
        try:
            response = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={curry.lower()}&vs_currencies={basic.lower()}"
            )
            response.raise_for_status()  # если статус запроса HTTP "200 ОК"
            # Пользуемся методом json() для парсинга информации. Полученные данные сохраняем в переменную data.
            data = response.json()
            # проверяем, есть ли ключ curry.lower в словаре и ключ basic.lower в словаре data[curry.lower()]
            if curry.lower() in data and basic.lower() in data[curry.lower()]:
                # если предыдущие условия выполнены, сохраняем данные курса валют из словаря data[curry.lower()] в переменную exchange_rate.
                exchange_rate = data[curry.lower()][basic.lower()]
                basic = base_options[basic]
                target = crypto_options[curry]
                # Добавляем метод для отображения текущего года, месяца и даты, когда данные курса валют были получены
                n = datetime.datetime.now()
                now = n.strftime("%d-%m-%Y")
                mb.showinfo(
                    f"Курс обмена на {now}: ",
                    f"Курс {exchange_rate:.1f} {basic} за 1 {target} на дату {now}",
                )
            else:
                mb.showerror("Ошибка", f"Валюта {curry} не найдена")
        # Проверяем все возможные ошибки и исключения, которые могут возникнуть в работе кода
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют")


# Список криптовалюты
crypto_options = {
    "Bitcoin": "Bitcoin",
    "Ethereum": "Ethereum",
    "Solana": "Solana",
    "WPTC": "Wrapped Bitcoin",
    "Tether": "Tether",
}

# Список валюты
base_options = {"USD": "Доллар США", "EUR": "Евро", "RUB": "Рубль"}

# Создаем главное окно
window = Tk()
window.title("Курс криптовалюты - КРИПТ")
window.geometry("360x300")
window.iconbitmap("rose.ico")

# Создаем выпадающее меню
Label(
    text="ВАЛЮТА: USD, EUR, RUB", bg="#c9c9d6", fg="#132440", font="Arial 10 bold"
).pack(padx=10, pady=5)
base_combobox = ttk.Combobox(values=list(base_options.keys()))
base_combobox.pack(padx=10, pady=5)
base_combobox.bind(
    "<<ComboboxSelected>>", update_b_label
)  # метод bind для связки элементов из выпадающего меню и функции update_b_label
b_label = ttk.Label()
b_label.pack(padx=10, pady=10)

Label(text="КРИПТОВАЛЮТА:", bg="#c9c9d6", fg="#132440", font="Arial 10 bold").pack(
    padx=10, pady=5
)
target_combobox = ttk.Combobox(values=list(crypto_options.keys()))
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)
# метод bind для связки элементов из выпадающего меню и функции update_t_label
t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(
    text="КУРС ОБМЕНА",
    bg="#132440",
    fg="#f9f8f8",
    font="Arial 10 bold",
    command=exchange,
).pack(padx=10, pady=10)


window.mainloop()
