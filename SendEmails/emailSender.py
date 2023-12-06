import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

sender_email = "stu218517"
password = "CAUK-3260"
votingForm = "https://docs.google.com/forms/d/e/1FAIpQLSdpv3q2KWIqV9WmjxfM0ikt7HNqRDXlaiKGxB01BW1EiRj_6Q/viewform"

users = [line.strip() for line in open("emailList.txt", 'r')]
list_onetime_links = [line.strip() for line in open("../onetimeLinkGenerator/generated_links.txt", 'r')]
nameList = [line.strip() for line in open("nameList.txt", 'r')]

with open('instruction_email_template.html', 'r', encoding="utf8") as template:
    instruction_email_template = template.read().replace('\n', '')
    instruction_email_template = instruction_email_template.replace('\t', '')

print(list_onetime_links)


server_log = open("server_log.txt", "w")

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtps.mail.uni-kiel.de", 465, context=context) as server:
    server.login(sender_email, password)

    print("TheKing--> total Users: ", len(users))
    server_log.write("Total users: " + str(len(users)) + "\n")
    for i in range(0, len(users)):
        print("TheKing--> email: ", users[i])
        print("TheKing--> name: ", nameList[i])
        print("TheKing--> link: ", list_onetime_links[i])
        server_log.write("\n\nProcessing user #" + str(i) + "\n")
        server_log.write("email: " +  users[i] + "\n")
        server_log.write("name: " + nameList[i] + "\n")
        server_log.write("link: " + list_onetime_links[i] + "\n")

        message = MIMEMultipart("alternative")
        message["Subject"] = "BSAAK President Election 2023/24"
        message["From"] = sender_email
        message["To"] = users[i]

        formatedHtml = instruction_email_template
        formatedHtml = formatedHtml.replace("__custom_name", nameList[i])
        formatedHtml = formatedHtml.replace("__custom_token", list_onetime_links[i])
        formatedHtml = formatedHtml.replace("__custom_link", votingForm)

        # print("TheKing--> instruction_email_template: ", formatedHtml)

        # Turn these into plain/html MIMEText objects
        part = MIMEText(formatedHtml, "html")


        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part)
        try:
            ret = server.sendmail(sender_email, users[i], message.as_string())
            print('TheKing--> Email is sent to  = ', users[i])
            server_log.write("Email sent SUCCESS to: " + users[i] + "\n")
        except Exception as e:
            print("TheKing--> sending failed with error: ", e)
            server_log.write("Email sent FAILED!!!! while sending to: " + users[i] + "\n")


        del message
        time.sleep(5)

    print("TheKing--> Script finished processing all tasks")
    server_log.write("\n\nScript finished processing all tasks\n")
    server_log.close()