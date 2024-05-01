# Whatsapp-Bulk-Messenger

Whatsapp Bulk Messenger automates sending of messages via Whatsapp Web. The tool can you used to send whatsapp message in bulk. Program uses runs through a list of numbers provided in numbers.txt and then tries to send a prediefined (but templated) message to each number in the list. It can also read other columns from the number csv to populate template specific words and then send out a personalized message to the number

Note: The current program is limited to sending only TEXT message

Note: Another version of similar project will be available which supports sending media and documents along with text. Please reach out to me on [email](mailto:khnaz35@gmail.com) for more enquiry.

# Requirements

*  Python >= 3.11.0
*  Chrome canary headless is installed by the program automatically

# Setup

1. Install python - >=v3.6
2. Run `pip install -r requirements.txt`

# Steps

1. Enter the message you want to send inside `contacts.csv` file.
2. Run `python auto.py`.
3. Once the program starts, it will log the info in whatsapp_messenger.log you'll see the new log file created when you run this tool.
4. After a while, Chrome canary should pop-up and open web.whatsapp.com.
5. Scan the QR code to login into whatsapp.
6. Press `Enter` to start sending out messages.
7. Sit back and relax!

### Funding

If you like this tool, I'd appreciate it if you could make a donation via [Buy Me a Coffee](https://buymeacoffee.com/khnaz35).