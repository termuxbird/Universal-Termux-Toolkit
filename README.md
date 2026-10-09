<div align="center">

# 🥷 Universal Termux Toolkit — Itachi Edition

**10 everyday tools. One colorful terminal menu. Built for Termux.**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Termux-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

[▶️ YouTube: Termux Bird](https://youtube.com/@termuxbird)

</div>

---

## ✨ Tools

| # | Tool | What it does |
|---|------|--------------|
| 1 | CLI Browser | Open websites with the `links` text browser |
| 2 | Phone Call | Start a call via Termux:API |
| 3 | Camera | Take photos (back/front camera) |
| 4 | Social Media Downloader | Download supported public media with `yt-dlp` |
| 5 | Email Tool | Read, search and send email (IMAP/SMTP) |
| 6 | File Manager | Browse, copy, move, rename, delete files |
| 7 | Gallery | View photos taken with the Camera tool |
| 8 | Notepad Pro | Create, edit, search notes with a built-in editor |
| 9 | SMS Tool | Send and read SMS |
| 10 | Music Player | Play local audio with `mpv` |

## 📦 Installation

1. Install **Termux** and the **Termux:API** app (both from the same source, e.g. F-Droid).
2. In Termux run:

```bash
pkg update && pkg install git -y
git clone https://github.com/YOUR_USERNAME/Universal-Termux-Toolkit.git
cd Universal-Termux-Toolkit
bash install_requirements.sh
python toolkit.py
```

> Replace `YOUR_USERNAME` with your GitHub username.

Quick help: `python toolkit.py --help` (or press `H` in the menu).

## 🔐 Permissions

Camera, Phone Call and SMS need Android permissions (allow them when asked).
For shared storage run `termux-setup-storage` once.

## 📧 Email notes

- Use an **App Password** (Gmail / Yahoo). See *Email Tool → Help / Login Guide*.
- Outlook/Hotmail may need OAuth2, which is **not supported** in this version.
- Accounts are stored **in plain text** in `~/.email_tool_accounts.json` (private file permissions). Use App Passwords only — never your main password.

## ⚠️ Disclaimer

This toolkit is for personal, lawful use. Only download or access content and accounts you own or have permission to use. Respect each platform's terms of service and copyright laws. The author is not responsible for misuse.

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Command not found | Re-run `bash install_requirements.sh` |
| Storage folders missing | Run `termux-setup-storage`, then restart Termux |
| Downloader fails | `python -m pip install -U yt-dlp` |
| Camera/SMS/Call not working | Install Termux:API app and grant permissions |

## 🤝 Contributing

Issues and pull requests are welcome.

## 📜 License

[MIT](LICENSE) © 2026 Itachi (Termux Bird)

## 🐦 Credits

Created by **Itachi** — YouTube: [Termux Bird](https://youtube.com/@termuxbird)
