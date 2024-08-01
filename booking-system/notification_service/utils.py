import smtplib
import logging
from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT
from email.message import EmailMessage



def get_email_template_dashboard(username, email, booking):
    email_message = EmailMessage()
    email_message['Subject'] = 'Подтверждение Бронирования Номера'
    email_message['From'] = SMTP_USER
    email_message['TO'] = email

    email_message.set_content(
        f'''
        <div>
            <h1 style="color: blue;">Здравствуйте, {username},</h1>
            <p>Ваше бронирование подтверждено! Вот детали вашего бронирования:</p>
            <ul>
                <li><strong>Номер:</strong> {booking['room_id']}</li>
                <li><strong>Дата заезда:</strong> {booking['check_in_date']}</li>
                <li><strong>Дата выезда:</strong> {booking['check_out_date']}</li>
            </ul>
            <p>Спасибо, что выбрали нас!</p>
            <img src="https://example.com/hotel-room.jpg" width="600" alt="Фото номера">
        </div>
        ''',
        subtype='html'
    )
    return email_message


def send_email(username, email, booking):
    # Логика отправки письма
    email_message = get_email_template_dashboard(username, email, booking)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email_message)
    logging.info(f"Sending email to {email}")

