from config import ADMIN_ID
from database import stats, get_all_users


def handle_admin(send, user_id, text):
    if user_id != ADMIN_ID:
        return False

    if text == "/stats":
        total, finished = stats()
        not_finished = total - finished

        send(user_id,
             f"📊 СТАТИСТИКА ВИКТОРИНЫ 📊\n\n"
             f"👥 Всего участников: {total}\n"
             f"🏆 Победителей: {finished}\n"
             f"🔄 В процессе: {not_finished}\n"
             f"📈 Процент побед: {round(finished / total * 100, 1) if total > 0 else 0}%")

        return True

    if text.startswith("/reset "):
        try:
            target_id = int(text.split()[1])
            from database import cursor, conn
            cursor.execute("DELETE FROM users WHERE user_id=?", (target_id,))
            conn.commit()
            send(user_id, f"✅ Прогресс пользователя {target_id} сброшен")
        except:
            send(user_id, "❌ Ошибка. Используйте: /reset 123456789")
        return True

    if text == "/winners":
        from database import cursor
        cursor.execute("SELECT user_id FROM users WHERE status='finished'")
        winners = cursor.fetchall()

        if winners:
            winner_list = "\n".join([f"• {w[0]}" for w in winners])
            send(user_id, f"🏆 Победители ({len(winners)}):\n\n{winner_list}")
        else:
            send(user_id, "Пока нет победителей")
        return True

    return False
