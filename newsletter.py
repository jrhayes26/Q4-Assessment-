# newsletter.py

import openai
import smtplib
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# === Step 1: Generate Book News with OpenAI ===
def generate_book_news():
    prompt = (
        "Pretend you're a literary news journalist. Generate 3 headlines and summaries "
        "about new or upcoming fiction book releases in April 2025. Each should include a title "
        "and a 2-3 sentence summary suitable for an email newsletter."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a literary news reporter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error fetching news from OpenAI: {e}]"

# === Step 2: Format Email Content ===
def format_email(news_content):
    subject = "📚 Your Daily Book News Digest"
    body = f"Subject: {subject}\n\n{news_content}"
    return body

# === Step 3: Send Email via SMTP ===
def send_email(body):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, body)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# === Main Program ===
def run_newsletter():
    news = generate_book_news()
    email_body = format_email(news)
    send_email(email_body)

if __name__ == "__main__":
    run_newsletter()
