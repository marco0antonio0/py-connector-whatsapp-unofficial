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
    cd py-connector-whatsapp-unofficial
    ```

2. **Install Dependencies**:
    Ensure you have Python installed. Then install the required Python packages:

    ```bash
    pip install selenium webdriver-manager pillow
    ```

3. **Generate QR Code Module**:
    Create a `generateQRcode.py` file with a function `createQRCODE` to generate QR codes.

4. **Configure WebDriver**:
    Ensure you have the Chrome browser installed. The `webdriver-manager` package will handle the WebDriver installation.

## Usage

1. **Initialize the Bot**:

    ```python
    from bot import botWhatsapp
    # with interface = true
    #without interface = false // terminal acess
    bot = botWhatsapp(gui=False)
    ```

2. **Start the Bot**:

    ```python
    bot.start()
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

py-connector-whatsapp-unofficial/
│
├── bot.py # Main bot class and functionalities
├── generateQRcode.py # QR code generation module
├── requirements.txt # List of dependencies
├── README.md # Project documentation
└── dados/ # Directory to store session data

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
