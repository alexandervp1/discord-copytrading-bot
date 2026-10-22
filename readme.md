# Discord Trade Bot

A Discord bot that watches analyst channels, reads their trade calls and updates,
and executes and manages the trades on a crypto exchange account: entries, stop
losses, staged take profits, and automatic SL adjustments.

> ⚠️ **Trading involves substantial risk of loss.** This software is provided as-is,
> with no guarantee of profit. Always test on the exchange testnet before using
> real funds. Not financial advice.

## How it works

1. Listens to the analyst channels set in the configuration
2. Classifies each message as a new call, an update, or noise
3. Extracts symbol, side, entry, stop loss, and take profits
4. Validates the result (sanity checks and risk limits)
5. Places the entry, SL, and TP orders on the exchange
6. Manages the trade after entry:
   - TP1 hit: trim 25%, move SL to breakeven
   - TP2 hit: trim 50%, move SL to TP1
   - TP3 hit: close the remaining position
   - Analyst update ("closing entirely", "moving SL"): applied to the matching trade
7. Sends anything unclear to a private review channel for manual approval

Trim percentages are configurable per analyst.

## Status

- [ ] Discord listener
- [ ] Message parser
- [ ] Exchange execution (testnet)
- [ ] Database (open trades, processed messages)
- [ ] Trade management (TP trims, SL to breakeven)
- [ ] Risk controls
- [ ] AI classification and image reading
- [ ] Review queue
- [ ] Live trading with small size

## Project structure

```
bot/
  main.py            entry point
  config.py          loads .env and config.yaml
  discord_client.py  channel listener
  parser.py          message -> signal
  exchange.py        order placement (ccxt)
  manager.py         TP/SL management
  risk.py            limits and sanity checks
  db.py              SQLite state
  ai.py              message classification and image reading
  review.py          review queue with buttons
tests/               parser and manager tests
data/                runtime files (gitignored)
```

## Setup

### Requirements

- Python 3.11+
- A Discord bot token, with **Message Content Intent** enabled
- Exchange API keys with **trade-only** permissions (no withdrawals), IP-whitelisted
- An AI provider API key (for the AI features)

### Install

```bash
git clone <your-repo-url>
cd discord-trade-bot
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
```

Windows: copy `.env.example` and rename the copy to `.env`.

Then fill in `.env`:

```
DISCORD_TOKEN=
CHANNEL_IDS=
EXCHANGE_API_KEY=
EXCHANGE_API_SECRET=
USE_TESTNET=true
```

### Run

```bash
python -m bot.main
```

## Discord bot setup

1. Create an application in the Discord Developer Portal and add a bot
2. On the **Bot** tab, enable **Message Content Intent** and click Save Changes
3. In **OAuth2 → URL Generator**, select the `bot` scope and these permissions:
   View Channels, Send Messages, Embed Links, Read Message History, Add Reactions
4. Open the generated link to invite the bot to the server
5. Give the bot read-only access to the analyst channels, and send access only in
   the private review channel

## Safety

- Start with `USE_TESTNET=true` and stay on testnet for at least a couple of weeks
- **Never commit `.env` or real API keys.** Rotate any key that leaks
- Use trade-only API keys with an IP whitelist
- Messages that can't be parsed with confidence are not traded
- Each Discord message is processed only once
- The AI outputs data only. Orders are placed by code after validation
- Do not use a user-account token ("self-bot"), which violates Discord's ToS

## Tests

```bash
pytest
```

## Disclaimer

The authors are not responsible for any financial losses. Use at your own risk.
