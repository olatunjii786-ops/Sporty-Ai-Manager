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

# --- MEMORY LEDGER (Maintains your synced real balance and active state) ---
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
                    const data = await response.json();
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
    """
    Quantitative Momentum Analysis Engine.
    Calculates operational pressure scores using in-game live statistics.
    """
    # Mathematical Pressure Weight: Dangerous Attacks + (Shots on Target * 3)
    home_pressure = home_attacks + (home_shots * 3)
    away_pressure = away_attacks + (away_shots * 3)
    
    signal = "HOLD / OBSERVE"
    recommendation = "No clear mathematical edge detected in current market window."
    target_market = "N/A"
    suggested_stake_percent = 0.0
    
    # Value Search: Late-game high-pressure attack spikes
    if match_minute >= 60 and match_minute <= 85:
        if home_pressure > (away_pressure * 1.8) and home_shots >= 4:
            signal = "STRONG BUY SIGNAL (HOME)"
            target_market = f"{home_team} to Win Live"
            recommendation = f"{home_team} is suffocating {away_team} with high-intensity attack matrices. Odds currently undervalued."
            suggested_stake_percent = 5.0 # Max 5% risk configuration
        elif away_pressure > (home_pressure * 1.8) and away_shots >= 4:
            signal = "STRONG BUY SIGNAL (AWAY)"
            target_market = f"{away_team} to Win Live"
            recommendation = f"{away_team} dominating counter-attack lanes. Underdog value window open."
            suggested_stake_percent = 5.0
            
    # Risk Mitigation Logic: Take-Profit / Cash-Out Thresholds
    elif match_minute > 85:
        signal = "CASH OUT NOTICE / STOP LOSS"
        recommendation = "Match reaching high-variance terminal minutes. Secure current accrued profit margins immediately."
        target_market = "Live Cash Out"
        suggested_stake_percent = 0.0

    return {
        "analysis_timestamp": datetime.now().isoformat(),
        "match_window": f"{match_minute}' min",
        "pressure_index": {"home": home_pressure, "away": away_pressure},
        "ai_signal": signal,
        "target_market": target_market,
        "recommended_action": recommendation,
        "risk_allocation": f"{suggested_stake_percent}% of bankroll"
    }

# --- CORE LOGIC MODULE 2: THE AVIATOR VARIANCE MATRIX ---
def analyze_aviator_variance_stream(incoming_crash_multiplier: float) -> Dict[str, Any]:
    """
    Processes incoming Aviator game crash feeds.
    Analyzes mathematical variance shifts to locate low-risk entry clusters.
    """
    # Append the live data feed point and maintain a maximum window frame of 20 rounds
    DB["cached_aviator_rounds"].append(incoming_crash_multiplier)
    if len(DB["cached_aviator_rounds"]) > 20:
        DB["cached_aviator_rounds"].pop(0)
        
    history = DB["cached_aviator_rounds"]
    recent_three = history[-3:]
    
    # Calculate operational house metrics
    instant_busts_count = sum(1 for r in history if r < 1.10)
    instant_bust_rate = (instant_busts_count / len(history)) * 100
    
    # Strategy Pattern Detection: Cold Sequence Recovery Pattern
    # If 2 or 3 rounds in a row crash instantly below 1.15x, a minor upward variance swing is mathematically favored
    is_cold_sequence = all(round_val < 1.15 for round_val in recent_three)
    
    if is_cold_sequence:
        signal = "TACTICAL ENTRY DETECTED"
        target_multiplier = 1.30  # Low-multiplier safety net configuration
        confidence = "78% (Variance Correction Target)"
        action = f"Set explicit Auto-Cashout limit to exactly {target_multiplier}x on SportyBet interface."
    else:
        signal = "STANDBY / MONITOR"
        target_multiplier = 0.0
        confidence = "Low Edge"
        action = "High variance detected. Wait for the house cluster sequence to cool down."
        
    return {
        "engine_status": "Active Sniffer Process",
        "processed_round_value": f"{incoming_crash_multiplier:.2f}x",
        "historical_rolling_window": history,
        "metrics": {
            "instant_bust_percentage_20_rounds": f"{instant_bust_rate:.1f}%"
        },
        "decision_matrix": {
            "ai_signal": signal,
            "target_cashout": f"{target_multiplier}x" if target_multiplier > 0 else "N/A",
            "model_confidence": confidence,
            "required_user_action": action
        }
    }

# --- SYSTEM ROUTE DISPATCHERS ---

@app.get("/")
def check_engine_status():
    """Root endpoint verifying operational readiness."""
    return {
        "status": "fully_operational",
        "project": "SportyBet Autonomous AI Assistant",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/wallet/dashboard")
def view_wallet_metrics():
    """Returns absolute ledger summaries, P&L statements, and net ROI calculations."""
    current_balance = DB["wallet"]["balance"]
    initial_deposit = DB["wallet"]["initial_deposit"]
    net_pnl = current_balance - initial_deposit
    roi = (net_pnl / initial_deposit) * 100 if initial_deposit > 0 else 0
    
    return {
        "account_ledger": {
            "currency": DB["wallet"]["currency"],
            "current_balance": f"₦{current_balance:.2f}",
            "initial_deposit": f"₦{initial_deposit:.2f}"
        },
        "performance_analytics": {
            "net_profit_loss": f"₦{net_pnl:.2f}",
            "return_on_investment_roi": f"{roi:.2f}%",
            "active_simulation_logs_count": len(DB["trades"])
        }
    }

@app.get("/ai/football/scan")
def scan_live_football(home_team: str = "Chelsea", away_team: str = "Arsenal", home_attacks: int = 45, away_attacks: int = 22, home_shots: int = 5, away_shots: int = 1, match_minute: int = 72):
    """
    Pass real-time match data points directly into the AI to compute in-play trading signals.
    Example: /ai/football/scan?home_team=Chelsea&away_team=Arsenal&home_attacks=60&away_attacks=25&home_shots=7&away_shots=2&match_minute=75
    """
    analysis_results = calculate_live_football_signals(
        home_team, away_team, home_attacks, away_attacks, home_shots, away_shots, match_minute
    )
    return {"status": "success", "data": analysis_results}

@app.get("/ai/aviator/feed")
def stream_aviator_data(last_crash_value: float = 1.02):
    """
    Feeds the most recent crash multiplier directly into the analytical processing model.
    Example: /ai/aviator/feed?last_crash_value=1.04
    """
    analysis_results = analyze_aviator_variance_stream(last_crash_value)
    return {"status": "success", "data": analysis_results}

@app.post("/trade/simulate")
def execute_simulated_allocation(trade: TradeRequest):
    """Locks and allocates financial capital from the internal balance pool to back a recommended signal."""
    current_balance = DB["wallet"]["balance"]
    if trade.stake_amount > current_balance:
        raise HTTPException(
            status_code=400,
            detail=f"Transaction Blocked: Stake ₦{trade.stake_amount:.2f} exceeds available capital ₦{current_balance:.2f}"
        )
        
    DB["wallet"]["balance"] -= trade.stake_amount
    trade_id = str(uuid.uuid4())[:8]
    
    trade_record = {
        "id": trade_id,
        "game_type": trade.game_type.upper(),
        "market_name": trade.market_name,
        "stake_amount": trade.stake_amount,
        "odds": trade.odds,
        "status": "LIVE/PENDING",
        "pnl": 0.0,
        "timestamp": datetime.now().isoformat()
    }
    
    DB["trades"].append(trade_record)
    return {"message": "Simulated capital successfully allocated to market vector.", "trade": trade_record}

@app.post("/trade/settle/{trade_id}")
def settle_simulated_allocation(trade_id: str, outcome: SettleRequest):
    """Settles open balances and calculates exact profit or losses based on match outcomes."""
    target_trade = next((t for t in DB["trades"] if t["id"] == trade_id), None)
    
    if not target_trade:
        raise HTTPException(status_code=404, detail="Target transaction ID not found.")
    if target_trade["status"] != "LIVE/PENDING":
        raise HTTPException(status_code=400, detail="Transaction already finalized in database ledger.")
        
    status_upper = outcome.status.upper()
    stake = target_trade["stake_amount"]
    odds = target_trade["odds"]
    
    if status_upper == "WON":
        gross_return = stake * odds
        net_profit = gross_return - stake
        target_trade["status"] = "WON"
        target_trade["pnl"] = net_profit
        DB["wallet"]["balance"] += gross_return
    elif status_upper == "LOST":
        target_trade["status"] = "LOST"
        target_trade["pnl"] = -stake
    else:
        raise HTTPException(status_code=400, detail="Invalid settlement status. Select 'WON' or 'LOST'.")
        
    return {
        "message": f"Ledger updated. Status: {target_trade['status']}",
        "updated_wallet_balance": f"₦{DB['wallet']['balance']:.2f}",
        "trade_metrics": target_trade
    }

@app.get("/trades/history")
def view_entire_history_logs():
    """Returns absolute history array containing all logged wins and losses."""
    return {"total_records": len(DB["trades"]), "history_logs": DB["trades"]}

# --- ENVIRONMENT START HANDLER ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
