from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'cyber_forensics_secret_key'

# HTML Template with Mobile-First Responsive Design & Passcode Lock
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Forensics: The Last Lecture</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #111827;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-blue: #3b82f6;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: #1f2937;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .mobile-container { width: 100%; max-width: 480px; height: 100vh; max-height: 850px; background: var(--card-bg); border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); display: flex; flex-direction: column; overflow: hidden; border: 1px solid var(--border-color); }
        @media(min-width: 500px) { .mobile-container { height: 90vh; } }
        
        .header { background: #1f2937; padding: 16px; text-align: center; border-bottom: 1px solid var(--border-color); }
        .header h1 { font-size: 1.1rem; color: var(--accent-green); letter-spacing: 1px; }
        .header p { font-size: 0.8rem; color: var(--text-muted); }

        .content { flex: 1; overflow-y: auto; padding: 16px; }
        
        /* Lock Screen Styles */
        .lock-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; }
        .pin-display { font-size: 2rem; letter-spacing: 8px; margin-bottom: 20px; background: #0b0f19; padding: 10px 20px; border-radius: 8px; border: 1px solid var(--border-color); width: 200px; }
        .keypad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; width: 240px; }
        .key { background: #1f2937; border: none; color: white; font-size: 1.2rem; padding: 16px; border-radius: 12px; cursor: pointer; transition: 0.2s; }
        .key:active { background: var(--accent-blue); }
        .error-msg { color: var(--accent-red); margin-top: 12px; font-size: 0.85rem; }

        /* Tool Cards */
        .tool-card { background: #1f2937; border-radius: 12px; padding: 14px; margin-bottom: 12px; border-left: 4px solid var(--accent-blue); }
        .tool-card.green { border-left-color: var(--accent-green); }
        .tool-card.red { border-left-color: var(--accent-red); }
        .tool-title { font-size: 0.95rem; font-weight: bold; margin-bottom: 6px; }
        .tool-desc { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 10px; }
        
        .btn { background: var(--accent-blue); color: white; border: none; padding: 8px 14px; border-radius: 6px; font-size: 0.85rem; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-green { background: var(--accent-green); color: #000; font-weight: bold; }
        
        /* Bottom Nav */
        .nav-bar { display: flex; background: #1f2937; border-top: 1px solid var(--border-color); padding: 10px; justify-content: space-around; }
        .nav-item { color: var(--text-muted); text-decoration: none; font-size: 0.75rem; text-align: center; flex: 1; }
        .nav-item.active { color: var(--accent-green); font-weight: bold; }

        .terminal-box { background: #000; color: #10b981; font-family: monospace; padding: 10px; border-radius: 6px; font-size: 0.78rem; margin-top: 8px; line-height: 1.4; }
    </style>
</head>
<body>
    <div class="mobile-container">
        {% if not session.get('authenticated') %}
        <!-- LOCK SCREEN -->
        <div class="header">
            <h1>RESTRICTED LAB TERMINAL</h1>
            <p>Enter Brother's Birthday Passcode</p>
        </div>
        <div class="content">
            <div class="lock-screen">
                <div class="pin-display">{{ pin_display }}</div>
                <form method="POST" action="/pin">
                    <input type="hidden" name="pin" value="{{ current_pin }}">
                    <div class="keypad">
                        <button type="submit" name="digit" value="1" class="key">1</button>
                        <button type="submit" name="digit" value="2" class="key">2</button>
                        <button type="submit" name="digit" value="3" class="key">3</button>
                        <button type="submit" name="digit" value="4" class="key">4</button>
                        <button type="submit" name="digit" value="5" class="key">5</button>
                        <button type="submit" name="digit" value="6" class="key">6</button>
                        <button type="submit" name="digit" value="7" class="key">7</button>
                        <button type="submit" name="digit" value="8" class="key">8</button>
                        <button type="submit" name="digit" value="9" class="key">9</button>
                        <button type="submit" name="digit" value="C" class="key" style="background:#374151;">C</button>
                        <button type="submit" name="digit" value="0" class="key">0</button>
                        <button type="submit" name="digit" value="OK" class="key btn-green">OK</button>
                    </div>
                </form>
                {% if error %}
                <div class="error-msg">{{ error }}</div>
                {% endif %}
                <p style="font-size:0.7rem; color: var(--text-muted); margin-top: 15px;">Hint: Brother's Birthday (4 digits)</p>
            </div>
        </div>
        {% else %}
        <!-- DASHBOARD & TOOLS -->
        <div class="header">
            <h1>CASE: THE LAST LECTURE</h1>
            <p>5-Player Digital Forensics Investigation</p>
        </div>
        
        <div class="content">
            {% if tab == 'tools' %}
                <h3 style="font-size: 0.9rem; margin-bottom: 10px; color: var(--accent-green);">Select Your Investigator Role:</h3>
                
                <div class="tool-card">
                    <div class="tool-title">🌐 Player 1: Network Stream Viewer</div>
                    <div class="tool-desc">Inspect PCAP traffic logs for unauthorized MQTT commands sent to smart HVAC & doors.</div>
                    <a href="/tool/net" class="btn">Open Tool</a>
                </div>

                <div class="tool-card red">
                    <div class="tool-title">💻 Player 2: TaskTrace Monitor</div>
                    <div class="tool-desc">Analyze RAM process list for hidden keyloggers and malicious background scripts.</div>
                    <a href="/tool/mem" class="btn">Open Tool</a>
                </div>

                <div class="tool-card">
                    <div class="tool-title">🗂️ Player 3: DataSift Carver</div>
                    <div class="tool-desc">Recover shredded chat log fragments and hidden directories from victim's disk.</div>
                    <a href="/tool/disk" class="btn">Open Tool</a>
                </div>

                <div class="tool-card green">
                    <div class="tool-title">⚡ Player 4: SmartLab Timeline</div>
                    <div class="tool-desc">Scrub sensor logs and smart chair telemetry during the hour of the incident.</div>
                    <a href="/tool/iot" class="btn">Open Tool</a>
                </div>

            {% elif tab == 'net' %}
                <a href="/" class="btn" style="margin-bottom:10px;">← Back to Tools</a>
                <div class="tool-title">Network Packet Capture</div>
                <div class="terminal-box">
                    [11:40:12] TCP 192.168.1.50 -> 10.0.0.4 [SYN]<br>
                    [11:42:01] MQTT: /smartlab/lock/override (MALICIOUS)<br>
                    [11:42:05] Door sensor status: JAMMED
                </div>
                <p style="font-size:0.8rem; margin-top:10px; color:var(--text-muted);">Finding: An external IP bypassed firewall rules via port 8883.</p>

            {% elif tab == 'mem' %}
                <a href="/" class="btn" style="margin-bottom:10px;">← Back to Tools</a>
                <div class="tool-title">RAM Process Analysis</div>
                <div class="terminal-box" style="color:#ef4444;">
                    PID 402: explorer.exe<br>
                    PID 884: python3 override_sys.py [ACTIVE]<br>
                    PID 1120: keylogger_hook.bin [HIDDEN]
                </div>
                <p style="font-size:0.8rem; margin-top:10px; color:var(--text-muted);">Finding: 'override_sys.py' disabled the victim's smart chair pressure sensor.</p>

            {% elif tab == 'disk' %}
                <a href="/" class="btn" style="margin-bottom:10px;">← Back to Tools</a>
                <div class="tool-title">Recovered Chat Fragment</div>
                <div class="terminal-box">
                    "Julian, if you leak the research, the lab locks down automatically at midnight..."
                </div>
                <p style="font-size:0.8rem; margin-top:10px; color:var(--text-muted);">Finding: Motive established via deleted cache files.</p>

            {% elif tab == 'iot' %}
                <a href="/" class="btn" style="margin-bottom:10px;">← Back to Tools</a>
                <div class="tool-title">SmartLab Sensor Timeline</div>
                <div class="terminal-box" style="color:#3b82f6;">
                    11:30 PM - Desk Chair #4 Pressure: Normal<br>
                    11:42 PM - Smart Door Lock: FORCE_OPEN<br>
                    11:45 PM - Ventilation Fan: Speed Max (CO2 Spike)
                </div>
                <p style="font-size:0.8rem; margin-top:10px; color:var(--text-muted);">Finding: Environmental tampering detected.</p>

            {% elif tab == 'evidence' %}
                <h3 style="font-size: 0.9rem; margin-bottom: 10px; color: var(--accent-blue);">Shared Evidence Board</h3>
                <div class="tool-card">
                    <div class="tool-title">Clue Checklist</div>
                    <ul style="font-size: 0.8rem; padding-left: 16px; color: var(--text-muted); line-height: 1.6;">
                        <li>✔ MQTT Command Injection (Network)</li>
                        <li>✔ Malicious Script `override_sys.py` (RAM)</li>
                        <li>✔ Threat Chat Fragments (Disk)</li>
                        <li>✔ Smart Door Lock Override (IoT Logs)</li>
                    </ul>
                </div>
                <div style="background:#1f2937; padding:12px; border-radius:8px; text-align:center;">
                    <p style="font-size:0.8rem; margin-bottom:8px;">Ready to solve the case?</p>
                    <button class="btn btn-green" onclick="alert('Case solved! Outstanding team investigation!')">Accuse Culprit</button>
                </div>
            {% endif %}
        </div>

        <div class="nav-bar">
            <a href="/tab/tools" class="nav-item {% if tab == 'tools' %}active{% endif %}">🔍 Tools</a>
            <a href="/tab/evidence" class="nav-item {% if tab == 'evidence' %}active{% endif %}">📋 Evidence Board</a>
            <a href="/logout" class="nav-item">🔒 Lock</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    if not session.get('authenticated'):
        session['pin'] = ''
        return render_template_string(HTML_TEMPLATE, pin_display="____", current_pin="", error=None)
    return redirect(url_for('show_tab', tab_name='tools'))

@app.route('/pin', methods=['POST'])
def pin():
    digit = request.form.get('digit')
    current_pin = request.form.get('pin', '')
    
    if digit == 'C':
        current_pin = ''
    elif digit == 'OK':
        if current_pin == '2487':
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template_string(HTML_TEMPLATE, pin_display="____", current_pin="", error="Incorrect Passcode! Try 2487")
    elif len(current_pin) < 4 and digit:
        current_pin += digit
        
    display = (current_pin + "____")[:4]
    return render_template_string(HTML_TEMPLATE, pin_display=display, current_pin=current_pin, error=None)

@app.route('/tab/<tab_name>')
def show_tab(tab_name):
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, tab=tab_name)

@app.route('/tool/<tool_name>')
def show_tool(tool_name):
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, tab=tool_name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
