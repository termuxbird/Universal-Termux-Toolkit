#!/usr/bin/env python3
"""
UNIVERSAL TERMUX TOOLKIT  (single-file edition)

Tools: CLI Browser, Phone Call, Camera, Social Media Downloader, Email Tool,
       File Manager, Gallery, Notepad Pro, SMS Tool, Music Player

Setup (Termux):
    termux-setup-storage
    pkg update && pkg install python termux-api links mpv ffmpeg -y
    python -m pip install -U "yt-dlp[default]"
    python toolkit.py
    python toolkit.py --help
"""

import email
import getpass
import imaplib
import json
import mimetypes
import os
import shutil
import smtplib
import socket
import ssl
import subprocess
import sys
import time
from datetime import datetime
from email.header import decode_header
from email.message import EmailMessage
from pathlib import Path

PYTHON = sys.executable
HOME = Path.home()
SHARED = HOME / "storage" / "shared"


# Terminal styling gracefully falls back when colors are unavailable.
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    PURPLE = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    DIM = "\033[2m"


def paint(value, color):
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return str(value)
    return f"{color}{value}{Style.RESET}"


def banner():
    clear()
    print(paint("╔══════════════════════════════════════════════════╗", Style.CYAN))
    print(paint("║          UNIVERSAL TERMUX TOOLKIT                ║", Style.CYAN + Style.BOLD))
    print(paint("║              ITACHI EDITION  •  v1.1             ║", Style.PURPLE + Style.BOLD))
    print(paint("╚══════════════════════════════════════════════════╝", Style.CYAN))
    print(paint("  10 everyday tools • One terminal • Built for Termux", Style.GREEN))
    print(paint("  Created by Itachi  •  YouTube: Termux Bird", Style.YELLOW))
    print(paint("─" * 52, Style.DIM))


def help_tool(pause_after=True):
    banner()
    print(paint("HELP & QUICK START", Style.CYAN + Style.BOLD))
    print("""
USAGE
  python toolkit.py              Launch the interactive menu
  python toolkit.py --help       Show this help in the terminal

TOOLS
  1. CLI Browser                 Open websites with the Links text browser
  2. Phone Call                  Start a call through Termux:API
  3. Camera                      Capture photos using the Android camera
  4. Social Media Downloader     Download supported public media with yt-dlp
  5. Email Tool                  Read and send email using configured IMAP/SMTP
  6. File Manager                Browse and manage files
  7. Gallery                     Browse images and media
  8. Notepad Pro                 Create and manage notes
  9. SMS Tool                    Send SMS through Termux:API
 10. Music Player                Play local audio with mpv

SETUP
  1. Run: bash install_requirements.sh
  2. Install the Termux:API Android app from the same trusted source as Termux.
  3. Grant Android permissions when prompted.
  4. Run: python toolkit.py

TIPS & TROUBLESHOOTING
  • If a command is missing, rerun install_requirements.sh.
  • If storage is unavailable, run: termux-setup-storage
  • Camera, call, and SMS features require Termux:API and Android permissions.
  • Email providers may require an App Password; see Email Tool > Help / Login Guide.
  • Download only content you have permission to access and save.

CREDITS
  Created by Itachi  |  YouTube: Termux Bird
  https://youtube.com/@termuxbird
  Built with Python and open-source Termux utilities.
""")
    if pause_after:
        pause("\nPress Enter to return to the main menu...")


def pause(msg="\nPress Enter to continue..."):
    input(msg)


def clear():
    os.system("clear")


# ======================================================================
# 1. CLI BROWSER
# ======================================================================
def browser_tool():
    while True:
        print("\n==============================")
        print("       TERMUX CLI BROWSER")
        print("==============================")
        print("1.  Open URL")
        print("2.  Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            url = input("🌐 URL: ").strip()
            if not url:
                print("URL is required.")
                continue
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            try:
                subprocess.run(["links", url])
            except FileNotFoundError:
                print("'links' is not installed. Run: pkg install links")
        elif choice == "2":
            break
        else:
            print("Invalid option.")


# ======================================================================
# 2. PHONE CALL
# ======================================================================
def call_tool():
    number = input("Phone number: ").strip()
    if not number:
        print("Phone number is required.")
        return
    try:
        subprocess.run(["termux-telephony-call", number])
    except FileNotFoundError:
        print("termux-api is not installed. Run: pkg install termux-api")


# ======================================================================
# 3. CAMERA
# ======================================================================
CAMERA_DIR = SHARED / "termux-photos"


def camera_tool():
    CAMERA_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        print("\n==========================")
        print("       CAMERA TOOL")
        print("==========================")
        print("1.  Take Photo")
        print("2.  Front Camera")
        print("3.  Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            camera = "0"
        elif choice == "2":
            camera = "1"
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
            continue

        filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
        path = CAMERA_DIR / filename

        try:
            subprocess.run(["termux-camera-photo", "-c", camera, str(path)], check=True)
            print("\nPhoto saved:")
            print(path)
        except Exception as e:
            print("Camera error:", e)


# ======================================================================
# 4. SOCIAL MEDIA DOWNLOADER
# ======================================================================
DL_DIR = SHARED / "Download" / "SocialDownloader"


def dl_banner():
    clear()
    print("=" * 40)
    print("       SOCIAL DOWNLOADER")
    print("        TERMUX EDITION")
    print("=" * 40)
    print(" YouTube | Instagram | TikTok | Facebook")
    print("-" * 40)


def dl_check_setup():
    try:
        subprocess.run(
            [PYTHON, "-m", "yt_dlp", "--version"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp is not installed.")
        print('Run: python -m pip install -U "yt-dlp[default]"')
        return False

    try:
        ok = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        ).returncode == 0
    except FileNotFoundError:
        ok = False
    if not ok:
        print("Warning: FFmpeg is missing. Audio conversion or merging may fail.")
    return True


def dl_ask_url():
    url = input("\nPaste video URL (B = Back): ").strip()
    if url.lower() == "b":
        return None
    if not url.startswith(("https://", "http://")):
        print("Enter a valid HTTP or HTTPS URL.")
        return None
    return url


def dl_download(url, mode):
    DL_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        PYTHON, "-m", "yt_dlp",
        "--no-playlist", "--newline", "--progress",
        "--restrict-filenames", "--windows-filenames",
        "-P", str(DL_DIR),
        "-o", "%(title).180B_%(id)s.%(ext)s",
    ]

    if mode == "video":
        print("\nVideo quality:")
        print("1. Best available")
        print("2. Up to 720p")
        print("3. Up to 480p")
        quality = input("Select an option: ").strip()
        if quality == "1":
            cmd += ["-f", "bv*+ba/b"]
        elif quality == "2":
            cmd += ["-f", "bv*[height<=720]+ba/b[height<=720]"]
        elif quality == "3":
            cmd += ["-f", "bv*[height<=480]+ba/b[height<=480]"]
        else:
            print("Invalid quality option.")
            return
        cmd += ["--merge-output-format", "mp4"]
    else:
        print("\nAudio format:")
        print("1. MP3")
        print("2. M4A (if supported)")
        print("3. Best available audio")
        audio = input("Select an option: ").strip()
        if audio == "1":
            cmd += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
        elif audio == "2":
            cmd += ["-x", "--audio-format", "m4a"]
        elif audio == "3":
            cmd += ["-f", "bestaudio/best", "-x"]
        else:
            print("Invalid audio option.")
            return

    cmd += ["--", url]

    print("\nStarting download...")
    print("Save folder:", DL_DIR)
    print("Press Ctrl+C to cancel.\n")

    try:
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print("\nDownload complete!")
        else:
            print("\nDownload failed.")
            print("The link may be unsupported, private, restricted, or temporarily unavailable.")
            print("To update yt-dlp, run: python -m pip install -U yt-dlp")
    except KeyboardInterrupt:
        print("\nDownload cancelled.")
    except FileNotFoundError as e:
        print("\nRequired program not found:", e)


def dl_browse_files():
    DL_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        clear()
        print("=" * 36)
        print("       DOWNLOADED FILES")
        print("=" * 36)

        files = sorted(
            [f for f in DL_DIR.iterdir()
             if f.is_file() and not f.name.endswith(".part")],
            key=lambda f: f.stat().st_mtime, reverse=True,
        )

        if not files:
            print("No downloaded files found.")
            print("\nFolder:", DL_DIR)
            input("\nPress Enter to go back...")
            return

        for i, f in enumerate(files, 1):
            size = f.stat().st_size
            text = (f"{size / (1024 * 1024):.1f} MB" if size >= 1024 * 1024
                    else f"{size / 1024:.1f} KB")
            print(f"{i}. {f.name} ({text})")

        print("\nB. Back to menu")
        pick = input("\nEnter file number to open: ").strip().lower()
        if pick == "b":
            return

        if pick.isdigit() and 1 <= int(pick) <= len(files):
            selected = files[int(pick) - 1]
            print("\nSelected:", selected.name)
            print("Path:", selected)
            try:
                subprocess.run(["termux-open", str(selected)], check=False)
            except FileNotFoundError:
                print("Open this file using your Android file manager.")
            input("\nPress Enter to go back...")
        else:
            input("Invalid number. Press Enter...")


def downloader_tool():
    if not dl_check_setup():
        return

    while True:
        dl_banner()
        print("1. Download Video")
        print("2. Download Audio")
        print("3. Open Download Folder")
        print("4. Update Download Engine")
        print("5. Exit")
        print("-" * 40)

        choice = input("Select an option: ").strip()

        if choice in ("1", "2"):
            url = dl_ask_url()
            if url:
                dl_download(url, "video" if choice == "1" else "audio")
                pause("\nPress Enter to return to the menu...")
        elif choice == "3":
            dl_browse_files()
        elif choice == "4":
            subprocess.run([PYTHON, "-m", "pip", "install", "-U", "yt-dlp"])
            pause("\nPress Enter to return to the menu...")
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
            pause("\nPress Enter to return to the menu...")


# ======================================================================
# 5. EMAIL TOOL
# ======================================================================
EMAIL_CONFIG = HOME / ".email_tool_accounts.json"

EMAIL_PROVIDERS = {
    "gmail.com": ("imap.gmail.com", 993, "smtp.gmail.com", 465),
    "yahoo.com": ("imap.mail.yahoo.com", 993, "smtp.mail.yahoo.com", 465),
    "outlook.com": ("outlook.office365.com", 993, "smtp.office365.com", 587),
    "hotmail.com": ("outlook.office365.com", 993, "smtp.office365.com", 587),
    "live.com": ("outlook.office365.com", 993, "smtp.office365.com", 587),
}


def em_load_accounts():
    try:
        with open(EMAIL_CONFIG) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def em_save_accounts(accounts):
    fd = os.open(EMAIL_CONFIG, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(accounts, f, indent=2)
    os.chmod(EMAIL_CONFIG, 0o600)


def em_show_help():
    print("""
========== EMAIL LOGIN HELP ==========

GMAIL:
1. Enable 2-Step Verification in your Google Account.
2. Open: https://myaccount.google.com/apppasswords
3. Generate an App Password.
4. Use the App Password instead of your normal password.

YAHOO:
1. Open Yahoo Account Security.
2. Generate an App Password.
3. Use the App Password when adding your email account.

OUTLOOK / HOTMAIL:
Normal-password sign-in may fail.
OAuth2 may be required; this version
does not support OAuth2 sign-in.

CUSTOM EMAIL:
Enter your provider's IMAP/SMTP server details.

Never share your password.
======================================
""")


def em_auth_error(e):
    msg = str(e).lower()
    if any(x in msg for x in ("auth", "password", "credentials",
                               "login failed", "authentication")):
        print("Login failed: incorrect App Password or authentication issue.")
        print("Check the Help / Login Guide option.")
    else:
        print("Email error:", e)


def em_add_account():
    address = input("Email address: ").strip()
    if "@" not in address:
        print("Invalid email address.")
        return

    domain = address.rsplit("@", 1)[1].lower()
    defaults = EMAIL_PROVIDERS.get(domain)

    if defaults:
        imap_host, imap_port, smtp_host, smtp_port = defaults
    else:
        print("Custom provider detected.")
        imap_host = input("IMAP host: ").strip()
        try:
            imap_port = int(input("IMAP port [993]: ").strip() or "993")
            smtp_host = input("SMTP host: ").strip()
            smtp_port = int(input("SMTP port [465]: ").strip() or "465")
        except ValueError:
            print("Invalid port.")
            return

    password = getpass.getpass("Password / App Password (hidden): ")
    if not password:
        print("Password is required.")
        return

    accounts = em_load_accounts()
    accounts[address] = {
        "password": password,
        "imap_host": imap_host, "imap_port": imap_port,
        "smtp_host": smtp_host, "smtp_port": smtp_port,
    }
    em_save_accounts(accounts)
    print("Account saved locally.")


def em_choose_account():
    accounts = em_load_accounts()
    addresses = list(accounts)
    if not addresses:
        print("Add an account first.")
        return None, None

    for i, address in enumerate(addresses, 1):
        print(f"{i}. {address}")

    try:
        index = int(input("Select account: ")) - 1
        if index < 0:
            raise IndexError
        return addresses[index], accounts[addresses[index]]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None, None


def em_decode_text(value):
    if not value:
        return ""
    result = []
    for part, enc in decode_header(value):
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def em_get_body(msg):
    parts = msg.walk() if msg.is_multipart() else [msg]
    for part in parts:
        if part.get_content_type() != "text/plain":
            continue
        if "attachment" in str(part.get("Content-Disposition", "")).lower():
            continue
        data = part.get_payload(decode=True)
        if data:
            return data.decode(part.get_content_charset() or "utf-8", errors="replace")
    return "[No plain-text message]"


def em_read_mail(address, account, search_term=None, sent=False):
    server = None
    try:
        server = imaplib.IMAP4_SSL(
            account["imap_host"], account["imap_port"],
            ssl_context=ssl.create_default_context(), timeout=20,
        )
        server.login(address, account["password"])

        if sent:
            status, _ = server.select('"[Gmail]/Sent Mail"', readonly=True)
            if status != "OK":
                status, _ = server.select('"Sent"', readonly=True)
        else:
            status, _ = server.select("INBOX", readonly=True)

        if status != "OK":
            print("Could not open the mail folder.")
            return

        if search_term:
            safe = search_term.replace("\\", "\\\\").replace('"', '\\"')
            status, data = server.search(
                None, "OR", "FROM", f'"{safe}"', "SUBJECT", f'"{safe}"'
            )
        else:
            status, data = server.search(None, "ALL")

        if status != "OK":
            print("Search failed.")
            return

        ids = data[0].split()
        ids = ids[::-1][:5] if search_term else ids[-5:][::-1]
        if not ids:
            print("No emails found.")
            return

        for mid in ids:
            status, content = server.fetch(mid, "(RFC822)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(content[0][1])
            print("\n" + "=" * 36)
            print("From:", em_decode_text(msg.get("From")))
            print("To:", em_decode_text(msg.get("To")))
            print("Subject:", em_decode_text(msg.get("Subject")))
            print("Date:", msg.get("Date", ""))
            print("-" * 36)
            print(em_get_body(msg)[:2000])

    except imaplib.IMAP4.error as e:
        em_auth_error(e)
    except (OSError, TimeoutError) as e:
        print("Connection error:", e)
    except Exception as e:
        print("Email error:", e)
    finally:
        if server:
            try:
                server.logout()
            except Exception:
                pass


def em_send_mail(address, account):
    to = input("Recipient email: ").strip()
    subject = input("Subject: ").strip()
    if "@" not in to:
        print("Invalid recipient email.")
        return

    print("Enter your message; type a single dot (.) on a new line to finish:")
    lines = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)

    msg = EmailMessage()
    msg["From"] = address
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content("\n".join(lines))

    try:
        context = ssl.create_default_context()
        if account["smtp_port"] == 465:
            with smtplib.SMTP_SSL(account["smtp_host"], account["smtp_port"],
                                  context=context, timeout=20) as server:
                server.login(address, account["password"])
                server.send_message(msg)
        else:
            with smtplib.SMTP(account["smtp_host"], account["smtp_port"],
                              timeout=20) as server:
                server.starttls(context=context)
                server.login(address, account["password"])
                server.send_message(msg)
        print("Email sent.")
    except smtplib.SMTPAuthenticationError:
        print("Incorrect App Password or SMTP authentication rejected.")
        print("Check the Help / Login Guide option.")
    except Exception as e:
        print("Send failed:", e)


def email_tool():
    while True:
        print("""
========== EMAIL TOOL ==========
1. Add account
2. Read inbox
3. Send email
4. Search emails
5. View sent emails
6. Remove account
7. Help / Login Guide
8. Exit
""")
        choice = input("Choose: ").strip()

        if choice == "1":
            em_add_account()
        elif choice in ("2", "3", "4", "5"):
            address, account = em_choose_account()
            if not account:
                continue
            if choice == "2":
                em_read_mail(address, account)
            elif choice == "3":
                em_send_mail(address, account)
            elif choice == "4":
                term = input("Search sender or subject: ").strip()
                em_read_mail(address, account, search_term=term)
            elif choice == "5":
                em_read_mail(address, account, sent=True)
        elif choice == "6":
            accounts = em_load_accounts()
            addresses = list(accounts)
            for i, address in enumerate(addresses, 1):
                print(f"{i}. {address}")
            try:
                idx = int(input("Account number to remove: ")) - 1
                if idx < 0:
                    raise IndexError
                del accounts[addresses[idx]]
                em_save_accounts(accounts)
                print("Account removed.")
            except (ValueError, IndexError):
                print("Invalid selection.")
        elif choice == "7":
            em_show_help()
        elif choice == "8":
            break
        else:
            print("Invalid option.")


# ======================================================================
# 6. FILE MANAGER
# ======================================================================
def fm_size_text(path):
    try:
        size = os.path.getsize(path)
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except OSError:
        return "?"


def filemanager_tool():
    start = str(SHARED)
    current = start
    clipboard = None
    operation = "copy"

    while True:
        print("\n" + "=" * 38)
        print("           FILE MANAGER")
        print("=" * 38)
        print("📍", current)
        print("-" * 38)

        try:
            items = sorted(
                os.listdir(current),
                key=lambda x: (not os.path.isdir(os.path.join(current, x)), x.lower()),
            )
        except OSError as e:
            print("Could not open folder:", e)
            if current == start:
                print("Run 'termux-setup-storage' first if storage is not set up.")
                return
            current = start
            continue

        if not items:
            print("Folder is empty.")

        for i, name in enumerate(items, 1):
            path = os.path.join(current, name)
            icon = "📁" if os.path.isdir(path) else "📄"
            extra = "" if os.path.isdir(path) else f" ({fm_size_text(path)})"
            print(f"{i}. {icon} {name}{extra}")

        print("\n[B] Back  [O] Open file  [R] Refresh")
        print("[N] New folder  [M] Rename  [D] Delete")
        print("[C] Copy  [V] Paste  [T] Move")
        print("[Q] Exit")

        choice = input("\nChoose: ").strip().lower()

        if choice == "q":
            break
        elif choice == "r":
            continue
        elif choice == "b":
            parent = os.path.dirname(current)
            if current != start and os.path.commonpath([start, parent]) == start:
                current = parent
        elif choice == "n":
            name = input("New folder name: ").strip()
            if name and name not in (".", "..") and "/" not in name:
                try:
                    os.mkdir(os.path.join(current, name))
                    print("Folder created.")
                except OSError as e:
                    print("❌", e)
        elif choice in ("o", "m", "d", "c", "t"):
            if not items:
                print("No files or folders found.")
                continue
            try:
                n = int(input("File/folder number: "))
                if n < 1 or n > len(items):
                    raise ValueError
                source = os.path.join(current, items[n - 1])
            except ValueError:
                print("Invalid number.")
                continue

            if choice == "o":
                if os.path.isdir(source):
                    current = source
                else:
                    try:
                        subprocess.run(["termux-open", "--chooser", source])
                    except FileNotFoundError:
                        print("termux-open not found (install termux-api).")
            elif choice == "m":
                new = input("New name: ").strip()
                if new and "/" not in new and new not in (".", ".."):
                    try:
                        target = os.path.join(current, new)
                        if os.path.exists(target):
                            print("A file or folder with that name already exists.")
                        else:
                            os.rename(source, target)
                            print("Renamed.")
                    except OSError as e:
                        print("❌", e)
            elif choice == "d":
                confirm = input(f"Delete '{items[n - 1]}'? (yes/no): ").strip().lower()
                if confirm == "yes":
                    try:
                        if os.path.isdir(source) and not os.path.islink(source):
                            shutil.rmtree(source)
                        else:
                            os.remove(source)
                        print("Deleted.")
                    except OSError as e:
                        print("❌", e)
            elif choice == "c":
                clipboard, operation = source, "copy"
                print("Copy source selected.")
            elif choice == "t":
                clipboard, operation = source, "move"
                print("Move source selected.")
        elif choice == "v":
            if not clipboard or not os.path.exists(clipboard):
                print("Select a file or folder with C or T first.")
                continue
            if os.path.isdir(clipboard) and os.path.realpath(current).startswith(
                    os.path.realpath(clipboard) + os.sep):
                print("A folder cannot be pasted inside itself.")
                continue
            target = os.path.join(current, os.path.basename(clipboard))
            if os.path.exists(target):
                print("A file or folder with that name already exists here.")
                continue
            try:
                if operation == "copy":
                    if os.path.isdir(clipboard):
                        shutil.copytree(clipboard, target)
                    else:
                        shutil.copy2(clipboard, target)
                    print("Copied.")
                else:
                    shutil.move(clipboard, target)
                    print("Moved.")
                    clipboard = None
            except OSError as e:
                print("Operation failed:", e)
        else:
            print("Invalid option.")

    print("Goodbye.")


# ======================================================================
# 7. GALLERY
# ======================================================================
def gallery_tool():
    gallery_dir = CAMERA_DIR  # same folder the Camera tool saves into

    def get_photos():
        gallery_dir.mkdir(parents=True, exist_ok=True)
        return sorted(
            [f for f in os.listdir(gallery_dir)
             if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))],
            reverse=True,
        )

    while True:
        photos = get_photos()

        print("\n================================")
        print("           GALLERY")
        print("================================")

        if not photos:
            print(" No photos found.")
        else:
            for i, photo in enumerate(photos, 1):
                print(f"{i}. 🖼️ {photo}")

        print("\nO.  Open Gallery Folder")
        print("R.  Refresh")
        print("Q.  Exit")

        choice = input("\nChoose: ").strip().lower()

        if choice == "q":
            print("Goodbye.")
            break
        elif choice == "r":
            continue
        elif choice == "o":
            try:
                subprocess.run(["termux-open", "--chooser", str(gallery_dir)])
            except FileNotFoundError:
                print("termux-open not found (install termux-api).")
        elif choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(photos):
                path = str(gallery_dir / photos[number - 1])
                try:
                    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
                    subprocess.run(["termux-open", "--chooser",
                                    "--content-type", mime, path], check=False)
                except Exception as e:
                    print("Could not open image:", e)
            else:
                print("Invalid photo number.")
        else:
            print("Invalid option.")


# ======================================================================
# 8. NOTEPAD PRO
# ======================================================================
NOTES_DIR = SHARED / "Documents" / "TermuxNotes"


def notes_list():
    return sorted(NOTES_DIR.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)


def notes_choose():
    notes = notes_list()
    if not notes:
        print("No saved notes found.")
        return None

    for i, note in enumerate(notes, 1):
        print(f"{i}. {note.stem}")

    choice = input("\nEnter note number (B = Back): ").strip().lower()
    if choice == "b":
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(notes):
        return notes[int(choice) - 1]

    print("Invalid selection.")
    return None


def notes_editor(original):
    os.environ.setdefault("ESCDELAY", "25")  # make Esc respond quickly
    import curses

    lines = original.split("\n") or [""]
    y, x, top = 0, 0, 0

    def editor(stdscr):
        nonlocal y, x, top
        curses.raw()
        curses.noecho()
        stdscr.keypad(True)
        stdscr.timeout(-1)

        while True:
            stdscr.erase()
            h, w = stdscr.getmaxyx()

            try:
                stdscr.addstr(0, 0, "PYTHON NOTE EDITOR - Ctrl+S Save | Esc Cancel"[:w - 1])
                for i in range(1, h - 1):
                    idx = top + i - 1
                    if idx < len(lines):
                        stdscr.addstr(i, 0, lines[idx][:w - 1])
                stdscr.addstr(h - 1, 0, "Arrows: Move | Enter: New line | Backspace: Delete"[:w - 1])
                stdscr.move(min(y - top + 1, h - 2), min(x, w - 1))
            except curses.error:
                pass

            stdscr.refresh()
            key = stdscr.getch()

            if key == 19:  # Ctrl+S
                return "\n".join(lines)
            if key == 27:  # Esc
                return None
            if key == curses.KEY_UP:
                y = max(0, y - 1)
                x = min(x, len(lines[y]))
            elif key == curses.KEY_DOWN:
                y = min(len(lines) - 1, y + 1)
                x = min(x, len(lines[y]))
            elif key == curses.KEY_LEFT:
                if x > 0:
                    x -= 1
                elif y > 0:
                    y -= 1
                    x = len(lines[y])
            elif key == curses.KEY_RIGHT:
                if x < len(lines[y]):
                    x += 1
                elif y < len(lines) - 1:
                    y += 1
                    x = 0
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if x > 0:
                    lines[y] = lines[y][:x - 1] + lines[y][x:]
                    x -= 1
                elif y > 0:
                    x = len(lines[y - 1])
                    lines[y - 1] += lines[y]
                    del lines[y]
                    y -= 1
            elif key in (10, 13, curses.KEY_ENTER):
                before, after = lines[y][:x], lines[y][x:]
                lines[y:y + 1] = [before, after]
                y += 1
                x = 0
            elif 32 <= key <= 126:
                lines[y] = lines[y][:x] + chr(key) + lines[y][x:]
                x += 1

            h, _ = stdscr.getmaxyx()
            if y < top:
                top = y
            elif y >= top + h - 2:
                top = y - h + 3

    return curses.wrapper(editor)


def notes_new():
    title = input("Enter note title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    title = "".join(c for c in title if c not in r'\/:*?"<>|')[:100]
    if not title:
        print("Title has no valid characters.")
        return
    note = NOTES_DIR / (title + ".txt")

    if note.exists():
        print("A note with this title already exists.")
        if input("Overwrite it? (Y/N): ").strip().lower() != "y":
            print("Cancelled.")
            return

    print("Opening built-in Python editor...")
    print("Arrow keys = Move | Ctrl+S = Save | Esc = Cancel")
    input("Press Enter to start editing...")

    content = notes_editor("")
    if content is None:
        print("Note creation cancelled.")
        return

    note.write_text(content, encoding="utf-8")
    print("Note saved successfully!")


def notes_view():
    notes = notes_list()
    if not notes:
        print("No saved notes found.")
        return

    for i, note in enumerate(notes, 1):
        print(f"{i}. {note.stem}")

    choice = input("\nEnter note number (B = Back): ").strip().lower()
    if choice == "b":
        return

    if choice.isdigit() and 1 <= int(choice) <= len(notes):
        note = notes[int(choice) - 1]
        print("\n" + "=" * 35)
        print(note.stem)
        print("=" * 35)
        print(note.read_text(encoding="utf-8"))
    else:
        print("Invalid selection.")


def notes_edit():
    note = notes_choose()
    if not note:
        return

    original = note.read_text(encoding="utf-8")
    print("Opening built-in Python editor...")
    print("Arrow keys = Move | Ctrl+S = Save | Esc = Cancel")
    input("Press Enter to start editing...")

    updated = notes_editor(original)
    if updated is None:
        print("Editing cancelled. Original note preserved.")
        return
    if updated == original:
        print("No changes made.")
        return

    note.write_text(updated, encoding="utf-8")
    print("Note saved successfully!")


def notes_delete():
    note = notes_choose()
    if not note:
        return

    answer = input(f"Delete '{note.stem}'? (Y/N): ").strip().lower()
    if answer == "y":
        note.unlink()
        print("Note deleted.")
    elif answer == "n":
        print("Deletion cancelled.")
    else:
        print("Invalid choice. Nothing deleted.")


def notes_search():
    query = input("Enter text to search: ").strip()
    if not query:
        print("Search query cannot be empty.")
        return

    matches = []
    query = query.casefold()
    for note in notes_list():
        try:
            if query in note.read_text(encoding="utf-8").casefold():
                matches.append(note)
        except (OSError, UnicodeError):
            continue

    print("\nMatching notes (maximum 5):")
    print("-" * 35)

    if not matches:
        print("No matching notes found.")
        return

    for i, note in enumerate(matches[:5], 1):
        print(f"{i}. {note.stem}")

    print("-" * 35)
    print(f"Showing {min(len(matches), 5)} of {len(matches)} matching notes.")


def notes_tool():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        clear()
        print("=" * 38)
        print("             NOTEPAD PRO")
        print("=" * 38)
        print("1. Create a New Note")
        print("2. View Saved Notes")
        print("3. Edit a Note")
        print("4. Delete a Note")
        print("5. Search Notes")
        print("6. Exit")
        print("-" * 38)

        choice = input("Select an option: ").strip()

        if choice == "1":
            notes_new()
        elif choice == "2":
            notes_view()
        elif choice == "3":
            notes_edit()
        elif choice == "4":
            notes_delete()
        elif choice == "5":
            notes_search()
        elif choice == "6":
            print("Thank you for using Notepad Pro!")
            break
        else:
            print("Invalid option.")
        pause()


# ======================================================================
# 9. SMS TOOL
# ======================================================================
def sms_send():
    number = input("Phone number: ").strip()
    message = input("Message: ")
    if not number or not message:
        print("Phone number and message are required.")
        return
    try:
        subprocess.run(["termux-sms-send", "-n", number, message], check=True)
        print("SMS sent.")
    except Exception as e:
        print("SMS send failed:", e)


def sms_read():
    try:
        result = subprocess.run(["termux-sms-list", "-l", "5"],
                                capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            print("Could not read SMS messages.")
            return
        if not result.stdout.strip():
            print("No SMS messages found.")
            return

        messages = json.loads(result.stdout)
        print("\n========== LATEST 5 SMS ==========\n")
        for i, sms in enumerate(messages, 1):
            print(f"📩 SMS {i}")
            print("📱 Number :", sms.get("number", "Unknown"))
            print("📨 Type   :", sms.get("type", "Unknown"))
            print("💬 Message:", sms.get("body", ""))
            print("Date   :", sms.get("received", ""))
            print("----------------------------------")
    except subprocess.TimeoutExpired:
        print("SMS reading timed out.")
    except json.JSONDecodeError:
        print("Could not parse SMS data.")
    except Exception as e:
        print("Error:", e)


def sms_tool():
    while True:
        print("\n==========================")
        print("        SMS TOOL")
        print("==========================")
        print("1.  Send SMS")
        print("2.  Read SMS")
        print("3.  Exit")

        choice = input("\nChoose: ").strip()
        if choice == "1":
            sms_send()
        elif choice == "2":
            sms_read()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


# ======================================================================
# 10. MUSIC PLAYER
# ======================================================================
MUSIC_FORMATS = (".mp3", ".m4a", ".aac", ".wav", ".ogg", ".flac", ".opus")


class MusicPlayer:
    def __init__(self):
        self.start = str(SHARED)
        self.folder = self.start
        self.socket_path = os.path.join(
            os.environ.get("TMPDIR", "/tmp"), "music-player.sock")
        self.player = None
        self.ipc = None
        self.songs = []
        self.current = 0

    def command(self, cmd):
        if not self.ipc:
            return
        try:
            self.ipc.sendall((json.dumps({"command": cmd}) + "\n").encode())
            self.ipc.recv(4096)
        except Exception:
            print("Player command failed.")

    def stop(self):
        if self.ipc:
            try:
                self.ipc.close()
            except Exception:
                pass
            self.ipc = None
        if self.player and self.player.poll() is None:
            self.player.terminate()
            try:
                self.player.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.player.kill()
        self.player = None
        try:
            os.remove(self.socket_path)
        except OSError:
            pass

    def play(self, index):
        if not self.songs:
            print("No music files found in this folder.")
            return
        self.current = index % len(self.songs)
        self.stop()
        try:
            self.player = subprocess.Popen(
                ["mpv", "--no-video", "--input-ipc-server=" + self.socket_path,
                 self.songs[self.current]],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            self.player = None
            print("Could not start MPV. Install it with: pkg install mpv")
            return
        except Exception as e:
            print("Playback error:", e)
            return

        for _ in range(30):
            if self.player.poll() is not None:
                print("Could not start MPV. Install it with: pkg install mpv")
                self.player = None
                return
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                sock.connect(self.socket_path)
                self.ipc = sock
                break
            except OSError:
                sock.close()
                time.sleep(0.1)
        else:
            self.stop()
            print("Could not connect to the player.")
            return
        print("Playing:", os.path.basename(self.songs[self.current]))

    def scan(self):
        try:
            self.songs = sorted(
                os.path.join(self.folder, n)
                for n in os.listdir(self.folder)
                if os.path.isfile(os.path.join(self.folder, n))
                and n.lower().endswith(MUSIC_FORMATS)
            )
        except OSError:
            self.songs = []

    def run(self):
        os.makedirs(self.start, exist_ok=True)

        while True:
            print("\n==========  MUSIC PLAYER ==========")
            print("📂 Folder:", self.folder)
            self.scan()

            for i, path in enumerate(self.songs, 1):
                print(f"{i}. 🎵 {os.path.basename(path)}")

            print("""
[F] Browse folders
[O] Open folder / select music
[S] Play selected song
[A] Pause / Resume
[N] Next
[P] Previous
[V] Volume
[B] Back
[R] Refresh
[Q] Quit
""")
            choice = input("Choose: ").strip().lower()

            if choice == "q":
                self.stop()
                break
            elif choice == "r":
                continue
            elif choice == "f":
                try:
                    entries = sorted(os.listdir(self.folder))
                    dirs = [x for x in entries if os.path.isdir(os.path.join(self.folder, x))]
                    for i, name in enumerate(dirs, 1):
                        print(f"{i}. 📁 {name}")
                    if dirs:
                        n = input("Folder number (Enter to cancel): ").strip()
                        if n.isdigit() and 1 <= int(n) <= len(dirs):
                            self.folder = os.path.join(self.folder, dirs[int(n) - 1])
                except OSError as e:
                    print("Folder error:", e)
            elif choice == "o":
                try:
                    entries = sorted(os.listdir(self.folder))
                    dirs = [x for x in entries if os.path.isdir(os.path.join(self.folder, x))]
                    files = [x for x in entries if os.path.isfile(os.path.join(self.folder, x))]
                    print("Folders:")
                    for i, name in enumerate(dirs, 1):
                        print(f"D{i}. 📁 {name}")
                    print("Music files:")
                    music_files = [x for x in files if x.lower().endswith(MUSIC_FORMATS)]
                    for i, name in enumerate(music_files, 1):
                        print(f"F{i}. 🎵 {name}")
                    sel = input("Enter D<number> for folder or F<number> for song: ").strip().lower()
                    if sel.startswith("d") and sel[1:].isdigit():
                        n = int(sel[1:])
                        if 1 <= n <= len(dirs):
                            self.folder = os.path.join(self.folder, dirs[n - 1])
                    elif sel.startswith("f") and sel[1:].isdigit():
                        n = int(sel[1:])
                        if 1 <= n <= len(music_files):
                            self.songs = [os.path.join(self.folder, x) for x in music_files]
                            self.play(n - 1)
                except OSError as e:
                    print("Folder error:", e)
            elif choice == "s":
                n = input("Song number: ").strip()
                if n.isdigit() and 1 <= int(n) <= len(self.songs):
                    self.play(int(n) - 1)
                else:
                    print("Invalid song number.")
            elif choice == "a":
                self.command(["cycle", "pause"])
            elif choice == "n" and self.songs:
                self.play(self.current + 1)
            elif choice == "p" and self.songs:
                self.play(self.current - 1)
            elif choice == "v":
                n = input("Volume 0-100: ").strip()
                if n.isdigit():
                    self.command(["set_property", "volume", max(0, min(100, int(n)))])
            elif choice == "b":
                parent = os.path.dirname(self.folder)
                if os.path.commonpath([self.start, parent]) == self.start:
                    self.folder = parent
            else:
                print("Invalid option.")

        print("Goodbye.")


def music_tool():
    MusicPlayer().run()


# ======================================================================
# LAUNCHER
# ======================================================================
TOOLS = [
    ("CLI Browser", browser_tool),
    ("Phone Call", call_tool),
    ("Camera", camera_tool),
    ("Social Media Downloader", downloader_tool),
    ("Email Tool", email_tool),
    ("File Manager", filemanager_tool),
    ("Gallery", gallery_tool),
    ("Notepad Pro", notes_tool),
    ("SMS Tool", sms_tool),
    ("Music Player", music_tool),
]


def main():
    while True:
        banner()
        for i, (name, _) in enumerate(TOOLS, 1):
            print(f"  {paint(f'{i:2}.', Style.YELLOW)} {name}")
        print()
        print(f"  {paint('H.', Style.PURPLE)} Help & Quick Start")
        print(f"  {paint('0.', Style.RED)} Exit")
        print(paint("─" * 52, Style.DIM))

        choice = input(paint("Select an option [0-10/H]: ", Style.CYAN)).strip().lower()
        if choice == "0":
            print(paint("\nThanks for using Universal Termux Toolkit!", Style.GREEN))
            print(paint("Created by Itachi • YouTube: Termux Bird • Stay curious. Stay safe.", Style.PURPLE))
            return
        if choice in ("h", "help", "?"):
            help_tool()
            continue
        if not choice.isdigit() or not 1 <= int(choice) <= len(TOOLS):
            print(paint("Invalid selection. Choose 0-10 or H for help.", Style.RED))
            pause("\nPress Enter to continue...")
            continue

        name, func = TOOLS[int(choice) - 1]
        try:
            func()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{name} stopped.")
        except Exception as exc:
            print(f"{name} encountered an error: {exc}")
        pause("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        help_tool(pause_after=False)
        raise SystemExit(0)
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nToolkit closed.")
