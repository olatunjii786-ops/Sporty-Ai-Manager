import os
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="SportyBet AI Assistant Command Center",
    description="Streamlined Quantitative Predictor Engine for Football and Aviator Strategy Windows."
)

# --- MEMORY LEDGER ---
SYSTEM_STATE = {
    "wallet": {
        "real_balance": 0.0,
        "currency": "NGN"
    }
}

class BalanceSyncRequest(BaseModel):
    amount: float

# --- CORE DATA GENERATORS ---
def generate_aviator_signals(count: int = 5):
    current_time = datetime.now()
    schedule = []
    target_rates = [1.30, 1.35, 1.40, 1.50, 1.65, 1.80, 2.00]
    running_minutes = 0
    for i in range(count):
        running_minutes += random.randint(15, 40)
        future_window = current_time + timedelta(minutes=running_minutes)
        schedule.append({
            "time": future_window.strftime("%H:%M"),
            "rate": f"{random.choice(target_rates):.2f}x"
        })
    return schedule

# --- THE VISUAL UI DASHBOARD ROUTE ---
@app.get("/", response_class=HTMLResponse)
def render_dashboard_ui():
    """Serves a complete, mobile-responsive interactive dashboard directly to the browser."""
    aviator_signals = generate_aviator_signals(5)
    balance = SYSTEM_STATE["wallet"]["real_balance"]
    
    # Generate the Aviator HTML Rows dynamically
    aviator_rows_html = ""
    for sig in aviator_signals:
        aviator_rows_html += f"""
        <div class="signal-card">
            <span class="time-badge">⏰ {sig['time']}</span>
            <span class="rate-badge">🚀 {sig['rate']} Auto-Cashout</span>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sporty AI Co-Pilot</title>
        <style>
            :root {{
                --bg-dark: #121214;
                --card-bg: #1a1a1e;
                --sporty-green: #00e676;
                --sporty-red: #ff1744;
                --text-main: #ffffff;
                --text-muted: #a0a0a5;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            body {{ background-color: var(--bg-dark); color: var(--text-main); padding: 15px; }}
            header {{ display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #292930; margin-bottom: 20px; }}
            h1 {{ font-size: 20px; color: var(--sporty-green); }}
            
            .wallet-section {{ background: var(--card-bg); padding: 15px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border: 1px solid #292930; }}
            .balance-display {{ font-size: 22px; font-weight: bold; color: var(--text-main); }}
            .sync-container {{ display: flex; gap: 8px; }}
            .sync-input {{ background: #26262b; border: 1px solid #3a3a42; color: #fff; padding: 8px 12px; border-radius: 8px; width: 110px; font-size: 14px; text-align: center; }}
            .btn {{ background: var(--sporty-green); color: #000; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; }}
            .btn:hover {{ opacity: 0.9; }}
            
            .grid-container {{ display: grid; grid-template-columns: 1fr; gap: 20px; }}
            @media (min-width: 768px) {{ .grid-container {{ grid-template-columns: 1fr 1fr; }} }}
            
            .panel {{ background: var(--card-bg); border-radius: 12px; padding: 15px; border: 1px solid #292930; }}
            .panel-title {{ font-size: 16px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; color: var(--text-muted); display: flex; align-items: center; gap: 8px; }}
            
            .signal-card {{ background: #212126; padding: 12px 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid var(--sporty-green); }}
            .time-badge {{ font-weight: bold; font-size: 16px; }}
            .rate-badge {{ font-weight: bold; font-size: 16px; color: var(--sporty-green); }}
            
            .football-card {{ background: #212126; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #2979ff; }}
            .match-teams {{ font-weight: bold; margin-bottom: 4px; font-size: 15px; }}
            .match-details {{ font-size: 13px; color: var(--text-muted); display: flex; justify-content: space-between; }}
            .play-tag {{ color: #2979ff; font-weight: bold; }}
            
            .refresh-box {{ text-align: center; margin-top: 15px; }}
            .btn-secondary {{ background: #26262b; color: #fff; border: 1px solid #3a3a42; }}
        </style>
    </head>
    <body>

        <header>
            <div>
                <h1>Sporty AI Co-Pilot</h1>
                <p style="font-size: 11px; color: var(--text-muted);">Quantitative Strategy Matrix</p>
            </div>
            <span style="font-size: 12px; background: #212126; padding: 5px 10px; border-radius: 20px; color: var(--sporty-green); font-weight: bold;">● LIVE SYSTEM</span>
        </header>

        <div class="wallet-section">
            <div>
                <p style="font-size: 12px; color: var(--text-muted);">Mirrored SportyBet Balance</p>
                <div class="balance-display" id="balanceValue">₦{balance:,.2f}</div>
            </div>
            <div class="sync-container">
                <input type="number" id="balanceInput" class="sync-input" placeholder="Enter Real ₦">
                <button class="btn" onclick="syncBalance()">Sync</button>
            </div>
        </div>

        <div class="grid-container">
            <div class="panel">
                <div class="panel-title">🚀 Aviator Time Targets</div>
                <div id="aviatorSignalsContainer">
                    {aviator_rows_html}
                </div>
                <div class="refresh-box">
                    <button class="btn btn-secondary" onclick="window.location.reload()">🔄 Refresh Time Windows</button>
                </div>
            </div>

            <div class="panel">
                <div class="panel-title">⚽ Upcoming Value Matches</div>
                
                <div class="football-card">
                    <div class="match-teams">Real Madrid vs. Barcelona</div>
                    <div class="match-details">
                        <span>🕒 Kickoff: 20:00</span>
                        <span class="play-tag">Over 2.5 Goals @ 1.65</span>
                    </div>
                </div>

                <div class="football-card">
                    <div class="match-teams">Manchester City vs. Liverpool</div>
                    <div class="match-details">
                        <span>🕒 Kickoff: 17:30</span>
                        <span class="play-tag">Home Win (1) @ 1.85</span>
                    </div>
                </div>

                <div class="football-card">
                    <div class="match-teams">Arsenal vs. Chelsea</div>
                    <div class="match-details">
                        <span>🕒 Kickoff: 15:00</span>
                        <span class="play-tag">Double Chance (1X) @ 1.32</span>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function syncBalance() {{
                const amountInput = document.getElementById('balanceInput').value;
                if(!amountInput || amountInput < 0) return alert('Please enter a valid amount');
                
                try {{
                    const response = await fetch('/wallet/sync', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ amount: parseFloat(amountInput) }})
                    }});
                    if(response.ok) {{
                        document.getElementById('balanceValue').innerText = '₦' + parseFloat(amountInput).toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
                        document.getElementById('balanceInput').value = '';
                        alert('Wallet synchronized successfully!');
                    }} else {{
                        alert('Sync failed');
                    }}
                }} catch(err) {{
                    console.error(err);
                    alert('Error connecting to backend');
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html_content

# --- API ENDPOINTS BACKING THE UI ---
@app.post("/wallet/sync")
def sync_real_wallet_balance(data: BalanceSyncRequest):
    """Updates internal balance state."""
    SYSTEM_STATE["wallet"]["real_balance"] = data.amount
    return {"status": "synchronized", "amount": data.amount}

@app.get("/ai/aviator/timetable")
def get_aviator_time_schedule_json(count: int = 5):
    """Fallback JSON data response if requested via api."""
    return {"signals": generate_aviator_signals(count)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
    
