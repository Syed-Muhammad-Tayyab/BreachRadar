<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=220&section=header&text=BreachRadar&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Know%20Before%20They%20Do&descAlignY=58&descSize=18)

### 🔐 Privacy-Safe Password Breach Checker — CLI Tool

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=2800&pause=900&color=00E5FF&center=true&vCenter=true&width=650&lines=Hashing+passwords+locally...;Checking+against+known+breaches...;Your+password+never+leaves+the+device...;Stay+one+step+ahead+of+attackers+%F0%9F%9B%A1%EF%B8%8F" alt="Typing SVG" />

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![k--Anonymity](https://img.shields.io/badge/Privacy-k--Anonymity%20Model-00C853?style=for-the-badge&logo=shieldsdotio&logoColor=white)](#-how-it-works)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-success?style=for-the-badge)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](#-contributing)

![GitHub repo size](https://img.shields.io/badge/dynamic-repo--size-informational?style=flat-square)
![GitHub stars](https://img.shields.io/badge/⭐_Star_this_repo-if_it_helped_you-gold?style=flat-square)

</div>

---

## 📜 Table of Contents

- [About](#-about)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [Roadmap](#-roadmap)
- [Disclaimer](#-disclaimer)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 About

**BreachRadar** is a lightweight command-line tool that checks whether a password has appeared in known public data-breach dumps — without ever sending your actual password over the network.

It uses the industry-standard **k-Anonymity** model (the same approach behind [Have I Been Pwned's Pwned Passwords API](https://haveibeenpwned.com/Passwords)) so you — or your users, if you build this into a signup form — can check password safety with **zero plaintext exposure**.

> Built as a practical cybersecurity utility: small enough to read in five minutes, solid enough to actually use.

---

## ⚙️ How It Works

```
┌──────────────┐     ┌───────────────────────┐     ┌────────────────────┐
│   Password    │ --> │  SHA-1 hash (local)   │ --> │  Split hash        │
│  (never sent) │     │  e.g. 5BAA6...         │     │  prefix | suffix   │
└──────────────┘     └───────────────────────┘     └────────────────────┘
                                                              │
                              Only the 5-char prefix is sent ▼
                                                   ┌─────────────────────┐
                                                   │  HIBP Range API     │
                                                   │  returns ALL hashes │
                                                   │  matching prefix    │
                                                   └─────────────────────┘
                                                              │
                                      Suffix matched locally  ▼
                                                   ┌─────────────────────┐
                                                   │  Breached? Y/N +    │
                                                   │  times seen         │
                                                   └─────────────────────┘
```

1. Your password is hashed **locally** with SHA-1.
2. Only the **first 5 characters** of that hash are sent to the API.
3. The API returns every breached hash suffix that shares that prefix (usually hundreds).
4. BreachRadar checks locally whether your full suffix is in that list.

Your full password and full hash **never leave your machine.**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔒 **Zero plaintext exposure** | Only a 5-char hash prefix is transmitted |
| ⌨️ **Hidden input mode** | Interactive prompt hides your typed password |
| 📂 **Bulk file checking** | Check an entire password list in one run |
| 🚦 **Exit codes for automation** | `0` = clean, `1` = breach found — CI/script friendly |
| 🧵 **Rate-limit friendly** | Small delay between bulk requests |
| 🧰 **Zero config** | One dependency, one file, works out of the box |

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=python)
![Requests](https://img.shields.io/badge/-Requests-black?style=flat-square&logo=python)
![HIBP API](https://img.shields.io/badge/-HIBP%20API-black?style=flat-square&logo=haveibeenpwned)

---

## 🗂️ Project Structure

```
BreachRadar/
├── breachradar.py      # Main CLI tool
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # You are here
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Internet connection (for the breach lookup only — no account/API key needed)

### Installation

```bash
git clone https://github.com/Syed-Muhammad-Tayyab/BreachRadar.git
cd BreachRadar

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🖥️ Usage

```bash
# Interactive mode (password input hidden, safest option)
python breachradar.py

# Check a single password inline (visible in shell history — use with care)
python breachradar.py --password "Summer2024!"

# Check a whole list of passwords from a file (one per line)
python breachradar.py --file passwords.txt
```

Exit code `1` means at least one checked password was found in a breach — handy for CI pipelines or pre-commit hooks guarding secrets files.

---

## 📟 Example Output

```
$ python breachradar.py --file passwords.txt
Checking 3 password(s) from 'passwords.txt'...

[X] line 1: FOUND in breaches (9,659,365 times) — change it immediately
[OK] line 2: not found in known breaches
[X] line 3: FOUND in breaches (412 times) — change it immediately
```

---

## 🗺️ Roadmap

- [x] Core k-Anonymity breach lookup
- [x] Interactive hidden-input mode
- [x] Bulk file checking
- [ ] JSON / CSV export of results
- [ ] Password strength scoring (entropy-based)
- [ ] Optional email breach check (HIBP breached-account API)
- [ ] Pre-commit hook packaging

---

## ⚠️ Disclaimer

This tool is for **defensive security purposes** — checking your own or your organization's credentials for exposure. It queries the public Have I Been Pwned Pwned Passwords API and does not store, log, or transmit full passwords. Use responsibly and only on credentials you own or are authorized to test.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 📬 Contact

<div align="center">

**Syed Muhammad Tayyab**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Syed-Muhammad-Tayyab)

⭐ **If this project helped you, consider giving it a star!** ⭐

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,100:0f2027&height=100&section=footer)

</div>
