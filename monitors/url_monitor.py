import requests
import time

class URLMonitor:
    def __init__(self, alert, urls_config):
        self.alert = alert
        self.urls = urls_config
        self.consecutive_failures = {}  # track failures per URL

    def check(self):
        for site in self.urls:
            name = site['name']
            url = site['url']
            threshold = site['response_time_threshold_ms']

            try:
                start = time.time()
                response = requests.get(url, timeout=10)
                response_time_ms = (time.time() - start) * 1000

                if response.status_code >= 400:
                    self._fire_alert(name, url, 
                        f"returned HTTP {response.status_code}", 
                        response_time_ms)
                elif response_time_ms > threshold:
                    self._fire_alert(name, url,
                        f"slow response ({response_time_ms:.0f}ms > {threshold}ms)",
                        response_time_ms)
                else:
                    # reset failure count on success
                    self.consecutive_failures[name] = 0
                    print(f"{name} — OK ({response_time_ms:.0f}ms)")

            except requests.exceptions.ConnectionError:
                self._fire_alert(name, url, "connection refused / unreachable", 0)
            except requests.exceptions.Timeout:
                self._fire_alert(name, url, "timed out after 10s", 0)

    def _fire_alert(self, name, url, reason, response_time_ms):
        self.consecutive_failures[name] = \
            self.consecutive_failures.get(name, 0) + 1
        
        count = self.consecutive_failures[name]
        message = (
            f"*ALERT: {name}*\n"
            f"URL: `{url}`\n"
            f"Reason: {reason}\n"
            f"Consecutive failures: {count}"
        )
        self.alert.send(message)
