
# Stablecoin Escrow & Invoice Platform – Detailed Build Roadmap (Notion-Ready)

---

## 🔄 Kanban Board Columns
- **To Do** – Tasks you plan to start
- **In Progress** – Actively working on
- **Done** – Completed features
- **Backlog** – Optional/later-phase features

---

## 📅 EPIC: Project Setup

### ✅ Task: Initialize monorepo (backend, contracts, frontend placeholder)
- **Depends On**: None
- **Priority**: 🔥 High
- **Tools**: GitHub, VS Code, Python virtualenv
- **Purpose**: Scaffolds your workspace with backend (FastAPI), smart contracts (Solidity), and frontend placeholder (React or Streamlit)
- **Estimated Time**: 2 hrs
- **Cost**: $0

### ✅ Task: Install and configure FastAPI + Web3.py
- **Depends On**: Initialize monorepo
- **Priority**: 🔥 High
- **Purpose**: Sets up backend API and Ethereum interaction tools
- **Tools**: FastAPI, Web3.py, Uvicorn
- **Estimated Time**: 2–3 hrs
- **Cost**: $0

### ✅ Task: Install Ollama + run local LLM (Mistral or LLaMA 3)
- **Depends On**: Initialize monorepo
- **Priority**: 🔥 High
- **Purpose**: Sets up a free local LLM agent to reduce OpenAI API costs
- **Tools**: Ollama, LangChain
- **Estimated Time**: 1 hr
- **Cost**: $0
- **Notes**: Run `ollama run mistral` to test locally

### ✅ Task: Create shared .env config structure
- **Depends On**: Install FastAPI + Web3.py
- **Priority**: ✅ Medium
- **Purpose**: Prepares config for secrets, keys, endpoints
- **Estimated Time**: 30 min
- **Cost**: $0

### ✅ Task: Connect to Base Goerli RPC (Alchemy or Infura)
- **Depends On**: Create .env
- **Priority**: ✅ Medium
- **Tools**: Alchemy/Infura
- **Purpose**: Allows smart contract interaction
- **Estimated Time**: 15 min
- **Cost**: Free tier (up to 5M req/mo)

...

## 📊 Cost Summary Snapshot

| Category | Estimated Cost |
|----------|----------------|
| Hosting (Railway/Fly) | $0–$10/mo |
| Alchemy (Base testnet) | Free |
| Web3.py + FastAPI | Free |
| LangChain + Ollama | Free |
| Smart contract gas (testnet) | Free via faucet |
| SendGrid | Free (100/day) |
| Persona KYC (sandbox) | Free |

**Total Estimated PoC Cost: $0–$20/mo bootstrapped**
