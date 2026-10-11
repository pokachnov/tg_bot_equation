from typing import NoReturn
from math import sqrt
import numpy as np
import config
import telebot
from telebot import types
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv("token.env")
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

#Доп. информация
def dop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back)
    bot.send_message(message.chat.id, "О способах решения уравнений: \nРешение через дискриминант - "
                                      "самый частый и проcтой способ решения квадратных уравнений, этот "
                                      "термин ввёл британский математик Джеймс Джозеф Сильвестр (1814—1897)\n"
                                      "Решение через теорему Виета - для данного способа нужен положительный дискриминант, "
                                      "только в этом случае его можно использовать. Первым вывел формулы Виета одноимённый "
                                      "французский математик Франсуа Виет. \n"
                                      "Решение через сумму коэффицентов является частными случаями Виеты, так же как и четный дискриминант "
                                      "является частным случаем обычного дискриминанта. \n"
                                      "Решение графическим способом - самое понятное и красивое, но не всегда точное. \n"
                                      "О боте: Создал этого телеграмм бота ученик 10А класса школы №1694 в качестве индивидуального проекта. \n"
                                      "Дробные коэффиценты следует вводить через точку, а не запятую", reply_markup = markup)

# решение квадратных уравнений
def solve_quadratic_equation(message):
    ans = []
    if len(message.text.split()) != 3:
      bot.send_message(message.chat.id, "Выбери заново")
      return
    a, b, c = message.text.split()
    a = float(a)
    b = float(b)
    c = float(c)
    d = b**2 - 4*a*c
    if d > 0:
        x1 = (-b + sqrt(d)) / (2*a)
        x2 = (-b - sqrt(d)) / (2*a)
        ans.append(x1)
        ans.append(x2)
    elif d == 0:
        x1 = -b / (2*a)
        ans.append(x1)
    else:
        ans = "Нет корней"
    #все решения
    if (d > 0):
        bot.send_message(message.chat.id, "Вот все решения, которыми можно решить это уравнение, выбирайте самый удобный")
        if (a + b + c) == 0:
            bot.send_message(message.chat.id, f"Так как сумма коэффицентов равна 0, то \nx1 = 1, x2 = c/a = {round(c/a, 6)}")
        if (a - b + c) == 0:
            bot.send_message(message.chat.id, f"Так как сумма 1(a) и 3(c) коэффицентов равна 2(b) коэффиценту, то \nx1 = -1, x2 = -c/a = {round(-c/a, 6)}")
        x1 = round((-b + sqrt(d)) / (2*a), 6)
        x2 = round((-b - sqrt(d)) / (2*a), 6)
        x1v = float()
        x2v = float()
        x1v = ((-b/a + sqrt((b**2 - 4*a*c)/a**2))/2)
        x2v = ((-b/a - sqrt((b**2 - 4*a*c)/a**2))/2)
        bot.send_message(message.chat.id, f"По теореме Виета можно, либо угадать корни, либо решить систему \nx1 + x2 = -b/a \nx1 * x2 = c/a \nx1 = {x1}, x2 = {x2}")
        bot.send_message(message.chat.id, f"С помощью дискриминанта можно найти корни \nD = b^2 - 4ac = {d} \nx1 = (-b + √D)/2a \nx2 = (-b - √D)/2a \nx1 = {x1}, x2 = {x2}")
        if (b % 2 == 0):
            k = b/2
            d_4 = k**2 - a*c
            x1_4 = round((-k + sqrt(d_4))/a, 6)
            x2_4 = round((-k - sqrt(d_4))/a, 6)
            bot.send_message(message.chat.id, f"Так как коэффицент b четный, то с помощью четного дискриминанта можно найти корни \nD/4 = (b/2)^2 - ac = {d_4} \nx1 = (-b/2 + √D/4)/a \nx2 = (-b/2 - √D/4)/a \nx1 = {x1_4}, x2 = {x2_4}")
    elif (d == 0):
        bot.send_message(message.chat.id, "Вот все решения, которыми можно решить это уравнение, выбирайте самый удобный")
        x = round(-b/(2*a), 6)
        if (x >= 0):
            bot.send_message(message.chat.id, f"Так как дискриминант равен 0, то квадратный трёхчлен можно преставить в виде квадрата разности \n{a}*(x - {x})^2 = 0 \nx = {x}")
        else:
            bot.send_message(message.chat.id, f"Так как дискриминант равен 0, то квадратный трёхчлен можно преставить в виде квадрата разности \n{a}*(x + {-x})^2 = 0 \nx = {x}")
        bot.send_message(message.chat.id, f"С помощью дискриминанта можно найти корни \nD = b^2 - 4ac = 0 \nx = -b/a = {x}")

    x = np.linspace(-10, 10, 1000)
    y = a*x**2 + b*x + c
    fig, ax = plt.subplots()
    ax.plot(x, y, color = "blue")
    plt.title('График функции')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.xlim(-10, 10)
    plt.ylim(-10, 20)
    plt.xticks(np.arange(min(x), max(x)+1, 1))
    plt.yticks(np.arange(-10, 20, 2))
    # plot X - axis
    plt.axhline(y=0, color='k')
    # plot Y - axis
    plt.axvline(x=0, color='k')
    plt.savefig('sine_plot.png')
    photo = open('sine_plot.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back)
    if (ans != "Нет корней"):
        msg = bot.send_message(message.chat.id, f"Ответ квадратного уравнения: {', '.join(map(str, np.around(ans, 6)))}" , reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, f"Ответ: нет корней, так как D < 0" , reply_markup=markup)

# решение кубических уравнений
def solve_kub_equation(message):
    ans = ''
    if len(message.text.split()) != 4:
      bot.send_message(message.chat.id, "Выбери заново")
      return
    a, b, c, d = message.text.split()
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    arr = np.roots([a, b, c, d])
    arr = arr.real[abs(arr.imag)<1e-5]
    arr = np.round(arr, 6)
    if len(arr) == 0 :
      ans = "Нет корней"
    else:
      ans = arr.tolist()
      ans = set(ans)
    #все решения
    if d == 0:
        bot.send_message(message.chat.id, f"Можно вынести x за скобку, и во второй скобке получится квадратный трёхчлен, если требуется можете решить его в нашем же боте")
        if len(ans) == 1:
            bot.send_message(message.chat.id, "Уравнение в скобках не имеет действительных корней, так как дискриминант < 0, значит единственным корнем будет 0")
        if len(ans) == 2:
            bot.send_message(message.chat.id, f"Так дискриминат уравнения в скобках = 0, Корень уравнения: x1, x2 = {', '.join(map(str, ans))}")
        if len(ans) == 3:
            bot.send_message(message.chat.id, f"Так дискриминат уравнения в скобках > 0, Корни уравнения: x1, x2, x3 = {', '.join(map(str, ans))}")

    if (a + b + c + d == 0):
        x1_3 = 1
        bot.send_message(message.chat.id, "Так как сумма коэффицентов равна 0, то одним из корней уравнения будет 1 \nЧтобы найти остальные корни надо поделить искомое уравнение на многочлен x - 1")
        arr_1, arr_2 = (np.polydiv([a, b, c, d], [1, -1]))
        a_n = arr_1[0]
        b_n = arr_1[1]
        c_n = arr_1[2]
        bot.send_message(message.chat.id, f"Поделив многочлен на многочлен получилось квадратное уравнение {a_n}x^2 + {b_n}x + {c_n} = 0, его надо решить, если требуется можете решить его в нашем же боте")
        result_kub = np.roots(arr_1)
        result_kub = result_kub.real[abs(result_kub.imag)<1e-5]
        result_kub = np.round(result_kub, 6)
        result_kub = result_kub.tolist()
        if not result_kub:
            bot.send_message(message.chat.id, "Квадратное уравнение не имеет действительных корней, так как дискриминант < 0")
        elif (len(result_kub) == 2):
            bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[0]}, x2 = {result_kub[1]}, x3 = 1")
        else:
            bot.send_message(message.chat.id, f"Так дискриминат уравнения в скобках = 0, Корни уравнения: x1 = {result_kub}, x2 = 1")

    if (a + c == b + d):
        x1_3 = -1
        bot.send_message(message.chat.id, "Так как сумма коэффициентов кубического уравнения при чётных степенях равна сумме коэффициентов при нечётных степенях, то одним из "
                                          "корней уравнения будет -1 \nЧтобы найти остальные корни надо поделить искомое уравнение на многочлен x + 1")
        arr_1, arr_2 = (np.polydiv([a, b, c, d], [1, 1]))
        a_n = arr_1[0]
        b_n = arr_1[1]
        c_n = arr_1[2]
        bot.send_message(message.chat.id, f"Поделив многочлен на многочлен получилось квадратное уравнение {a_n}x^2 + {b_n}x + {c_n} = 0, его надо решить")
        result_kub = np.roots(arr_1)
        result_kub = result_kub.real[abs(result_kub.imag)<1e-5]
        result_kub = np.round(result_kub, 6)
        result_kub = result_kub.tolist()
        if not result_kub:
            bot.send_message(message.chat.id, "Квадратное уравнение не имеет действительных корней, так как дискриминант < 0, значит x1 = -1")
        elif (len(result_kub) == 2):
            if (result_kub[0] == -1.0):
                bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[1]}, x2 = -1")
            elif (result_kub[1] == -1.0):
                bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[0]},x2 = -1")
            else:
                bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[0]}, x2 = {result_kub[1]}, x3 = -1")
        else:
            bot.send_message(message.chat.id, f"Так дискриминат уравнения в скобках = 0, Корни уравнения: x1 = {result_kub}, x2 = -1")
    if (round(d) == d and d != 0):
        mas = [1, -1]
        for i in range(2, int(abs(d))+1):
            if d % i == 0:
                mas.append(i)
                mas.append(-i)
        for elem in mas:
            if (a*pow(elem, 3) + b*pow(elem, 2) + c*elem + d == 0):
                arr_1, arr_2 = (np.polydiv([a, b, c, d], [1, -elem]))
                result_kub = np.roots(arr_1)
                result_kub = result_kub.real[abs(result_kub.imag)<1e-5]
                result_kub = np.round(result_kub, 6)
                result_kub = result_kub.tolist()
                a_n = arr_1[0]
                b_n = arr_1[1]
                c_n = arr_1[2]
                if elem >= 0:
                     bot.send_message(message.chat.id, f"Подставляя делители последнего свободного члена d в уравнение вместо x, надо найти тот случай, когда сумма равна 0"
                                                        f", в таком случае этот делитель будет одним из корней уравнения, после чего надо делить искомое уравнение на многочлен x - {int(elem)}")
                else:
                     bot.send_message(message.chat.id, f"Подставляя делители последнего свободного члена d в уравнение вместо x, надо найти тот случай, когда сумма равна 0"
                                                       f", в таком случае этот делитель будет одним из корней уравнения, после чего надо делить искомое уравнение на многочлен x + {-int(elem)}")
                elem = 1
                break
        if (elem == 1):
            bot.send_message(message.chat.id, f"Поделив многочлен на многочлен получилось квадратное уравнение {a_n}x^2 + {b_n}x + {c_n} = 0, его надо решить")
            if not result_kub:
                bot.send_message(message.chat.id, f"Квадратное равнение не имеет действительных корней, так как дискриминант < 0, значит x1 = {elem}")
            elif (len(result_kub) == 2):
                if (result_kub[0] == elem):
                    bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[1]}, x2 = {elem}")
                elif (result_kub[1] == elem):
                    bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[0]},x2 = {np.euler_gamma}")
                else:
                    bot.send_message(message.chat.id, f"Корни уравнения: x1 = {result_kub[0]}, x2 = {result_kub[1]}, x3 = {elem}")
            else:
                bot.send_message(message.chat.id, f"Так дискриминат уравнения в скобках = 0, Корни уравнения: x1 = {result_kub}, x2 = {elem}")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back)
    if (ans != "Нет корней"):
        msg = bot.send_message(message.chat.id, f"Ответ кубического уравнения: {', '.join(map(str, ans))}" , reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, f"Ответ: нет корней, так как D < 0" , reply_markup=markup)


# начало работы бота
@bot.message_handler(commands=['start'])

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Вводить коэффиценты для квадратного уравнения")
    btn2 = types.KeyboardButton("Вводить коэффиценты для кубического уравнения")
    btn3 = types.KeyboardButton("Дополнительная информация")
    markup.add(btn1).row(btn2).row(btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для решения квадратных и кубических уравнений".format(message.from_user), reply_markup=markup)
# остальная часть
@bot.message_handler(content_types=['text'])

def func(message):
    if(message.text == "Вводить коэффиценты для квадратного уравнения"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, "Введите a, b, c (писать через пробел) в уравнении ax^2 + bx + c = 0")
        bot.register_next_step_handler(msg, solve_quadratic_equation)

    elif(message.text == "Вводить коэффиценты для кубического уравнения"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg_1 = bot.send_message(message.chat.id, "Введите a, b, c, d  (писать через пробел) в уравнении ax^3 + bx^2 + cx + d = 0")
        bot.register_next_step_handler(msg_1, solve_kub_equation)

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Вводить коэффиценты для квадратного уравнения")
        btn2 = types.KeyboardButton("Вводить коэффиценты для кубического уравнения")
        btn3 = types.KeyboardButton("Дополнительная информация")
        markup.add(btn1).row(btn2).row(btn3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    elif(message.text == "Дополнительная информация"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg_2 = bot.send_message(message.chat.id, "Дополнительная информация о боте и способах решения")
        dop(msg_2)
bot.polling(none_stop=True)