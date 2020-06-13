import smtplib, ssl


def sendEmail(message):
  port = 465  # For SSL
  password = "buenbitmailsender"

  sender_email = "diffbuenbitmailsender@gmail.com"
  receiver_email = "vallejojuanp@gmail.com"

  # Create a secure SSL context
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login("diffbuenbitmailsender@gmail.com", password)
      server.sendmail(sender_email, receiver_email, message)