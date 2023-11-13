from datetime import datetime

now: str = lambda: datetime.now().strftime('%H:%M:%S')
