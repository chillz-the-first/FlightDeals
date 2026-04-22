# ✈️ Flight Deal Finder

> Automated cheap flight alerts via WhatsApp & Email

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Day 40](https://img.shields.io/badge/100%20Days%20of%20Code-Day%2040-orange?style=flat)
![APIs](https://img.shields.io/badge/APIs-SerpApi%20%7C%20Sheety%20%7C%20Twilio%20%7C%20Gmail-blue?style=flat)

---

## 📋 Description

Flight Deal Finder is a Python automation tool that monitors flight prices from Cape Town (CPT) to a list of destinations stored in a Google Sheet. When a price drops below a configured threshold, it instantly alerts you via WhatsApp (Twilio) and sends deal emails to all registered users.

Built as the Day 40 capstone project for the 100 Days of Code Python Bootcamp, it combines REST APIs, environment-based secrets management, response caching, and multi-channel notifications into a single automated pipeline.

---

## ✨ Features

- 🔍 Searches Google Flights via SerpApi for both direct and indirect routes
- 📊 Reads destination wishlist and lowest prices from a live Google Sheet (Sheety)
- 🔄 Automatically updates the sheet when a new lowest price is found
- 💬 Sends a WhatsApp message via Twilio when a deal is detected
- 📧 Emails all registered users with full flight details
- ⚡ Caches API responses for 1 hour with `requests-cache` to reduce API usage
- 🔒 All secrets managed securely via `.env` — nothing hardcoded

---

## 📁 Project Structure

```
flight-deal-finder/
├── main.py                 # Entry point — orchestrates the full search loop
├── flight_search.py        # SerpApi Google Flights integration
├── flight_data.py          # FlightData model + cheapest flight logic
├── data_manager.py         # Sheety Google Sheets read/write
├── notification_manager.py # Twilio WhatsApp + Gmail SMTP alerts
├── .env                    # Secret keys (never commit this!)
├── .env.example            # Template for required environment variables
└── requirements.txt        # Python dependencies
```

---

## ⚙️ How It Works

1. **Fetch destinations** — reads city names, IATA codes, and lowest prices from your Google Sheet via Sheety
2. **Search flights** — queries SerpApi for direct flights first; falls back to indirect if none found
3. **Compare prices** — finds the cheapest available fare and compares it to the sheet's recorded lowest
4. **Alert & update** — if a cheaper deal is found, updates the sheet, sends a WhatsApp notification, and emails all users

---

## 🔧 Prerequisites

- Python 3.10 or higher
- A [SerpApi](https://serpapi.com) account with Google Flights access
- A [Sheety](https://sheety.co) account with two sheets: `prices` and `users`
- A [Twilio](https://twilio.com) account with a WhatsApp-enabled number
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) enabled

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/flight-deal-finder.git
cd flight-deal-finder
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your environment

```bash
cp .env.example .env
```

Then open `.env` and fill in your API keys (see table below).

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|:---:|
| `SERP_KEY` | Your SerpApi API key | ✅ |
| `SERP_ENDPOINT` | SerpApi base URL (`https://serpapi.com/search`) | ✅ |
| `SHEETY_FLIGHTS_ENDPOINT` | Sheety endpoint for your prices sheet | ✅ |
| `SHEETY_USERS_ENDPOINT` | Sheety endpoint for your users sheet | ✅ |
| `SHEETY_BEARER` | Sheety Bearer token for authentication | ✅ |
| `TWILIO_SID` | Twilio Account SID | ✅ |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | ✅ |
| `TWILIO_VIRTUAL_NUMBER` | Your Twilio WhatsApp sender number | ✅ |
| `TWILIO_WHATSAPP_NUMBER` | Your personal WhatsApp number to receive alerts | ✅ |
| `SENDER_EMAIL` | Gmail address to send deal emails from | ✅ |
| `GMAIL_APP_PASSWORD` | Gmail App Password (not your login password) | ✅ |
| `SMTP_SERVER` | SMTP server — defaults to `smtp.gmail.com` | ➖ |

### .env.example

```
SERP_KEY=your_serpapi_key_here
SERP_ENDPOINT=https://serpapi.com/search
SHEETY_FLIGHTS_ENDPOINT=https://api.sheety.co/xxx/flightDeals/prices
SHEETY_USERS_ENDPOINT=https://api.sheety.co/xxx/flightDeals/users
SHEETY_BEARER=your_sheety_bearer_token
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_VIRTUAL_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=+0987654321
SENDER_EMAIL=youraddress@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
SMTP_SERVER=smtp.gmail.com
```

---

## 📦 requirements.txt

```
requests
requests-cache
python-dotenv
twilio
```

---

## 📊 Google Sheet Setup

Your Sheety project should have two sheets:

### prices sheet

| city | iataCode | lowestPrice |
|------|----------|-------------|
| Paris | CDG | 8000 |
| Tokyo | TYO | 12000 |
| London | LON | 9000 |

### users sheet

| firstName | lastName | emailAddress |
|-----------|----------|--------------|
| Jane | Doe | jane@example.com |

> 💡 Prices are in **ZAR (South African Rand)**. Update `currency` in `flight_search.py` if needed.

---

## ▶️ Running the Script

```bash
python main.py
```

> 💡 **Tip:** Schedule this with a cron job (Linux/macOS) or Task Scheduler (Windows) to run daily and catch deals automatically.

**Example cron job — runs every morning at 8am:**
```bash
0 8 * * * /usr/bin/python3 /path/to/flight-deal-finder/main.py
```

---

## 🔒 Security Notes

- **Never commit your `.env` file** — it contains sensitive API keys
- Add `.env` to your `.gitignore` before your first commit
- Use a **Gmail App Password**, not your regular Google account password
- Rotate your API keys if you accidentally expose them publicly

```bash
# .gitignore
.env
flight_cache.sqlite
__pycache__/
*.pyc
```

---

## 🛠️ Built With

| Service | Purpose |
|---------|---------|
| [SerpApi](https://serpapi.com) | Google Flights search API |
| [Sheety](https://sheety.co) | Google Sheets as a REST API |
| [Twilio](https://twilio.com) | WhatsApp messaging |
| [smtplib](https://docs.python.org/3/library/smtplib.html) | Email via Gmail SMTP |
| [requests-cache](https://requests-cache.readthedocs.io) | Transparent HTTP response caching |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` file management |

---

## 🎓 Course

Built as part of the **[100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/)** by Dr. Angela Yu on Udemy — Day 40 Capstone Project.

---

*Made with ☕ and Python during 100 Days of Code*