import json
import time
import os

class LogParser:
    def __init__(self, rules_path):
        with open(rules_path, 'r', encoding='utf-8-sig') as f:
            self.rules = json.load(f)['rules']

    def check_line(self, line):
        for rule in self.rules:
            if rule['pattern'].lower() in line.lower():
                return {
                    "zaman": "Anlik",
                    "kural": rule['name'],
                    "seviye": rule['severity'],
                    "mesaj": line.strip()
                }
        return None

    def static_analysis(self, file_path):
        found_events = []
        if not os.path.exists(file_path):
            return found_events
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                res = self.check_line(line)
                if res:
                    found_events.append(res)
        return found_events

    def tail_file_generator(self, file_path):
        if not os.path.exists(file_path):
             yield f"data: Hata: {file_path} bulunamadi!\n\n"
             return

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            f.seek(0, 2)
            yield f"data: --- Canli Takip Basladi: {os.path.basename(file_path)} ---\n\n"
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                res = self.check_line(line)
                if res:
                    json_data = json.dumps(res)
                    yield f"data: {json_data}\n\n"