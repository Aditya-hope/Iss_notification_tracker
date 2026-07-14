# ISS Overhead Notifier

A simple Python script that checks whether the International Space Station (ISS) is currently overhead **and** it's nighttime at your location. If both are true, it emails you so you can go outside and spot it.

## How It Works

Every 60 seconds, the script:

1. **Checks ISS position** — calls the [Open Notify API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/) to get the ISS's current latitude/longitude, and compares it against your location (within a ±5° box).
2. **Checks if it's night** — calls the [Sunrise-Sunset API](https://sunrise-sunset.org/api) to get sunrise/sunset times (UTC) for your location, and checks if the current hour falls outside daylight hours.
3. **Sends an email** — if the ISS is overhead *and* it's night, sends yourself an email via Gmail SMTP.

## Requirements

- Python 3.x
- `requests` library

```bash
pip install requests
```

## Setup

1. **Set your coordinates** — update `My_lat` and `My_long` in the script with your location's latitude and longitude.

2. **Gmail App Password** — you'll need a [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your regular Gmail password) since this script logs into Gmail's SMTP server directly.

   ⚠️ **Never hardcode your email or app password in the script**, especially if you push this to GitHub. The script reads them from environment variables instead:

   ```python
   my_email = os.environ["ISS_EMAIL"]
   app_password = os.environ["ISS_APP_PASSWORD"]
   ```

   **Set them before running:**

   PowerShell (current session only):
   ```powershell
   $env:ISS_EMAIL="you@gmail.com"
   $env:ISS_APP_PASSWORD="your-app-password"
   ```

   PowerShell (persistent — saved to your user environment):
   ```powershell
   setx ISS_EMAIL "you@gmail.com"
   setx ISS_APP_PASSWORD "your-app-password"
   ```
   *(Close and reopen your terminal/editor after using `setx` for it to take effect.)*

   macOS/Linux (bash/zsh):
   ```bash
   export ISS_EMAIL="you@gmail.com"
   export ISS_APP_PASSWORD="your-app-password"
   ```

3. **Run it:**

   ```bash
   python iss_tracker.py
   ```

   The script runs in an infinite loop, checking every 60 seconds. Stop it with `Ctrl+C`.

## Notes / Known Limitations

- **Timezone mismatch:** the Sunrise-Sunset API returns sunrise/sunset in UTC, but `datetime.now().hour` uses your local system time. These are compared directly without converting, so the night-check may be off depending on your UTC offset. Worth fixing if results seem wrong.
- The `±5°` overhead window is a rough approximation — it doesn't account for actual visibility (line of sight, weather, ISS altitude), just a loose bounding box.
- The APIs used are free and unauthenticated but have no uptime guarantees; consider adding retry/error handling for long-running use.
- Email is sent every time both conditions are true — since the loop checks every minute, you may get repeated emails while the ISS remains overhead. Consider adding a cooldown or an "already notified" flag if that's not desired.
- If your app password is ever accidentally exposed (e.g. pasted somewhere, committed to git), revoke it immediately at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) and generate a new one.

## License

Free to use and modify.