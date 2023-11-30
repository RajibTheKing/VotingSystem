import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

sender_email = "stu218517"
password = "CAUK-3260"

users = [line.strip() for line in open("emailList.txt", 'r')]
list_onetime_links = [line.strip() for line in open("../onetimeLinkGenerator/generated_links.txt", 'r')]
nameList = [line.strip() for line in open("nameList.txt", 'r')]

with open('instruction_email_template.html', 'r', encoding="utf8") as template:
    instruction_email_template = template.read().replace('\n', '')
    instruction_email_template = instruction_email_template.replace('\t', '')

print("TheKing--> instruction_email_template: ", instruction_email_template);

print(list_onetime_links)



# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtps.mail.uni-kiel.de", 465, context=context) as server:
    server.login(sender_email, password)

    print("TheKing--> total Users: ", len(users))
    for i in range(0, len(users)):
        print("TheKing--> Trying to send email: ", users[i])
        message = MIMEMultipart("alternative")
        message["Subject"] = "(BSAK Election 2023) Instructions, Link for token and voting form."
        message["From"] = sender_email
        message["To"] = users[i]

        html = instruction_email_template

        formatedHtml = html.format(name = nameList[i],
                                   token = list_onetime_links[i], 
                                   form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdpv3q2KWIqV9WmjxfM0ikt7HNqRDXlaiKGxB01BW1EiRj_6Q/viewform")

        # Turn these into plain/html MIMEText objects
        part = MIMEText(formatedHtml, "html")


        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part)

        ret = server.sendmail(sender_email, users[i], message.as_string())
        print('TheKing--> Email is sent to  = ', users[i])
        del message
        time.sleep(5)
