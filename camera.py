import os
import glob
import picamera
import smtplib
from time import sleep


from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

sender = 'eightsemester1519@gmail.com'
password = 'raspberrypi'
receiver = 'eightsemester1519@gmail.com'

DIR = './Database/'
FILE_PREFIX = 'image'

print 'Sending E-Mail'

if not os.path.exists(DIR):
    os.makedirs(DIR)


files = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
count = 0

if len(files) > 0:
    # Grab the count from the last filename.
    count = int(files[-1][-7:-4])+1

# Save image to file
filename = os.path.join(DIR, FILE_PREFIX + '%03d.jpg' % count)

with picamera.PiCamera() as camera:
    pic = camera.capture(filename)

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = 'Picture Requested'
body = 'Picture is Attached.'
msg.attach(MIMEText(body, 'plain'))
attachment = open(filename, 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
text = msg.as_string()
server.sendmail(sender, receiver, text)
server.quit()


