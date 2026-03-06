# """
# run_with_ngrok.py  —  calls ngrok.exe directly, auto-detects Streamlit port
# """

# import sys
# import os
# import time
# import subprocess
# import threading
# import json
# import urllib.request
# import socket

# APP_FILE   = "b.py"
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# NGROK_EXE  = os.path.join(SCRIPT_DIR, "ngrok.exe")

# print("=" * 55)
# print("  📚 Book Order System — ngrok Launcher")
# print("=" * 55)

# # ── Checks ─────────────────────────────────────────────────────────────────────
# if not os.path.exists(APP_FILE):
#     print(f"\n❌ '{APP_FILE}' not found in: {SCRIPT_DIR}")
#     sys.exit(1)

# if not os.path.exists(NGROK_EXE):
#     print(f"\n❌ ngrok.exe not found in: {SCRIPT_DIR}")
#     print("   Download from: https://ngrok.com/download")
#     sys.exit(1)

# # ── Find a free port ────────────────────────────────────────────────────────────
# def find_free_port():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("", 0))
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         return s.getsockname()[1]

# PORT = find_free_port()
# print(f"\n✅ Found free port: {PORT}")

# # ── Start Streamlit on that exact port ─────────────────────────────────────────
# def start_streamlit():
#     subprocess.run(
#         [
#             sys.executable, "-m", "streamlit", "run", APP_FILE,
#             "--server.port", str(PORT),
#             "--server.headless", "true",
#             "--server.enableCORS", "false",
#             "--server.enableXsrfProtection", "false",
#             "--server.address", "localhost",
#         ],
#         cwd=SCRIPT_DIR
#     )

# print(f"⏳ Starting Streamlit on port {PORT}...")
# t = threading.Thread(target=start_streamlit, daemon=True)
# t.start()

# # Wait until Streamlit is actually accepting connections
# print("⏳ Waiting for Streamlit to be ready...")
# for _ in range(30):
#     time.sleep(1)
#     try:
#         with socket.create_connection(("localhost", PORT), timeout=1):
#             print(f"✅ Streamlit is ready on port {PORT}")
#             break
#     except OSError:
#         pass
# else:
#     print("❌ Streamlit did not start in time.")
#     sys.exit(1)

# # ── Kill any existing ngrok ─────────────────────────────────────────────────────
# subprocess.run(["taskkill", "/f", "/im", "ngrok.exe"],
#                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# time.sleep(1)

# # ── Start ngrok.exe on the CORRECT port ────────────────────────────────────────
# print("⏳ Starting ngrok tunnel...")
# ngrok_proc = subprocess.Popen(
#     [NGROK_EXE, "http", str(PORT)],
#     stdout=subprocess.DEVNULL,
#     stderr=subprocess.DEVNULL,
#     cwd=SCRIPT_DIR
# )

# # Poll ngrok's local API for the public URL
# public_url = None
# for _ in range(20):
#     time.sleep(0.5)
#     try:
#         with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2) as r:
#             data    = json.loads(r.read())
#             tunnels = data.get("tunnels", [])
#             for tunnel in tunnels:
#                 if tunnel.get("proto") == "https":
#                     public_url = tunnel["public_url"]
#                     break
#             if public_url:
#                 break
#     except Exception:
#         pass

# if public_url:
#     print("\n" + "=" * 55)
#     print("  ✅  Your app is LIVE!")
#     print("=" * 55)
#     print(f"\n  🌐  Public URL :  {public_url}")
#     print(f"  💻  Local  URL :  http://localhost:{PORT}")
#     print("\n  Share the Public URL with anyone worldwide.")
#     print("\n  Press Ctrl+C to stop.")
#     print("=" * 55 + "\n")
# else:
#     print("\n❌ Could not get ngrok public URL.")
#     print("   Make sure auth token is set:")
#     print("   .\\ngrok.exe config add-authtoken YOUR_TOKEN")
#     ngrok_proc.terminate()
#     sys.exit(1)

# # ── Keep alive ─────────────────────────────────────────────────────────────────
# try:
#     while True:
#         time.sleep(1)
#         if ngrok_proc.poll() is not None:
#             print("\n⚠️  ngrok stopped unexpectedly.")
#             break
# except KeyboardInterrupt:
#     print("\n🛑 Shutting down...")
#     ngrok_proc.terminate()
#     print("✅ Stopped. Goodbye!")



"""
run_with_ngrok.py  —  Calls ngrok.exe directly, auto-finds a free port
"""

import sys, os, time, subprocess, threading, json, urllib.request, socket

APP_FILE   = "b.py"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NGROK_EXE  = os.path.join(SCRIPT_DIR, "ngrok.exe")

print("=" * 55)
print("  📚 Book Order System — ngrok Launcher")
print("=" * 55)

if not os.path.exists(APP_FILE):
    print(f"\n❌ '{APP_FILE}' not found in: {SCRIPT_DIR}")
    sys.exit(1)

if not os.path.exists(NGROK_EXE):
    print(f"\n❌ ngrok.exe not found in: {SCRIPT_DIR}")
    sys.exit(1)

# Find a free port automatically
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

PORT = find_free_port()
print(f"\n✅ Found free port: {PORT}")

# Start Streamlit on that exact port
def start_streamlit():
    subprocess.run(
        [
            sys.executable, "-m", "streamlit", "run", APP_FILE,
            "--server.port", str(PORT),
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--server.address", "0.0.0.0",
        ],
        cwd=SCRIPT_DIR
    )

print(f"⏳ Starting Streamlit on port {PORT}...")
t = threading.Thread(target=start_streamlit, daemon=True)
t.start()

# Wait until Streamlit is actually accepting connections
print("⏳ Waiting for Streamlit to be ready...")
for _ in range(30):
    time.sleep(1)
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=1):
            print(f"✅ Streamlit is ready!")
            break
    except OSError:
        pass
else:
    print("❌ Streamlit failed to start. Check b_updated.py for errors.")
    sys.exit(1)

# ── YOUR NGROK AUTH TOKEN (no setup needed) ────────────────────────────────────
NGROK_AUTH_TOKEN = "3AZPzlbMQFGto2beKJBvatMqGzW_2Xxb4JPoRirKtBEfhvUiW"

# Kill any stale ngrok process
subprocess.run(["taskkill", "/f", "/im", "ngrok.exe"], capture_output=True)
time.sleep(1)

# Set auth token directly via ngrok.exe (overwrites any bad config)
print("⏳ Setting ngrok auth token...")
result = subprocess.run(
    [NGROK_EXE, "config", "add-authtoken", NGROK_AUTH_TOKEN],
    capture_output=True, text=True, cwd=SCRIPT_DIR
)
if result.returncode == 0:
    print("✅ Auth token set successfully!")
else:
    print(f"⚠️  Token set warning: {result.stderr.strip()}")
time.sleep(1)

# Start ngrok pointing at the EXACT port Streamlit is on
print("⏳ Starting ngrok tunnel...")
ngrok_proc = subprocess.Popen(
    [NGROK_EXE, "http", str(PORT)],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=SCRIPT_DIR
)

# Poll ngrok local API for public URL
public_url = None
for _ in range(20):
    time.sleep(1)
    try:
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2) as r:
            data = json.loads(r.read())
            for tunnel in data.get("tunnels", []):
                if tunnel.get("proto") == "https":
                    public_url = tunnel["public_url"]
                    break
            if public_url:
                break
    except Exception:
        pass

if public_url:
    print("\n" + "=" * 55)
    print("  ✅  Your app is LIVE!")
    print("=" * 55)
    print(f"\n  🌐  Public URL :  {public_url}")
    print(f"  💻  Local  URL :  http://localhost:{PORT}")
    print("\n  Share the Public URL with anyone worldwide.")
    print("  Press Ctrl+C to stop.")
    print("=" * 55 + "\n")
else:
    print("\n❌ Could not get ngrok URL. Check auth token:")
    print("   .\\ngrok.exe config add-authtoken YOUR_TOKEN")
    ngrok_proc.terminate()
    sys.exit(1)

try:
    while True:
        time.sleep(1)
        if ngrok_proc.poll() is not None:
            print("\n⚠️  ngrok stopped unexpectedly.")
            break
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    ngrok_proc.terminate()
    print("✅ Stopped. Goodbye!")