import smtplib
import os
import json
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run_automation():
    sender_email = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']

    history_file = 'history.json'
    history = json.load(open(history_file, 'r')) if os.path.exists(history_file) else []
    sent_emails = {entry['email'] for entry in history}

    with open('emails.txt', 'r', encoding='utf-8') as f:
        contacts = [line.strip().split(',') for line in f if line.strip()]

    with open('messages.txt', 'r', encoding='utf-8') as f:
        raw_content = f.read()
        all_templates = [m.strip() for m in raw_content.split('===') if m.strip()]

    to_send = [(n, e) for n, e in contacts if e not in sent_emails][:10]

    if not to_send:
        print("Koi naya email bhejney ke liye nahi hai!")
        return

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)

        for name, email in to_send:
            template = random.choice(all_templates)
            personalized_text = template.replace("(agent name)", name)
            
            lines = personalized_text.split('\n')
            subject_line = lines[0].replace("Subject: ", "").strip()
            body_text = "\n".join(lines[1:]).strip()

            msg = MIMEMultipart()
            msg['Subject'] = subject_line
            msg['From'] = f"Pushpendra <{sender_email}>"
            msg['To'] = email
            msg.attach(MIMEText(body_text, 'plain'))

            smtp.send_message(msg)

            history.append({
                "name": name,
                "email": email,
                "date": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
                "subject": subject_line,
                "status": "Sent"
            })
            print(f"Email sent to: {name}")

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    run_automation()
