# Ethereum Gas Market & Fee Mechanism Analysis (EIP-1559)

A comprehensive analysis of Ethereum's EIP-1559 fee market using real blockchain data to understand base fee adjustment, gas usage patterns, priority fees, and validator economics.

## 🎯 Project Overview

This project analyzes Ethereum's revolutionary EIP-1559 fee mechanism by collecting and analyzing 1,000 blocks of real mainnet data. The analysis reveals how the protocol automatically adjusts transaction costs based on network demand.

## 📊 Key Findings

### 1. **EIP-1559 Self-Balancing Mechanism**
- **Average block fullness: 50.55%** - Almost exactly at the 50% target
- **48.7% blocks above target** → Base fee increases ~4.58%
- **51.3% blocks below target** → Base fee decreases ~4.08%
- **Perfect equilibrium** achieved through automatic adjustment

### 2. **Current Network State (Low Activity Period)**
- **Base fee: 0.0548 Gwei** (extremely low)
- **Priority fees: 0.4638 Gwei** (8.5x higher than base fee)
- **Tips dominate** fee composition (78-91% of total fees)
- **Network is inflationary** during quiet periods (-11.05 ETH net in 1,000 blocks)

### 3. **Congestion Impact**
- **Block fullness range:** 0.47% to 100%
- **Transaction variance:** 3 to 2,444 tx/block
- **Burn rate doubles** during high congestion (+97.79%)
- **Tips decrease 27.64%** during congestion (base fee does the work)

### 4. **Validator Economics**
- **ETH burned:** 1.64 ETH (over 1,000 blocks)
- **Tips to validators:** 12.69 ETH
- **Burn/Tips ratio:** 0.13:1
- In high-fee periods, this ratio inverts (more burn than tips)

## 🛠️ Tech Stack

- **Blockchain:** Ethereum Mainnet
- **Data Source:** Infura RPC API
- **Languages:** Python 3.14
- **Libraries:** Web3.py, Pandas, Matplotlib

## 📁 Project Structure
```
ethereum-gas-analysis/
├── data_collection/
│   ├── config.py              # RPC configuration
│   └── fetch_blocks.py        # Block data fetcher
├── analysis/
│   ├── base_fee_analysis.py   # EIP-1559 base fee mechanics
│   ├── gas_usage_analysis.py  # Block fullness & congestion
│   ├── priority_fee_analysis.py # Tip behavior analysis
│   └── validator_economics.py # Burn vs tips economics
├── visualizations/
│   ├── generate_charts.py     # Chart generation
│   └── charts/                # Output visualizations
├── data/
│   └── blocks.json            # Collected block data
└── README.md
```

## 📈 Visualizations

The project generates 6 charts:

1. **Base Fee Timeline** - Shows EIP-1559 fee adjustments over time
2. **Block Fullness Distribution** - Histogram of network congestion
3. **Gas Used vs Target** - Compares actual vs target gas usage
4. **ETH Burned vs Tips** - Validator earnings vs protocol burn
5. **Priority Fee Distribution** - User tip behavior patterns
6. **Dashboard** - Combined view of all key metrics

## 🚀 How to Run

### Prerequisites
```bash
Python 3.14+
Virtual environment (venv)
Ethereum RPC endpoint (Infura/Alchemy)
```

### Installation
```bash
# Clone/navigate to project
cd D:\ethereum-gas-analysis

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Dependencies already installed:
# web3, pandas, matplotlib, requests, python-dotenv
```

### Data Collection
```python
# Collect 1,000 blocks from Ethereum mainnet
cd data_collection
python fetch_blocks.py
```

### Run Analysis
```python
# Analyze base fee adjustment
cd analysis
python base_fee_analysis.py

# Analyze gas usage patterns
python gas_usage_analysis.py

# Analyze priority fees
python priority_fee_analysis.py

# Analyze validator economics
python validator_economics.py
```

### Generate Visualizations
```python
cd visualizations
python generate_charts.py
```

## 💡 Key Insights

### What is EIP-1559?
EIP-1559 (implemented August 2021) revolutionized Ethereum's fee market by:
- Introducing a **base fee** that adjusts automatically based on demand
- **Burning** the base fee (removing ETH from circulation)
- Adding **priority fees** (tips) that go to validators
- Targeting **50% block fullness** for optimal efficiency

### Why This Matters
- **For Users:** More predictable transaction costs
- **For Ethereum:** Deflationary pressure during high usage
- **For Validators:** Simpler, more predictable revenue
- **For Protocol:** Self-regulating capacity management

## 📊 Dataset Information

- **Blocks Analyzed:** 1,000
- **Block Range:** 24,337,593 - 24,338,592
- **Date Collected:** January 2026
- **Network State:** Low congestion period
- **Data Points per Block:** 11 metrics

## 🔬 Analysis Methodology

1. **Data Collection:** Real-time RPC calls to Ethereum mainnet
2. **Metric Calculation:** EIP-1559 formulas applied to raw block data
3. **Statistical Analysis:** Mean, median, distribution analysis
4. **Visualization:** Time series and distribution plots
5. **Economic Analysis:** Burn mechanics and validator incentives

## 📝 Future Enhancements

- [ ] Extended time series (10,000+ blocks)
- [ ] Comparison across different congestion periods
- [ ] MEV (Maximal Extractable Value) correlation
- [ ] Real-time monitoring dashboard
- [ ] Cross-chain fee market comparison

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Working with blockchain data via RPC
- ✅ Understanding EIP-1559 fee mechanics
- ✅ Python data analysis and visualization
- ✅ Protocol economics and tokenomics
- ✅ Statistical analysis of time-series data

## 📚 References

- [EIP-1559 Specification](https://eips.ethereum.org/EIPS/eip-1559)
- [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)
- [Web3.py Documentation](https://web3py.readthedocs.io/)

## 👤 Author

**Elakiya Elangovan**
- Project Type: Blockchain Infrastructure & Protocol Analysis
- Focus: Ethereum Fee Market Dynamics
- Date: January 2026

## 📄 License

This project is for educational and research purposes.

---

**Note:** This analysis captures a low-fee period on Ethereum. During high-demand periods (DeFi summers, NFT drops), base fees can exceed 100 Gwei, making the protocol strongly deflationary.
