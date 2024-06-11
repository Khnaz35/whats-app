# Whatsapp Bulk Messenger

Whatsapp Bulk Messenger is a tool designed to automate the sending of messages through Whatsapp Web. It enables the bulk sending of templated messages, which can be personalized using data from a CSV file. Each message is tailored using specific information associated with a contact number, enhancing the personal touch of your communications.

## Features

- **Bulk Messaging:** Send messages to multiple recipients automatically.
- **Message Personalization:** Utilize additional CSV data to personalize messages for each contact.
- **Media Attachments:** Send images and videos along with text messages.
- **Error Handling and Logging:** Comprehensive logging and error handling to ensure smooth operation.

> **Note:** Future versions may include support for additional media types and documents. For more details, contact me at [khnaz35@gmail.com](mailto:khnaz35@gmail.com).

## Requirements

- Python 3.11.0 or newer
- Chrome Canary (The tool installs this automatically in headless mode)
- If you need to download the driver manually, it can be downloaded from here: [Chrome-drivers](https://sites.google.com/chromium.org/driver/)

## Setup

1. Ensure Python version 3.11.0 or higher is installed.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Populate the `contacts.csv` file with the message details, contact numbers, and paths to media attachments (if any).

   Example CSV structure:
   ```csv
   FirstName,LastName,Phone,Message,AttachmentPath
   Ali,Ahmed,1121121787,"Dear {%S first name last name}, take note that your class will start today at 7:45pm via online https://google-meet.com","/path/to/your/attachment.jpg"
   ```

2. Execute the script:
   ```bash
   python auto.py
   ```

3. Follow on-screen instructions to log into Whatsapp Web using a QR code.
4. Press `Enter` to initiate message sending.
5. Monitor the progress in `whatsapp_messenger.log`.

### Logging

Logs are maintained in `whatsapp_messenger.log`, tracking both routine operations and errors. The log files rotate after reaching 10 MB to save space and avoid overloading.

### Configuration

Settings for the tool are managed through the `environment.yml` file, which includes parameters such as log file location, delay settings, retry attempts, and paths to necessary resources.

### Example `environment.yml`

```yaml
chrome_binary_location: "/path/to/Google Chrome Canary"
user_data_dir: "/path/to/your/chrome/user/data"
contacts_file: "contacts.csv"
log_file: "whatsapp_messenger.log"
max_log_size: 10485760  # 10MB
log_backup_count: 5
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
delay: 10
retry_attempts: 3
min_sleep_time: 2
max_sleep_time: 5
```

## Disclaimer

This tool is intended for educational and personal use only. The developer is not responsible for any misuse of this tool, including but not limited to spamming, harassment, or any violations of WhatsApp's terms of service. Use this tool responsibly and ensure you have permission to contact each recipient.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you find this tool helpful and would like to support its development, consider making a donation through [Buy Me a Coffee](https://buymeacoffee.com/khnaz35).

### LICENSE

The source code is licensed under the MIT license, which you can find in the MIT-LICENSE.txt file.