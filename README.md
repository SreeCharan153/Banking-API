# 🏦 Banking System (CLI) — SQLite Backend

A command-line banking application built with **Python** and **SQLite**.  
It supports secure PIN-based login, deposits, withdrawals, transfers, balance inquiry, and a full transaction history.

---

## 🚀 Features
- **Accounts**
  - Create account with unique `account_no`
  - Update mobile number and email
  - Secure PIN storage (hashed with SHA-512)
- **Transactions**
  - Deposit / Withdraw
  - Transfer between accounts
  - Balance inquiry
- **History**
  - Every transaction recorded with action, amount, timestamp
- **Data**
  - SQLite database at `Database/Bank.db`

---

## 🛠️ Tech Stack
- **Language:** Python (3.10+ recommended)
- **Database:** SQLite (file: `Database/Bank.db`)
- **Security:** PIN hashed via SHA-512 (upgrade path: PBKDF2/Bcrypt/Argon2)
- **CLI App:** `main.py` (drives flows), `ATM.py` (business logic), `history.py` (logs)

---

## 📂 Project Structure
~~~text
Banking-API/
├─ ATM.py               # Core banking logic (create, auth, deposit, withdraw, transfer, etc.)
├─ history.py           # Transaction history utilities
├─ main.py              # CLI entry point (menus, input handling)
├─ Database/
│  ├─ Bank.db           # SQLite database
│  └─ Bank.sqbpro       # SQLiteStudio project file (optional)
├─ requirements.txt     # Python dependencies (if any)
└─ README.md            # This file
~~~

---

## ⚙️ Installation & Setup
~~~bash
# 1) Clone the repository
git clone https://github.com/SreeCharan153/Banking-API.git
cd Banking-API

# 2) (Recommended) Create & activate a virtual environment
python -m venv venv
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the CLI
python main.py
# Follow the on-screen prompts to create an account, login, and perform transactions.
~~~

---

## 🧭 Usage (CLI Flow)

### Create Account
~~~text
> Create Account
Enter Name: Alice
Enter Mobile: 9876543210
Enter Email: alice@example.com
Set 4-digit PIN: ****
Account created! Your account number is: ACC1001
~~~

### Login & Balance
~~~text
> Login
Account No: ACC1001
PIN: ****
Login successful.
Current Balance: 1000.00
~~~

### Deposit / Withdraw
~~~text
> Deposit
Amount: 500
Deposit successful. New Balance: 1500.00

> Withdraw
Amount: 200
Withdrawal successful. New Balance: 1300.00
~~~

### Transfer
~~~text
> Transfer
From: ACC1001
To:   ACC1002
Amount: 300
Transfer successful.
From Balance: 1000.00
To Balance:   2300.00
~~~

### History (Mini Statement)
~~~text
> History (ACC1001)
[1] DEPOSIT   +500.00   2025-08-20 10:30:00
[2] WITHDRAW  -200.00   2025-08-20 11:00:00
[3] TRANSFER  -300.00   2025-08-20 12:15:00
~~~

---

## 🔐 Security Notes
- **PIN Hashing:** Stored as SHA-512 digest (never plaintext).
- **Recommendation:** Upgrade to a slow, salted hash (e.g., **PBKDF2** or **bcrypt**) to resist brute-force attacks.
- **Validation:** Inputs (amounts/mobile/email) are validated in code; consider DB constraints for defense-in-depth.

---

## 🗃️ Database Schema

### Tables
- **accounts**
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `account_no` TEXT UNIQUE NOT NULL
  - `name` TEXT NOT NULL
  - `pin` TEXT NOT NULL           *(SHA-512 hash of PIN)*
  - `balance` REAL DEFAULT 0.0    *(non-negative recommended)*
  - `mobileno` TEXT               *(consider UNIQUE + length check)*
  - `gmail` TEXT                  *(consider UNIQUE)*

- **history**
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `account_id` TEXT NOT NULL    *(recommend INTEGER + FK to accounts.id)*
  - `action` TEXT NOT NULL        *(recommend CHECK IN ('DEPOSIT','WITHDRAW','TRANSFER'))*
  - `amount` REAL NOT NULL        *(recommend CHECK (amount > 0))*
  - `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP

### Suggested Hardening (optional migrations)
~~~sql
-- Enforce referential integrity & data quality
PRAGMA foreign_keys = ON;

-- Make account_id an INTEGER FK and constrain actions/amounts
-- (Requires migrating existing data if types differ.)
CREATE TABLE IF NOT EXISTS history_new (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  action TEXT NOT NULL CHECK(action IN ('DEPOSIT','WITHDRAW','TRANSFER')),
  amount REAL NOT NULL CHECK(amount > 0),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Example index for faster lookups by account_no
CREATE INDEX IF NOT EXISTS idx_accounts_account_no ON accounts(account_no);
~~~

---

## 🧭 Roadmap
- Migrate PIN hashing → **PBKDF2 / bcrypt / Argon2** with per-user salt
- Enforce DB constraints (FKs, CHECKs, UNIQUE on email/mobile)
- Add unit tests (pytest) and GitHub Actions CI
- Export a **mini-statement** API or migrate to a **REST API** (Flask/FastAPI)
- Optional: JWT auth if/when HTTP endpoints are introduced

---

## 🧪 Testing Tips
- Try creating multiple accounts and performing inter-account transfers.
- Validate edge cases:
  - Overdraft prevention (withdraw > balance)
  - Negative/zero amounts (reject)
  - Duplicate account numbers/emails/mobiles (avoid or handle)
- Verify history correctness after each operation.



## 🙌 Credits
Built as a learning project to practice **backend fundamentals**, **secure credential storage**, and **transaction workflows** with a real database.
