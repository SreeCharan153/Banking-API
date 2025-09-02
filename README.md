# 🏦 Banking System — SQLite Backend

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

### Backend (FastAPI API)  

1. **Clone the repository**  
   git clone https://github.com/SreeCharan153/Banking-API.git  
   cd Banking-API  

2. **(Recommended) Create & activate a virtual environment**  
   python -m venv venv  
   # Mac/Linux:  
   source venv/bin/activate  
   # Windows:  
   venv\Scripts\activate  

3. **Install dependencies**  
   pip install -r requirements.txt  

4. **Start the FastAPI server**  
   uvicorn main:app --reload  

   - API available at: http://127.0.0.1:8000  
   - Interactive docs: http://127.0.0.1:8000/docs  

---

### Frontend (Next.js Web Application)  

- Repository: [Banking-Frontend](https://github.com/SreeCharan153/Banking-Frontend.git)  
- Live Demo: [Banking Web App](https://my-banking-application.vercel.app/)  

**Run locally:**  
   git clone https://github.com/SreeCharan153/Banking-Frontend.git  
   cd Banking-Frontend  

   npm install  
   npm run dev  

   App will run at: http://localhost:3000  

---

## 🧭 Usage  

### API (FastAPI Backend)  
- Once the backend is running, visit:  
  - Interactive API Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
  - Alternative ReDoc UI → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

Available endpoints include:  
- **POST /create_account** → Create a new user account  
- **POST /login** → Authenticate with account number + PIN  
- **GET /balance/{account_no}** → Check current balance  
- **POST /deposit** → Deposit money into an account  
- **POST /withdraw** → Withdraw money from an account  
- **POST /transfer** → Transfer funds between accounts  
- **GET /history/{account_no}** → View transaction history  

### Frontend (Next.js Web App)  
- Live Demo: [Banking Web App](https://my-banking-application.vercel.app/)  
- Repository: [Banking-Frontend](https://github.com/SreeCharan153/Banking-Frontend.git)  

The frontend provides a simple UI to:  
- Create a new account  
- Login with account number & PIN  
- View current balance  
- Deposit & withdraw funds  
- Transfer money between accounts  
- View transaction history (mini statement)  


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
