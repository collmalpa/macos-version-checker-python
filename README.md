# macOS Version Checker and Notifier (Python version)

This Python script checks for the latest version of macOS on the official Apple support page and notifies users via Telegram if a new version is detected. It keeps track of the versions previously detected and sends an alert only when a new version is available. The script uses a configuration file to store Telegram bot settings and recipient information.

## Features

- **Automated macOS Version Check**: Fetches the current macOS version information from the official Apple support page.
- **Telegram Notifications**: Sends a Telegram message when a new macOS version is detected.
- **Version Tracking**: Maintains a record of the previously detected macOS versions to avoid redundant notifications.
- **Configurable Settings**: Uses a separate `config.ini` file for easy configuration of Telegram bot credentials and recipient information.

## Usage

### Clone the Repository:

```bash
git clone https://github.com/collmalpa/macos-version-checker-python.git
cd macos-version-checker-python
```

### Create and Edit `config.ini`:

Create a `config.ini` file with the following content:

```ini
[Telegram]
TOKEN = your_telegram_bot_token
chat_id = your_chat_id

[URLs]
macOS_info_url = https://support.apple.com/en-us/HT201222

[Files]
output_file = LatestMacOSVersion.txt

[macOSforSearch]
macOSforSearch = Sonoma 14
```

Fill in your Telegram bot credentials.

### Run the Script:

```bash
python3 macos_version_checker.py
```

### Schedule the Script with Cron:

It's recommended to add this script to cron to run at regular intervals. This ensures you are promptly notified when a new macOS version is available.

To add the script to cron:
1. Open the cron table for editing:
    ```bash
    crontab -e
    ```
2. Add a new cron job to run the script at your desired frequency (e.g., hourly):
    ```bash
    0 * * * * /usr/bin/python3 /path/to/your/macos_version_checker.py
    ```
3. Save and close the cron table.

## Docker Setup

You can also run this script in a Docker container with a scheduled cron job. Follow these steps to build and run the Docker container.

### Prerequisites

- Docker installed on your machine

### Building the Docker Image

1. Clone the repository:

    ```sh
    git clone https://github.com/collmalpa/macos-version-checker-python.git
    cd macos-version-checker-python
    ```

2. Build the Docker image:

    ```sh
    docker build -t macos-version-checker .
    ```

### Running the Docker Container

To run the Docker container, use the following command:

```sh
docker run -d --name macos-version-checker macos-version-checker
```

This command runs the container in detached mode. The script inside the container is scheduled to run every hour, as specified in the crontab file.

## Note

The method of sending notifications via Telegram is secure and efficient. For modern applications, Telegram provides a robust API that can be easily integrated with Python scripts for various notification purposes.

This script is an evolution of a previous one I wrote in PowerShell (https://github.com/collmalpa/macos-version-checker), which had certain limitations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
