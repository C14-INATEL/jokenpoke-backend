import os
import smtplib
import sys
from email.mime.text import MIMEText

STATUS = sys.argv[1].upper() if len(sys.argv) > 1 else "UNKNOWN"
if STATUS not in ("SUCCESS", "FAILURE", "UNSTABLE"):
    print("Uso: python3 notify.py SUCCESS|FAILURE|UNSTABLE", file=sys.stderr)
    sys.exit(1)

TO = os.environ.get("PIPELINE_NOTIFY_EMAIL", "").strip()
SMTP_HOST = os.environ.get("SMTP_HOST", "").strip()
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "").strip()
SMTP_PASS = os.environ.get("SMTP_PASSWORD", "").strip()

for name, val in [
    ("PIPELINE_NOTIFY_EMAIL", TO),
    ("SMTP_HOST", SMTP_HOST),
    ("SMTP_USER", SMTP_USER),
    ("SMTP_PASSWORD", SMTP_PASS),
]:
    if not val:
        print(f"ERRO: variável {name} não definida.", file=sys.stderr)
        sys.exit(1)

JOB = os.environ.get("JOB_NAME", "jokenpoke-backend")
BUILD = os.environ.get("BUILD_NUMBER", "?")
URL = os.environ.get("BUILD_URL", "#")
BRANCH = os.environ.get("BRANCH_NAME", os.environ.get("GIT_BRANCH", "local"))
COMMIT = os.environ.get("GIT_COMMIT", "unknown")

ICONS = {"SUCCESS": "✅", "FAILURE": "❌", "UNSTABLE": "⚠️"}

subject = f"[Jenkins] {ICONS[STATUS]} {STATUS} — {JOB} #{BUILD}"

body = f"""\
Pipeline {STATUS}
 
Job:    {JOB}
Build:  #{BUILD}
Branch: {BRANCH}
Commit: {COMMIT}
URL:    {URL}
"""

msg = MIMEText(body, "plain", "utf-8")
msg["Subject"] = subject
msg["From"] = SMTP_USER
msg["To"] = TO

with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
    s.starttls()
    s.login(SMTP_USER, SMTP_PASS)
    s.sendmail(SMTP_USER, TO.split(","), msg.as_string())

print(f"[notify.py] E-mail enviado → {TO}")
