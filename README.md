# CyberLab Suite

CyberLab Suite is a safe, portfolio-oriented Python desktop application that demonstrates cybersecurity concepts without including credential theft, denial-of-service attacks, unauthorized cracking, or real email spoofing.

## Included Modules

- Key Event Visualizer — shows keyboard events only while its own text box is focused
- Authorized Port Scanner — scans a user-provided host and up to 50 specified ports
- Local Security Checks — performs non-exploitative system configuration checks
- PCAP Metadata Analyzer — examines metadata and hashes of an existing capture file
- Secure Password Generator — uses Python's `secrets` module
- Wi-Fi Network Viewer — shows nearby network information without revealing saved passwords
- NFC Tag Simulator — demonstrates a simulated NDEF-style payload
- Email Spoofing Awareness Simulator — demonstrates misleading display names/headers without sending mail
- File Hash Utility — calculates SHA-256 and SHA-1 hashes

## Run

```bash
python cyberlab_suite.py
```

## Build Windows EXE

Double-click:

```text
build_windows_exe.bat
```

The executable is created at:

```text
dist\CyberLabSuite.exe
```

## Ethical Use

Use security testing features only on devices and networks that you own or have explicit authorization to test.

This project intentionally does not implement:
- Global/background keylogging
- DDoS or traffic flooding
- Wi-Fi credential extraction
- NFC cracking
- Credential theft
- Real email spoofing

These exclusions make the project suitable for a public GitHub portfolio while still demonstrating Python, networking, security awareness, GUI development, hashing, subprocess handling, and basic socket programming.
