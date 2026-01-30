"""
Ethereum block data fetcher.
Connects to Ethereum and retrieves block-level data for EIP-1559 analysis.
"""

import json
import time
from web3 import Web3
from datetime import datetime
from config import Config

class BlockFetcher:
    """Fetches and processes Ethereum block data"""
    
    def __init__(self):
        """Initialize Web3 connection"""
        self.w3 = Web3(Web3.HTTPProvider(Config.get_endpoint(), request_kwargs={'timeout': Config.REQUEST_TIMEOUT}))
        self.verify_connection()
    
    def verify_connection(self):
        """Verify connection to Ethereum node"""
        try:
            if self.w3.is_connected():
                latest_block = self.w3.eth.block_number
                print(f'Connected to Ethereum - Latest block: {latest_block:,}')
                return True
            else:
                print('Failed to connect to Ethereum')
                return False
        except Exception as e:
            print(f'Connection error: {e}')
            return False
    
    def fetch_block(self, block_number):
        """Fetch a single block with full transaction details."""
        try:
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            
            block_data = {
                'number': block['number'],
                'timestamp': block['timestamp'],
                'base_fee_per_gas': block.get('baseFeePerGas', 0),
                'gas_used': block['gasUsed'],
                'gas_limit': block['gasLimit'],
                'transaction_count': len(block['transactions']),
                'miner': block['miner'],
            }
            
            block_data['gas_target'] = block['gasLimit'] // 2
            block_data['block_fullness'] = (block_data['gas_used'] / block_data['gas_limit']) * 100
            
            priority_fees = []
            for tx in block['transactions']:
                if 'maxPriorityFeePerGas' in tx and tx['maxPriorityFeePerGas'] is not None:
                    priority_fees.append(tx['maxPriorityFeePerGas'])
            
            if priority_fees:
                block_data['avg_priority_fee'] = sum(priority_fees) // len(priority_fees)
                block_data['max_priority_fee'] = max(priority_fees)
                block_data['min_priority_fee'] = min(priority_fees)
            else:
                block_data['avg_priority_fee'] = 0
                block_data['max_priority_fee'] = 0
                block_data['min_priority_fee'] = 0
            
            block_data['eth_burned'] = (block_data['base_fee_per_gas'] * block_data['gas_used']) / 1e18
            
            return block_data
            
        except Exception as e:
            print(f'Error fetching block {block_number}: {e}')
            return None
    
    def fetch_block_range(self, start_block, end_block):
        """Fetch a range of blocks."""
        blocks_data = []
        total_blocks = end_block - start_block + 1
        
        print(f'Fetching blocks {start_block:,} to {end_block:,} ({total_blocks:,} blocks)')
        
        for i, block_num in enumerate(range(start_block, end_block + 1), 1):
            block_data = self.fetch_block(block_num)
            
            if block_data:
                blocks_data.append(block_data)
                
                if i % 10 == 0 or i == total_blocks:
                    progress = (i / total_blocks) * 100
                    print(f'Progress: {i}/{total_blocks} ({progress:.1f}%) - Block {block_num:,}')
            
            time.sleep(0.1)
        
        print(f'Fetched {len(blocks_data)} blocks successfully')
        return blocks_data
    
    def save_blocks(self, blocks_data, filename='data/blocks.json'):
        """Save block data to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(blocks_data, f, indent=2)
            print(f'Saved {len(blocks_data)} blocks to {filename}')
            return True
        except Exception as e:
            print(f'Error saving data: {e}')
            return False

if __name__ == '__main__':
    print('Testing Block Fetcher...')
    fetcher = BlockFetcher()
    latest = fetcher.w3.eth.block_number
    print(f'Fetching last 5 blocks for testing...')
    test_blocks = fetcher.fetch_block_range(latest - 4, latest)
    
    if test_blocks:
        print('Sample Block Data:')
        sample = test_blocks[0]
        print(f'Block Number: {sample["number"]:,}')
        print(f'Base Fee: {sample["base_fee_per_gas"] / 1e9:.2f} Gwei')
        print(f'Gas Used: {sample["gas_used"]:,} / {sample["gas_limit"]:,}')
        print(f'Block Fullness: {sample["block_fullness"]:.2f}%')
        print(f'ETH Burned: {sample["eth_burned"]:.6f} ETH')
        print(f'Transactions: {sample["transaction_count"]}')
