from time import sleep
import os
import httpx
import schedule
from utils.email import Email

SOURCE = "http://www.koeri.boun.edu.tr/scripts/lst5.asp"
PLACE = os.getenv("PLACE")
THRESHOLD = int(os.getenv("THRESHOLD"))
MIN_ML = float(os.getenv("ML"))
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO").split(",")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")
email = Email(EMAIL_FROM, EMAIL_TO)

print(f"SOURCE={SOURCE}")
print(f"PLACE={PLACE}")
print(f"THRESHOLD={THRESHOLD}")
print(f"EMAIL_FROM={EMAIL_FROM}")
print(f"EMAIL_TO={EMAIL_TO}")
print(f"EMAIL_SUBJECT={EMAIL_SUBJECT}")


def schedule_actions():
    schedule.every().minutes.do(earthquake_follower)
    while True:
        schedule.run_pending()
        sleep(1)


def earthquake_follower():
    earthquakes = httpx.get(SOURCE)
    related_earthquakes = []

    for line in earthquakes.text.splitlines():
        if line.find(PLACE) > -1:

            ml = float(line.split()[6])

            if ml >= MIN_ML:
                related_earthquakes.append(line)

    if len(related_earthquakes) >= THRESHOLD:
        html_build = """
            <h3>{}</h3>
            <h4>Earthquakes:</h4>
            <u>Tarih</u> | <u>Saat</u> | <u>Enlem(N)</u> | <u>Boylam(E)</u> | <u>Derinlik(km)</u> | <u>MD</u> | <u>ML</u> | <u>Mw</u> | <u>Yer</u> | <u>Çözüm Niteliği</u>
            <hr/>
            {}
        """
        body = html_build.format(EMAIL_SUBJECT, '<br>'.join(related_earthquakes))
        email.send_mail(EMAIL_SUBJECT, body, True)


if __name__ == "__main__":
    schedule_actions()
    # earthquake_follower() # for testing the function
