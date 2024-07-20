import requests
from bs4 import BeautifulSoup
import configparser
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path to the configuration file
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')

# Read the configuration file
config = configparser.ConfigParser()

if not os.path.exists(config_path):
    logging.error("Config file not found.")
    exit(1)

config.read(config_path)

# Check for the presence of required sections and keys in the configuration file
required_sections = ['Telegram', 'URLs', 'Files', 'macOSforSearch']
required_keys = {
    'Telegram': ['TOKEN', 'chat_id'],
    'URLs': ['macOS_info_url'],
    'Files': ['output_file'],
    'macOSforSearch': ['macOSforSearch']
}

for section in required_sections:
    if section not in config:
        logging.error(f"Missing section in config file: {section}")
        exit(1)
    for key in required_keys[section]:
        if key not in config[section]:
            logging.error(f"Missing key in section {section}: {key}")
            exit(1)

# Extract configuration values
TOKEN = config['Telegram']['TOKEN']
chat_id = config['Telegram']['chat_id']
url = config['URLs']['macOS_info_url']
output_file = config['Files']['output_file']
macOSforSearch = config['macOSforSearch']['macOSforSearch']

# Read the last macOS version stored in a file
def read_last_macOS_version(file_path):
    if not os.path.exists(file_path):
        return ''
    try:
        with open(file_path, 'r') as file:
            return ''.join(file.read().split())
    except FileNotFoundError:
        return ''

# Write the latest macOS version to a file
def write_latest_macOS_version(file_path, latest_macOS):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(latest_macOS + '\n')

# Fetch the macOS information from the specified URL
def fetch_macOS_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching macOS info: {e}")
        return ''

# Parse the macOS information from the HTML content
def parse_macOS_info(html, macOSforSearch):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows:
        if macOSforSearch in row.text:
            return row.text
    return ''

# Send a message via Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Sent message via Telegram")
    except requests.RequestException as e:
        logging.error(f"Error sending message via Telegram: {e}")

def get_updates(token):
    """Получение обновлений от Telegram для получения новых chat ID"""
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching updates from Telegram: {e}")
        return None

def update_chat_ids(token, config_path):
    """Обновление chat_id в config.ini с новыми chat ID"""
    updates = get_updates(token)
    if not updates or not updates.get('result'):
        return

    chat_ids = set(config['Telegram']['chat_id'].split(','))
    for update in updates['result']:
        if 'message' in update:
            chat_id = str(update['message']['chat']['id'])
            if chat_id not in chat_ids:
                chat_ids.add(chat_id)
                logging.info(f"Found new chat ID: {chat_id}")

    # Обновляем конфигурационный файл
    config['Telegram']['chat_id'] = ','.join(chat_ids)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
     
# Main function to check for the latest macOS version and send a notification if a new version is detected
def main():
     # Обновляем chat ID в config.ini
    update_chat_ids(TOKEN, config_path)
    last_macOS_version = read_last_macOS_version(output_file)
    
    html = fetch_macOS_info(url)
    if not html:
        return

    latest_macOS = parse_macOS_info(html, macOSforSearch)
    clearlatest_macOS = ''.join(latest_macOS.split())

    if last_macOS_version != clearlatest_macOS:
        lines = latest_macOS.splitlines()
        if lines:
            latest_macOS_ver = lines[0]
            date_release = lines[2] if len(lines) > 2 else "Unknown"
            message = (
                f"Hi!\n"
                f"New macOS is available for download.\n"
                f"Date of release:\n"
                f"{date_release}\n"
                f"{'-' * 56}\n"
                f"Latest available version of macOS:\n"
                f"{latest_macOS_ver}\n"
                f"{'-' * 56}\n"
                f"More information is available on the page:\n"
                f"https://support.apple.com/en-us/HT201222\n"
            )
            chat_ids = config['Telegram']['chat_id'].split(',')
            for chat_id in chat_ids:
                send_telegram_message(TOKEN, chat_id, message)
            write_latest_macOS_version(output_file, latest_macOS)
        else:
            logging.error("Failed to parse latest macOS version")


if __name__ == "__main__":
    main()
