#!/data/data/com.termux/files/usr/bin/bash

set -u

echo "======================================"
echo " Universal Termux Toolkit | Itachi Edition"
echo "======================================"

if [ -z "${PREFIX:-}" ] || [ ! -d "$PREFIX" ]; then
    echo "Error: Run this script inside Termux."
    exit 1
fi

echo
echo "[1/4] Updating package lists..."
pkg update -y || {
    echo "Package update failed. Check your internet/repositories and try again."
    exit 1
}

echo
echo "[2/4] Installing Termux packages..."
pkg install -y python termux-api links mpv ffmpeg unzip || {
    echo "Some Termux packages could not be installed."
    exit 1
}

echo
echo "[3/4] Installing Python downloader requirement..."
if ! python -m pip install --upgrade "yt-dlp[default]"; then
    echo "Full install failed (some optional extras may need compiling). Trying basic yt-dlp..."
    python -m pip install --upgrade yt-dlp || {
        echo "yt-dlp installation failed. Check your internet connection and try again."
        exit 1
    }
fi

echo
echo "[4/4] Requesting shared-storage permission..."
termux-setup-storage

echo
echo "======================================"
echo " Setup steps completed."
echo "======================================"
echo "Important:"
echo "1. Install the separate Termux:API Android app from the same trusted source as Termux."
echo "2. Allow camera, phone and SMS permissions when Android asks."
echo "3. To start the toolkit, enter its folder and run:"
echo "   python toolkit.py"
echo
echo "If storage folders do not appear, approve the Android storage permission prompt,"
echo "then close and reopen Termux."

echo "Credits: Itachi | YouTube: Termux Bird (https://youtube.com/@termuxbird)"
echo "Run: python toolkit.py --help for the quick-start guide."
