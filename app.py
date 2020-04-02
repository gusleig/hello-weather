import smtplib
import email
import email.mime.application
from xml.dom import minidom
import os
import sys
import time
from email.mime.multipart import MIMEMultipart
import pyowm


cfgFile = os.path.realpath('./config.xml')

smtp = ''
fromaddr = ''
toaddr = ''
ccaddr = ''
server = ''
port = ''
useSSL = ''
username = ''
passwd = ''
city = ''
apikey = ''


def getNodeText(node):
    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)

    return ''.join(result)


def get_config(cfg):
    global smtp, fromaddr, toaddr, ccaddr, server, port, useSSL, username, passwd, apikey, city

    doc = minidom.parse(cfg)
    root = doc.getElementsByTagName("config")[0]

    apikey = getNodeText(root.getElementsByTagName("apikey")[0])
    city = getNodeText(root.getElementsByTagName("city")[0])

    smtp = root.getElementsByTagName("smtp")[0]

    fromaddr = getNodeText(smtp.getElementsByTagName("from")[0])
    toaddr = getNodeText(smtp.getElementsByTagName("to")[0])
    ccaddr = getNodeText(smtp.getElementsByTagName("cc")[0])

    server = getNodeText(smtp.getElementsByTagName("server")[0])
    port = getNodeText(smtp.getElementsByTagName("port")[0])
    useSSL = getNodeText(smtp.getElementsByTagName("ssl")[0])
    username = getNodeText(smtp.getElementsByTagName("user")[0])
    passwd = getNodeText(smtp.getElementsByTagName("password")[0])


def send_mail(date, body, subject, smtp, fromaddr, toaddr, ccaddr, server, port, useSSL, username, passwd):

    msg = MIMEMultipart()

    msg['Subject'] = date + " - " + subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Cc'] = ccaddr

    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    if len(server) == 0 or len(port) == 0:
        return

    rcpt = ccaddr.split(",") + [toaddr]

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (fromaddr, ", ".join(rcpt), subject + " : " + date, body)

    email_text = "\r\n".join([
        "From: " + fromaddr,
        "To: " + ", ".join(rcpt),
        "Subject: " + date + " - " + subject,
        "",
        body
    ])

    try:
        with smtplib.SMTP(server, port) as s:
            s.ehlo()

            if useSSL.lower() == 'true':
                s.starttls()
            else:
                s.ehlo()
            s.login(fromaddr, passwd)
            s.sendmail(fromaddr, rcpt, email_text)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


def get_weather(apikey, location='Rio de Janeiro, BR'):

    owm = pyowm.OWM(apikey)
    # observation = owm.weather_at_id(cityid)
    w = owm.weather_at_place(location)
    weather = w.get_weather()
    wind = weather.get_wind()
    temp = weather.get_temperature('celsius')
    humidity = weather.get_humidity()

    report = """
    Report for: %s \n
    Temperature: %s \n
    Winds: %s \n
    Humidity: %s
    """

    report = report % (location, temp, wind, humidity)
    return report


if __name__ == "__main__":

    currentdate = time.strftime("%Y-%m-%d %H:%M:%S")

    get_config(cfgFile)

    body = get_weather(apikey, city)

    subject = "Weather report for: " + city

    send_mail(currentdate, body, subject, smtp, fromaddr, toaddr, ccaddr, server, port, useSSL, username, passwd)

    print("Email sent")