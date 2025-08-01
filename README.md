# Gasless Escrow System

A milestone-based escrow platform that enables **completely gasless interactions** for end users through EIP-2612 permits and ERC-2771 meta-transactions. Built for freelancers and clients who want to use blockchain escrow without crypto complexity.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Solidity](https://img.shields.io/badge/Solidity-^0.8.28-363636.svg?logo=solidity)
![Python](https://img.shields.io/badge/Python-3.11+-3776ab.svg?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178c6.svg?logo=typescript&logoColor=white)

## 🌟 Overview

This project demonstrates how to build **truly gasless Web3 applications** by combining:

- **EIP-2612 USDC Permits** - Gasless token approvals through off-chain signatures
- **ERC-2771 Meta-Transactions** - Gasless contract interactions via trusted forwarders
- **Sponsor-Paid Gas** - Backend pays all transaction fees on behalf of users
- **Milestone-Based Escrow** - Secure payment system with incremental fund release

**The Result:** Users can interact with smart contracts using only email authentication - no wallets, no ETH, no gas fees, no crypto knowledge required.

## 💡 Key Innovation

**Problem:** Traditional Web3 UX requires users to:
- Install wallets (MetamMask, etc.)
- Buy ETH for gas fees  
- Understand blockchain concepts
- Manage private keys and seed phrases

**Solution:** This system abstracts away all blockchain complexity:
- ✅ **Sign in with email** - No wallet installation
- ✅ **Zero gas fees** - Backend sponsors all transactions
- ✅ **Familiar UX** - Feels like a traditional web app
- ✅ **Full security** - All transactions cryptographically signed by users

## 🏗️ Technical Architecture

```mermaid
graph TB
    User[👤 User] --> Frontend[🖥️ Next.js Frontend]
    Frontend --> Backend[🐍 FastAPI Backend]
    Backend --> Sponsor[💰 Sponsor Account]
    Backend --> DB[(🗄️ PostgreSQL)]
    
    User --> |EIP-2612 Permit| USDC[💱 USDC Contract]
    User --> |EIP-712 Signature| Forwarder[📡 ERC2771Forwarder]
    
    Sponsor --> |Pays Gas| Forwarder
    Sponsor --> |Pays Gas| USDC
    
    Forwarder --> |Meta-Transaction| Escrow[📝 Escrow Contract]
    USDC --> |Transfer| Escrow
    
    subgraph "Base Sepolia Testnet"
        USDC
        Forwarder
        Escrow
    end
```

### Flow Breakdown

1. **User Action**: User wants to fund a milestone
2. **USDC Permit**: User signs EIP-2612 permit (gasless approval)
3. **Sponsor Submission**: Backend submits permit using sponsor account (pays gas)
4. **Meta-Transaction**: User signs EIP-712 meta-transaction for escrow funding
5. **Forwarder Execution**: Backend submits meta-transaction via ERC2771Forwarder (pays gas)
6. **Contract Execution**: Escrow contract receives original user address via `_msgSender()`
7. **Token Transfer**: USDC transfers from user to escrow contract
8. **Milestone Update**: Database updated with funding status

## 🛠️ Tech Stack

### Smart Contracts
- **Solidity ^0.8.28** - Contract development
- **Hardhat** - Development framework  
- **OpenZeppelin ERC2771Context** - Meta-transaction support
- **OpenZeppelin ERC2771Forwarder** - Trusted forwarder implementation
- **Base Sepolia** - L2 testnet deployment

### Backend
- **FastAPI** - High-performance Python API
- **Web3.py** - Ethereum interaction
- **PostgreSQL** - Data persistence
- **eth-account** - Cryptographic signing
- **python-dotenv** - Environment management

### Frontend  
- **Next.js 15** - React framework with SSR
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **NextAuth.js** - Authentication
- **Lucide React** - Icon library

### Infrastructure
- **EIP-2612** - USDC permit signatures
- **EIP-712** - Typed data signing
- **ERC-2771** - Meta-transaction standard
- **Base L2** - Low-cost blockchain deployment

## 📁 Project Structure

```
stablecoin-poc/
├── contracts/                 # Smart contract development
│   ├── contracts/
│   │   ├── Escrow.sol         # Main escrow contract with ERC2771Context
│   │   └── Forwarder.sol      # ERC2771Forwarder implementation
│   ├── scripts/               # Deployment scripts
│   └── hardhat.config.js      # Hardhat configuration
│
├── backend/                   # FastAPI backend
│   └── app/
│       ├── main.py           # FastAPI application entry
│       ├── routes/           # API endpoints
│       │   ├── escrow.py     # Escrow-related endpoints
│       │   ├── invoice.py    # Invoice management
│       │   └── users.py      # User management
│       ├── services/         # Business logic
│       │   ├── escrow.py     # Meta-transaction orchestration
│       │   └── permit2.py    # EIP-2612 permit handling
│       ├── database/         # Data access layer
│       └── utils/            # Contract ABIs and utilities
│
├── frontend/                 # Next.js frontend
│   ├── components/           # React components
│   ├── pages/               # Next.js pages
│   └── services/            # API client
│
└── shared/                  # Shared Python modules
    ├── constants.py         # Blockchain constants
    └── utils.py            # Utility functions
```

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+**
- **Python 3.11+**
- **PostgreSQL**
- **Alchemy API key** (for Base Sepolia RPC)

### Environment Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gasless-escrow-system.git
cd gasless-escrow-system
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Blockchain Configuration
RPC_URL=https://base-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY
USDC_CONTRACT_ADDRESS=0x036CbD53842c5426634e7929541eC2318f3dCF7e
FORWARDER_CONTRACT_ADDRESS=YOUR_DEPLOYED_FORWARDER_ADDRESS
PERMIT2_ADDRESS=0x000000000022D473030F116dDEE9F6B43aC78BA3

# Wallet Configuration (for testnet only!)
SPONSOR_PRIVATE_KEY=your_sponsor_private_key_here

# Application Configuration
ENV=development
PORT=8000
API_URL=http://localhost:8000
SERVER_SECRET=your_server_secret_key_here
NEXTAUTH_SECRET=your_nextauth_secret_here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
```

### Smart Contract Deployment

1. **Install dependencies**
```bash
cd contracts
npm install
```

2. **Deploy contracts**
```bash
# Deploy forwarder
npx hardhat run scripts/deployForwarder.js --network base_sepolia

# Deploy escrow (using forwarder address)
npx hardhat run scripts/deployEscrow.js --network base_sepolia
```

3. **Update contract addresses in .env**

### Backend Setup

1. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up database**
```bash
# Create PostgreSQL database
createdb escrowdb

# Tables are auto-created on startup
```

3. **Run backend**
```bash
cd backend
PYTHONPATH=/path/to/project uvicorn app.main:app --reload
```

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Run development server**
```bash
npm run dev
```

## 💰 Gas Sponsorship Model

The system uses a **sponsor account** that pays gas fees for all user transactions:

```python
# Backend sponsors gas for user transactions
sponsor_account = w3.eth.account.from_key(SPONSOR_PRIVATE_KEY)

# User signs permit (gasless)
permit_signature = generate_usdc_permit_signature(user_account, spender, amount)

# Sponsor submits permit (pays gas)
submit_usdc_permit_via_sponsor(permit_signature, sponsor_account)

# User signs meta-transaction (gasless)  
meta_tx_signature = sign_meta_transaction(user_account, function_call)

# Sponsor executes meta-transaction (pays gas)
execute_meta_transaction(meta_tx_signature, sponsor_account)
```

**Cost Estimation:**
- Permit transaction: ~50,000 gas
- Meta-transaction: ~150,000 gas  
- Base Sepolia gas price: ~0.001 gwei
- **Cost per user action: ~$0.0002**

## 🔐 Security Model

### User Security
- **Private keys generated** and encrypted server-side
- **Never exposed** to frontend or user
- **EIP-712 signatures** ensure transaction authenticity
- **Permit expiration** limits approval timeframes

### Contract Security  
- **OpenZeppelin contracts** - battle-tested implementations
- **ERC2771Context** - prevents signature replay attacks
- **Trusted forwarder** - validates meta-transaction signatures
- **Client authorization** - only authorized addresses can fund/release

### Backend Security
- **Environment variables** for sensitive data
- **Database encryption** for private keys
- **API rate limiting** (recommended for production)
- **CORS configuration** restricts frontend access

## 🧪 Testing

### Contract Tests
```bash
cd contracts
npx hardhat test
```

### Backend Tests  
```bash
cd backend
python -m pytest tests/
```

### Integration Tests
```bash
# Test full gasless flow
python test_contract.py
```

## 📊 Gas Optimization

The system achieves gasless UX through several optimizations:

1. **EIP-2612 Permits** - Replace `approve()` + `transferFrom()` with single permit
2. **Batch Operations** - Multiple permits can be signed offline
3. **Meta-Transaction Batching** - Single forwarder call for multiple operations
4. **Efficient Contract Design** - Minimal storage operations
5. **L2 Deployment** - Base L2 offers ~100x cheaper gas than mainnet

## 🤝 Contributing

This project is open-sourced to demonstrate gasless Web3 UX patterns. Contributions welcome!

### Development Setup
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)  
3. Make changes and test thoroughly
4. Commit with clear messages (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

### Areas for Contribution
- [ ] Additional ERC-20 token support
- [ ] Enhanced frontend components  
- [ ] Mobile-responsive design
- [ ] Advanced escrow features (disputes, arbitration)
- [ ] Gas optimization improvements
- [ ] Comprehensive test coverage
- [ ] Documentation improvements

## 🚀 Deployment

### Testnet Deployment
The system is configured for **Base Sepolia** testnet:
- Low gas costs for testing
- Faucets available for test tokens
- Identical to mainnet Base L2

### Production Considerations
For mainnet deployment:
1. **Update contract addresses** for mainnet USDC
2. **Deploy to Base mainnet** for low gas costs
3. **Implement monitoring** for sponsor account balance
4. **Add rate limiting** and abuse prevention
5. **Consider multi-sig** for sponsor account security

## 📚 Resources

### EIP Standards
- [EIP-2612: Permit Extension for ERC-20](https://eips.ethereum.org/EIPS/eip-2612)
- [EIP-712: Typed Structured Data Hashing](https://eips.ethereum.org/EIPS/eip-712)  
- [ERC-2771: Secure Protocol for Native Meta Transactions](https://eips.ethereum.org/EIPS/eip-2771)

### Documentation
- [OpenZeppelin Meta Transactions](https://docs.openzeppelin.com/contracts/4.x/api/metatx)
- [Base L2 Documentation](https://docs.base.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenZeppelin** - For secure, audited smart contract implementations
- **Base Protocol** - For low-cost L2 infrastructure  
- **FastAPI** - For high-performance Python web framework
- **Next.js** - For excellent React development experience

---

**Built with ❤️ for the future of gasless Web3 UX**

*This project demonstrates that blockchain applications can have the same user experience as traditional web applications while maintaining the security and decentralization benefits of Web3.*