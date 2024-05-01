# Whatsapp Bulk Messenger

Whatsapp Bulk Messenger is a tool designed to automate the sending of messages through Whatsapp Web. It enables the bulk sending of templated messages, which can be personalized using data from a CSV file. Each message is tailored using specific information associated with a contact number, enhancing the personal touch of your communications.

## Features

- **Bulk Messaging:** Send messages to multiple recipients automatically.
- **Message Personalization:** Utilize additional CSV data to personalize messages for each contact.
- **Text-Only Support:** Currently, the tool supports sending text messages only.

> **Note:** A future version will support media and document attachments. For more details, contact me at [khnaz35@gmail.com](mailto:khnaz35@gmail.com).

## Requirements

- Python 3.11.0 or newer
- Chrome Canary (The tool installs this automatically in headless mode)

## Setup

1. Ensure Python version 3.6 or higher is installed.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Populate the `contacts.csv` file with the message details and contact numbers.
2. Execute the script:
   ```bash
   python auto.py
   ```
3. Follow on-screen instructions to log into Whatsapp Web using a QR code.
4. Press `Enter` to initiate message sending.
5. Monitor the progress in `whatsapp_messenger.log`.

### Logging

Logs are maintained in `whatsapp_messenger.log`, tracking both routine operations and errors. The log files rotate after reaching 10 MB to save space and avoid overloading.

## Support

If you find this tool helpful and would like to support its development, consider making a donation through [Buy Me a Coffee](https://buymeacoffee.com/khnaz35).
