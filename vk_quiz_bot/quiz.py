from config import *
from database import *
import random

GOOD = [
    "🔥 Отлично!",
    "🚀 Верно!",
    "⭐ Молодец!",
    "💪 Так держать!",
    "🎯 Точное попадание!",
    "✨ Прекрасно!",
    "📚 Ты настоящий эрудит!",
    "🎓 Профессорский уровень!",
    "🧠 Мозг кипит! Отлично!",
    "🏆 Ещё одно слово!",
    "✅ Правильно!",
    "👍 Хорошая работа!"
]

BAD = [
    "🤔 Нет такого слова. Посмотри внимательнее на филворд",
    "📖 Попробуй найти другое слово",
    "💡 Не угадал, но ты близко! Попробуй ещё раз",
    "🌀 Это слово не спрятано в филворде",
    "🧐 Может быть, другое слово?",
    "📝 Проверь, как написано слово в филворде",
    "🎯 Почти получилось! Следующее слово точно найдёшь",
    "🌟 Не расстраивайся, ищи дальше!",
    "🔎 Взгляни под другим углом"
]


def start_quiz(send, user_id):
    user = get_user(user_id)

    if user and user[1] == "finished":
        send(user_id, "🎉 Ты уже прошёл викторину!")
        return

    create_user(user_id)

    send(user_id,
         "🔍 Найди 12 терминов в филворде и отправляй их мне.\n\n"
         "Слова могут быть расположены:\n"
         "• по горизонтали →\n"
         "• по вертикали ↓\n"
         "• и даже по диагонали ↗\n\n"
         "Удачи! 🍀")

    send(user_id,
         "",
         attachment=QUIZ_IMAGE)


def check_answer(send, user_id, text):
    user = get_user(user_id)

    if not user:
        send(user_id, "Нажми 'Начать игру', чтобы начать викторину")
        return

    if user[1] == "finished":
        send(user_id, "🏆 Ты уже победитель! Покажи сообщение организатору")
        return

    words = user[2].split(",") if user[2] else []
    word = text.lower().strip()

    if word not in CORRECT_WORDS:
        send(user_id, random.choice(BAD))
        return

    if word in words:
        send(user_id, "🔁 Ты уже находил это слово! Ищи дальше 👀")
        return

    words.append(word)
    update_words(user_id, words)

    progress = len(words)
    remaining = REQUIRED_WORDS - progress

    if progress == REQUIRED_WORDS:
        good_phrase = "🎉🏆 ПОБЕДА! 🏆🎉\nТы нашёл все слова!"
    elif progress >= REQUIRED_WORDS - 3:
        good_phrase = f"{random.choice(GOOD)}\n🔥 Осталось всего {remaining} слова!"
    elif progress >= REQUIRED_WORDS // 2:
        good_phrase = f"{random.choice(GOOD)}\n📊 Прогресс: {progress}/{REQUIRED_WORDS}"
    else:
        good_phrase = f"{random.choice(GOOD)}\n{progress}/{REQUIRED_WORDS}"

    send(user_id, good_phrase)

    if progress >= REQUIRED_WORDS:
        finish_user(user_id)

        congratulations = (
            "🎉✨🎓 ПОЗДРАВЛЯЕМ! 🎓✨🎉\n\n"
            "Ты успешно прошёл викторину!\n"
            "Сохрани это сообщение и покажи его организатору\n"
        )

        send(user_id, congratulations, attachment=WIN_IMAGE)
