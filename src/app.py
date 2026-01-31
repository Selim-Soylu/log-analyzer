from flask import Flask, render_template, request, jsonify, Response, send_file
import os
import json
import csv
import io
from parser import LogParser

app = Flask(__name__)

LOG_DIR = "/app/logs" if os.path.exists("/app/logs") else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_PATH, "..", "config", "rules.json")
parser = LogParser(RULES_PATH)

last_static_results = []

@app.route('/')
def index():
    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.log')]
    return render_template('index.html', files=log_files)

@app.route('/api/analyze', methods=['POST'])
def analyze_static():
    global last_static_results
    filename = request.json.get('filename')
    file_path = os.path.join(LOG_DIR, filename)
    
    results = parser.static_analysis(file_path)
    last_static_results = results
    return jsonify(results)

@app.route('/api/stream/<filename>')
def stream_log(filename):
    file_path = os.path.join(LOG_DIR, filename)
    return Response(parser.tail_file_generator(file_path), mimetype='text/event-stream')

@app.route('/api/download_csv')
def download_csv():
    global last_static_results
    if not last_static_results:
        return "İndirilecek veri yok. Önce statik analiz yapın.", 400

    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=["zaman", "kural", "seviye", "mesaj"])
    cw.writeheader()
    cw.writerows(last_static_results)
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8-sig'))
    output.seek(0)
    
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="log_raporu.csv")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)