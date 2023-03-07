import os
import boto3
from botocore.exceptions import ClientError

# aws ses config
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


class Email:

    def __init__(self, sender, recipients=[]):
        self.client = boto3.client('ses',
                                   region_name=AWS_REGION,
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                                   )
        self.sender = sender
        self.recipients = recipients

    def __body(self, body, is_html):
        content = ""
        if is_html:
            content = {
                'Html': {
                    'Charset': "UTF-8",
                    'Data': body,
                }
            }
        else:
            content = {'Text': {
                'Charset': "UTF-8",
                'Data': body,
            }}
        return content

    def send_mail(self, subject, body, is_html=False):
        body_json_content = self.__body(body, is_html)
        try:
            response = self.client.send_email(
                Source=self.sender,
                Destination={
                    'ToAddresses': self.recipients,
                },
                Message={
                    'Body': body_json_content,
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    }
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])