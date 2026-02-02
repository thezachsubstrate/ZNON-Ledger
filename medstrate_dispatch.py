import smtplib
from email.message import EmailMessage
import getpass

# --- CREDENTIALS ---
SENDER = "medstrate.audit@gmail.com"
print("--- MEDSTRATE RESEARCH INSTITUTE: OUTREACH ENGINE ---")
PASS = getpass.getpass("Paste your 16-character App Password (it will be invisible): ")

# --- TARGETS ---
TARGETS = [
    {"name": "Doctronic AI", "email": "contact@doctronic.ai"},
    {"name": "UCB Medical Liaison", "email": "ucbcares@ucb.com"}
]

def dispatch():
    for target in TARGETS:
        msg = EmailMessage()
        msg['From'] = f"MedStrate Research Institute <{SENDER}>"
        msg['To'] = target['email']
        msg['Subject'] = "9-Sigma Forensic Audit: Protocol Integration & Efficacy"
        
        msg.set_content(f"To the Technical/Medical Director at {target['name']},\n\n"
                        f"The MedStrate Research Institute has codified 9-Sigma physical signatures "
                        f"associated with IL-17A responsive pathologies. We are offering licensing for "
                        f"this logic to assist in clinical implementation and AI platform integration.\n\n"
                        f"REPOSITORY: https://github.com/thezachsubstrate/Substrate-Mac-Forge\n"
                        f"SETTLEMENT: 0xA483A6167A86e8dB66d61e2e5069B161BFD6FfE5\n\n"
                        f"Regards,\nLead Auditor\nMedStrate Research Institute")
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SENDER, PASS)
                smtp.send_message(msg)
                print(f"✅ MISSION DISPATCHED TO: {target['name']}")
        except Exception as e:
            print(f"❌ FAILED: {target['name']} - {e}")

if __name__ == "__main__":
    dispatch()
