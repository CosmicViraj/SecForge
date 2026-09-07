import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import secrets
import string
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime

APP_NAME = "CyberLab Suite"

class CyberLabSuite:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("980x650")
        self.root.minsize(900, 600)

        self.make_ui()

    def make_ui(self):
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=18, pady=(15, 8))

        ttk.Label(header, text=APP_NAME, font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Safe cybersecurity learning toolkit for authorized testing and portfolio demonstrations.",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 0))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=10)

        self.add_key_demo()
        self.add_port_scanner()
        self.add_vuln_checker()
        self.add_packet_analyzer()
        self.add_password_generator()
        self.add_wifi_viewer()
        self.add_nfc_simulator()
        self.add_email_simulator()
        self.add_hash_tool()

        footer = ttk.Label(
            self.root,
            text="Use only on systems and networks you own or have explicit permission to test.",
            font=("Segoe UI", 9, "italic")
        )
        footer.pack(pady=(0, 10))

    def new_tab(self, title):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=title)
        return frame

    # 1. Safe keystroke demo
    def add_key_demo(self):
        tab = self.new_tab("Key Event Demo")
        ttk.Label(tab, text="Keystroke Event Visualizer", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(
            tab,
            text="Captures keys only while this box is focused. Nothing is stored or captured globally."
        ).pack()

        self.key_box = tk.Text(tab, height=12, width=80, font=("Consolas", 11))
        self.key_box.pack(padx=20, pady=20, fill="both", expand=True)
        self.key_box.insert("end", "Click here and type to visualize key events...\n\n")
        self.key_box.bind("<KeyPress>", self.show_key_event)

        self.key_status = ttk.Label(tab, text="Waiting for local key events...")
        self.key_status.pack(pady=(0, 15))

    def show_key_event(self, event):
        self.key_status.config(text=f"Key: {event.keysym} | Keycode: {event.keycode}")

    # 2. Authorized port scanner
    def add_port_scanner(self):
        tab = self.new_tab("Port Scanner")
        ttk.Label(tab, text="Authorized Port Scanner", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(tab, text="Default target is localhost. Scan only systems you are authorized to test.").pack()

        form = ttk.Frame(tab)
        form.pack(pady=15)

        ttk.Label(form, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.host_entry = ttk.Entry(form, width=30)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Ports (e.g. 22,80,443):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ports_entry = ttk.Entry(form, width=30)
        self.ports_entry.insert(0, "22,80,443,3000,5000,8000")
        self.ports_entry.grid(row=1, column=1, padx=5)

        ttk.Button(form, text="Scan", command=self.scan_ports).grid(row=2, column=0, columnspan=2, pady=10)

        self.port_output = tk.Text(tab, height=18, font=("Consolas", 10))
        self.port_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def scan_ports(self):
        host = self.host_entry.get().strip()
        try:
            socket.gethostbyname(host)
        except Exception:
            messagebox.showerror("Invalid Host", "Could not resolve that host.")
            return

        try:
            ports = sorted(set(int(p.strip()) for p in self.ports_entry.get().split(",") if p.strip()))
            if not ports or any(p < 1 or p > 65535 for p in ports) or len(ports) > 50:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid Ports", "Enter up to 50 valid ports separated by commas.")
            return

        self.port_output.delete("1.0", "end")
        self.port_output.insert("end", f"Scanning {host}\n{'-'*50}\n")

        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.25)
            try:
                result = sock.connect_ex((host, port))
                status = "OPEN" if result == 0 else "closed"
                self.port_output.insert("end", f"{port:5}  {status}\n")
            except Exception as exc:
                self.port_output.insert("end", f"{port:5}  error: {exc}\n")
            finally:
                sock.close()

    # 3. Safe vulnerability checker
    def add_vuln_checker(self):
        tab = self.new_tab("Security Checks")
        ttk.Label(tab, text="Local Security Configuration Checks", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(tab, text="Performs non-exploitative checks on this computer.").pack()

        ttk.Button(tab, text="Run Checks", command=self.run_local_checks).pack(pady=15)

        self.vuln_output = tk.Text(tab, font=("Consolas", 10))
        self.vuln_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def run_local_checks(self):
        out = []
        out.append(f"OS: {platform.platform()}")
        out.append(f"Python: {platform.python_version()}")
        out.append("")

        # Basic local checks only
        if os.name == "nt":
            try:
                r = subprocess.run(
                    ["netsh", "advfirewall", "show", "allprofiles", "state"],
                    capture_output=True, text=True, timeout=5
                )
                out.append("Windows Firewall:")
                out.append(r.stdout.strip()[:1500] or "Unable to read firewall state.")
            except Exception as exc:
                out.append(f"Firewall check unavailable: {exc}")
        else:
            out.append("Firewall check: Windows-specific check skipped.")

        out.append("")
        out.append("Recommendations:")
        out.append("- Keep the OS and applications updated.")
        out.append("- Keep the firewall enabled.")
        out.append("- Avoid running daily applications as administrator.")
        out.append("- Use unique passwords and MFA where available.")

        self.vuln_output.delete("1.0", "end")
        self.vuln_output.insert("end", "\n".join(out))

    # 4. Packet/PCAP analyzer
    def add_packet_analyzer(self):
        tab = self.new_tab("Packet Analyzer")
        ttk.Label(tab, text="PCAP Metadata Analyzer", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(
            tab,
            text="Analyzes an existing .pcap/.pcapng file. It does not capture live traffic."
        ).pack()
        ttk.Button(tab, text="Select PCAP File", command=self.analyze_pcap).pack(pady=15)

        self.pcap_output = tk.Text(tab, font=("Consolas", 10))
        self.pcap_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def analyze_pcap(self):
        path = filedialog.askopenfilename(
            filetypes=[("PCAP files", "*.pcap *.pcapng"), ("All files", "*.*")]
        )
        if not path:
            return

        size = os.path.getsize(path)
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                sha256.update(block)

        self.pcap_output.delete("1.0", "end")
        self.pcap_output.insert(
            "end",
            f"File: {path}\n"
            f"Size: {size:,} bytes\n"
            f"SHA-256: {sha256.hexdigest()}\n\n"
            "Tip: Open the PCAP in Wireshark for protocol-level packet analysis.\n"
        )

    # 5. Password generator
    def add_password_generator(self):
        tab = self.new_tab("Password Generator")
        ttk.Label(tab, text="Secure Password Generator", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))

        row = ttk.Frame(tab)
        row.pack(pady=15)

        ttk.Label(row, text="Length:").pack(side="left", padx=5)
        self.pw_len = tk.IntVar(value=20)
        ttk.Spinbox(row, from_=8, to=64, textvariable=self.pw_len, width=8).pack(side="left", padx=5)
        ttk.Button(row, text="Generate", command=self.generate_password).pack(side="left", padx=10)

        self.password_value = tk.StringVar()
        ttk.Entry(tab, textvariable=self.password_value, font=("Consolas", 14), width=55).pack(pady=12)

        ttk.Label(tab, text="Generated locally using Python's secrets module.").pack()

    def generate_password(self):
        length = max(8, min(64, int(self.pw_len.get())))
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        self.password_value.set("".join(secrets.choice(alphabet) for _ in range(length)))

    # 6. Wi-Fi viewer
    def add_wifi_viewer(self):
        tab = self.new_tab("Wi-Fi Viewer")
        ttk.Label(tab, text="Wi-Fi Network Viewer", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(tab, text="Shows nearby Wi-Fi network information without extracting saved passwords.").pack()
        ttk.Button(tab, text="Scan Nearby Wi-Fi", command=self.scan_wifi).pack(pady=15)

        self.wifi_output = tk.Text(tab, font=("Consolas", 10))
        self.wifi_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def scan_wifi(self):
        self.wifi_output.delete("1.0", "end")
        if os.name != "nt":
            self.wifi_output.insert("end", "This demo currently supports Windows netsh output.")
            return
        try:
            r = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                capture_output=True, text=True, timeout=10
            )
            self.wifi_output.insert("end", r.stdout or r.stderr or "No data returned.")
        except Exception as exc:
            self.wifi_output.insert("end", f"Wi-Fi scan unavailable: {exc}")

    # 7. NFC simulator
    def add_nfc_simulator(self):
        tab = self.new_tab("NFC Simulator")
        ttk.Label(tab, text="NFC Tag Simulator", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(tab, text="Educational simulator only — no NFC cracking or unauthorized access.").pack()

        ttk.Label(tab, text="Simulated NFC payload:").pack(pady=(20, 5))
        self.nfc_input = ttk.Entry(tab, width=60)
        self.nfc_input.insert(0, "https://example.com")
        self.nfc_input.pack()

        ttk.Button(tab, text="Generate Simulated Tag", command=self.make_nfc_demo).pack(pady=15)
        self.nfc_output = tk.Text(tab, height=12, font=("Consolas", 10))
        self.nfc_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def make_nfc_demo(self):
        payload = self.nfc_input.get()
        tag = {
            "type": "NDEF-SIMULATED",
            "payload": payload,
            "created": datetime.now().isoformat(timespec="seconds"),
            "digest": hashlib.sha256(payload.encode()).hexdigest()[:24]
        }
        self.nfc_output.delete("1.0", "end")
        self.nfc_output.insert("end", json.dumps(tag, indent=2))

    # 8. Email spoofing awareness simulator
    def add_email_simulator(self):
        tab = self.new_tab("Email Simulator")
        ttk.Label(tab, text="Email Header / Spoofing Awareness Simulator", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(tab, text="Demonstrates how display names and headers can mislead users. It does not send email.").pack()

        form = ttk.Frame(tab)
        form.pack(pady=15)

        self.email_name = ttk.Entry(form, width=35)
        self.email_name.insert(0, "IT Support")
        self.email_addr = ttk.Entry(form, width=35)
        self.email_addr.insert(0, "support@example.test")

        ttk.Label(form, text="Display name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.email_name.grid(row=0, column=1, padx=5)
        ttk.Label(form, text="From address:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.email_addr.grid(row=1, column=1, padx=5)

        ttk.Button(form, text="Generate Demo Headers", command=self.generate_email_demo).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        self.email_output = tk.Text(tab, font=("Consolas", 10))
        self.email_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def generate_email_demo(self):
        name = self.email_name.get().strip() or "Example Sender"
        addr = self.email_addr.get().strip() or "sender@example.test"

        text = (
            f"From: {name} <{addr}>\n"
            f"Reply-To: reply@example.test\n"
            f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S')}\n"
            f"Authentication-Results: simulated; SPF=example; DKIM=example; DMARC=example\n\n"
            "Awareness note:\n"
            "The visible display name is not proof of sender identity. Verify the actual address\n"
            "and authentication results before trusting sensitive requests."
        )
        self.email_output.delete("1.0", "end")
        self.email_output.insert("end", text)

    # 9. Hash utility
    def add_hash_tool(self):
        tab = self.new_tab("Hash Utility")
        ttk.Label(tab, text="File Hash Calculator", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Button(tab, text="Select File", command=self.hash_file).pack(pady=15)
        self.hash_output = tk.Text(tab, font=("Consolas", 10))
        self.hash_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def hash_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        h256 = hashlib.sha256()
        h1 = hashlib.sha1()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h256.update(chunk)
                h1.update(chunk)

        self.hash_output.delete("1.0", "end")
        self.hash_output.insert(
            "end",
            f"File: {path}\n\nSHA-256:\n{h256.hexdigest()}\n\nSHA-1:\n{h1.hexdigest()}\n"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberLabSuite(root)
    root.mainloop()
