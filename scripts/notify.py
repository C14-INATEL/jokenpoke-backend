import os
import sys
import smtplib
from email.mime.text import MIMEText
 
if len(sys.argv) < 2 or sys.argv[1].upper() not in ("SUCCESS", "FAILURE", "UNSTABLE"):
    print("Uso: python3 notify.py SUCCESS|FAILURE|UNSTABLE", file=sys.stderr)
    sys.exit(1)
 
STATUS = sys.argv[1].upper()
 
TO       = os.environ["PIPELINE_NOTIFY_EMAIL"]
SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASSWORD"]
 
JOB      = os.environ.get("JOB_NAME",    "jokenpoke-backend")
BUILD    = os.environ.get("BUILD_NUMBER", "?")
URL      = os.environ.get("BUILD_URL",    "#")
BRANCH   = os.environ.get("BRANCH_NAME",  os.environ.get("GIT_BRANCH", "local"))
COMMIT   = os.environ.get("GIT_COMMIT",   "unknown")
DURATION = os.environ.get("BUILD_DURATION_STRING", "N/A")
 
ICONS = {"SUCCESS": "✅", "FAILURE": "❌", "UNSTABLE": "⚠️"}
icon  = ICONS[STATUS]
 
subject = f"[Jenkins] {icon} {STATUS} — {JOB} #{BUILD}"
 
body = f"""\
Pipeline {STATUS}
 
Job:     {JOB}
Build:   #{BUILD}
Branch:  {BRANCH}
Commit:  {COMMIT}
Duração: {DURATION}
 
{URL}
"""
 
msg            = MIMEText(body, "plain", "utf-8")
msg["Subject"] = subject
msg["From"]    = SMTP_USER
msg["To"]      = TO
 
with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
    s.starttls()
    s.login(SMTP_USER, SMTP_PASS)
    s.sendmail(SMTP_USER, TO.split(","), msg.as_string())
 
print(f"[notify.py] E-mail enviado → {TO}")