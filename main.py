import yaml
import os
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from alerts.telegram_alert import TelegramAlert
from monitors.url_monitor import URLMonitor
from monitors.system_monitor import SystemMonitor

def load_config():
    load_dotenv()
    with open('config.yaml', 'r') as f:
        content = f.read()
    content = os.path.expandvars(content)
    config = yaml.safe_load(content)

    token = config['telegram']['token']
    chat_id = config['telegram']['chat_id']

    if not token or str(token).startswith('$'):
        raise ValueError("TELEGRAM_TOKEN not set in .env")
    if not chat_id or str(chat_id).startswith('$'):
        raise ValueError("TELEGRAM_CHAT_ID not set in .env")

    return config

def run_checks(url_monitor, system_monitor):
    print("\n--- Running checks ---")
    url_monitor.check()
    system_monitor.check()

def main():
    config = load_config()

    alert = TelegramAlert(
        str(config['telegram']['token']),
        str(config['telegram']['chat_id'])
    )

    url_monitor = URLMonitor(alert, config['urls'])
    system_monitor = SystemMonitor(alert, config['thresholds'])

    interval = config['schedule']['check_interval_minutes']

    alert.send("*InfraWatch Bot started*\nMonitoring active.")

    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_checks,
        'interval',
        minutes=interval,
        args=[url_monitor, system_monitor]
    )

    run_checks(url_monitor, system_monitor)
    scheduler.start()

if __name__ == "__main__":
    main()
