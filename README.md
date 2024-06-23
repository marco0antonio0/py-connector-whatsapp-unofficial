# WhatsApp Automation Bot

This project is a WhatsApp automation bot developed using Selenium WebDriver. The bot provides various functionalities such as logging in, sending messages, sending media, and checking for new messages on WhatsApp Web.

## Features

- **Login Automation**: Automatically logs into WhatsApp Web and persists session data.
- **Message Sending**: Send text messages and media (images/videos) to specific contacts.
- **Chat Management**: Open chats by contact name and navigate through chats.
- **QR Code Generation**: Generates QR codes for WhatsApp Web login.
- **Message Retrieval**: Retrieve the last message from a chat.
- **New Message Notifications**: Check for new messages and handle notifications.

## Installation

To use this bot, follow these steps:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/marco0antonio0/py-connector-whatsapp-unofficial
    ```

    ```bash
    cd py-connector-whatsapp-unofficial
    ```

2. **Install Dependencies**:
    Ensure you have Python installed. Then install the required Python packages:

    ```bash
    pip install selenium webdriver-manager pillow
    ```

3. **Start the code of the path main:**
    for the start python script, so execute :

    ```bash
    python3 main.py
    ```

4. **Now to necessary login:**
    The login is necessary for the use script where is execute in localhost when the your machine
    Now check if the bash console is if the show you an qrcode message

5. **Now this code is Already complete start:**
    The started progamme is sucessfull

## How to usage the functionalidades of checking message and obtain last message of the contact

- The guide thating is the main.py file

## How to usage functionalidade

1. **Initialize the Bot**:

    ```python
    from services import automation
    # with interface = true
    #without interface = false // terminal acess
    bot = automation(gui=False)
    ```

2. **Start the Bot**:

    ```python
    # if gui= true so the show with interface
    # else so the without interface
    bot.start(gui=false)
    ```

3. **Send a Message**:

    ```python
    bot.openChatByContact("Contact Name")
    bot.sendMensage("Hello, this is a test message!")
    ```

4. **Send an Image with Text**:

    ```python
    bot.sendImageWithText("path/to/image.jpg", "Here is an image with a caption!")
    ```

5. **Check for New Messages**:

    ```python
    new_message = bot.VerificarNovaMensagem()
    if new_message:
        print("New message from:", new_message)
    ```

6. **Retrieve Last Message**:

    ```python
    last_message = bot.pegar_ultima_mensagem()
    print("Last message:", last_message)
    ```

7. **Exit the Bot**:

    ```python
    bot.exit()
    ```

## Project Structure

```yaml
py-connector-whatsapp-unofficial/
│
├──main.py
├── requirements.txt # List of dependencies
├── README.md        # Project documentation
├── dados/           # Directory to store session data
└──servies/
        ├── bot.py            # Main bot class and functionalities
        └── generateQRcode.py # QR code generation module
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Selenium](https://www.selenium.dev/) - WebDriver for browser automation.
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) - For managing WebDriver binaries.
- [Pillow](https://python-pillow.org/) - Python Imaging Library for handling images.

## Contact

For any questions or suggestions, feel free to open an issue or contact me at [marcomesquitajr@hotmail.com](mailto:marcomesquitajr@hotmail.com).
