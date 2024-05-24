import smtplib
from email.message import EmailMessage
from json import loads
sender = "techspecsmaster@gmail.com"
password = "uzsh xuya rykg bbiz"

def sendMessage(reciever,msg):

    em = EmailMessage()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    print(sender,password,reciever,msg)
    s.login(sender, password)
    em["To"] = reciever
    message = f"""
    Dear User,
    {msg}
    """
    em["From"] = sender
    em["Subject"] = "Message Recieved"
    em.set_content(message)
    print("here")
    err =s.send_message(em, sender, reciever)
    print(err)
    s.quit()

