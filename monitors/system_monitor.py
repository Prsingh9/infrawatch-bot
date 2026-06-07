import psutil

class SystemMonitor:
    def __init__(self, alert, thresholds):
        self.alert = alert
        self.thresholds = thresholds

    def check(self):
        self._check_cpu()
        self._check_memory()
        self._check_disk()

    def _check_cpu(self):
        cpu = psutil.cpu_percent(interval=1)
        threshold = self.thresholds['cpu_percent']
        if cpu > threshold:
            self.alert.send(
                f" *HIGH CPU ALERT*\n"
                f"Current: `{cpu}%`\n"
                f"Threshold: `{threshold}%`"
            )
        else:
            print(f" CPU — {cpu}%")

    def _check_memory(self):
        mem = psutil.virtual_memory()
        threshold = self.thresholds['memory_percent']
        if mem.percent > threshold:
            self.alert.send(
                f"*HIGH MEMORY ALERT*\n"
                f"Current: `{mem.percent}%` "
                f"({mem.used // 1024**3}GB / {mem.total // 1024**3}GB)\n"
                f"Threshold: `{threshold}%`"
            )
        else:
            print(f" Memory — {mem.percent}%")

    def _check_disk(self):
        disk = psutil.disk_usage('/')
        threshold = self.thresholds['disk_percent']
        if disk.percent > threshold:
            self.alert.send(
                f" *HIGH DISK ALERT*\n"
                f"Current: `{disk.percent}%` "
                f"({disk.used // 1024**3}GB / {disk.total // 1024**3}GB)\n"
                f"Threshold: `{threshold}%`"
            )
        else:
            print(f"Disk — {disk.percent}%")
