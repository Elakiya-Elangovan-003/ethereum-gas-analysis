"""
Validator Economics Analysis
Analyzes ETH burned vs validator tips under EIP-1559.
"""

import json
import statistics

class ValidatorEconomicsAnalyzer:
    """Analyzes validator earnings and ETH burn dynamics"""
    
    def __init__(self, blocks_file='../data/blocks.json'):
        """Load block data"""
        with open(blocks_file, 'r') as f:
            self.blocks = json.load(f)
        print(f'Loaded {len(self.blocks)} blocks for analysis')
    
    def calculate_total_burn_and_tips(self):
        """Calculate total ETH burned and total tips"""
        total_burned = sum(b['eth_burned'] for b in self.blocks)
        
        # Calculate total tips
        total_tips = 0
        for block in self.blocks:
            avg_tip = block['avg_priority_fee']
            gas_used = block['gas_used']
            tx_count = block['transaction_count']
            
            if tx_count > 0:
                # Estimate total tips: avg tip * gas used
                total_tips += (avg_tip * gas_used) / 1e18
        
        print('\n=== TOTAL ETH BURNED VS TIPS ===\n')
        print(f'Total ETH burned: {total_burned:.6f} ETH')
        print(f'Total tips to validators: {total_tips:.6f} ETH')
        print(f'Burn vs Tips ratio: {total_burned/total_tips:.2f}:1')
        print(f'\nETH removed from circulation: {total_burned:.6f} ETH')
        print(f'ETH given to validators: {total_tips:.6f} ETH')
        print(f'Net deflationary effect: {total_burned - total_tips:.6f} ETH')
        
        return total_burned, total_tips
    
    def analyze_burn_rate_by_congestion(self):
        """Analyze burn rate under different congestion levels"""
        
        low_congestion = [b for b in self.blocks if b['block_fullness'] < 50]
        high_congestion = [b for b in self.blocks if b['block_fullness'] >= 50]
        
        low_burn = sum(b['eth_burned'] for b in low_congestion)
        high_burn = sum(b['eth_burned'] for b in high_congestion)
        
        print('\n=== BURN RATE BY CONGESTION ===\n')
        print(f'Low congestion blocks: {len(low_congestion)}')
        print(f'  Total burned: {low_burn:.6f} ETH')
        print(f'  Avg per block: {low_burn/len(low_congestion):.6f} ETH')
        
        print(f'\nHigh congestion blocks: {len(high_congestion)}')
        print(f'  Total burned: {high_burn:.6f} ETH')
        print(f'  Avg per block: {high_burn/len(high_congestion):.6f} ETH')
        
        increase = ((high_burn/len(high_congestion)) - (low_burn/len(low_congestion))) / (low_burn/len(low_congestion)) * 100
        print(f'\nBurn rate increase during congestion: {increase:.2f}%')
    
    def analyze_validator_revenue_composition(self):
        """Analyze validator revenue: base fee burn vs tips"""
        
        print('\n=== VALIDATOR REVENUE COMPOSITION ===\n')
        
        for block in self.blocks[:5]:  # Show first 5 blocks as examples
            burned = block['eth_burned']
            
            # Estimate tips for this block
            avg_tip = block['avg_priority_fee']
            gas_used = block['gas_used']
            tips = (avg_tip * gas_used) / 1e18
            
            total_fees = burned + tips
            
            print(f'Block {block["number"]}:')
            print(f'  Base fee (burned): {burned:.6f} ETH ({burned/total_fees*100:.1f}%)')
            print(f'  Tips (to validator): {tips:.6f} ETH ({tips/total_fees*100:.1f}%)')
            print(f'  Total fees: {total_fees:.6f} ETH')
            print()
    
    def analyze_base_fee_vs_tips(self):
        """Compare base fee to tips across all blocks"""
        
        base_fees = [b['base_fee_per_gas'] / 1e9 for b in self.blocks]
        avg_tips = [b['avg_priority_fee'] / 1e9 for b in self.blocks]
        
        print('\n=== BASE FEE VS TIPS COMPARISON ===\n')
        print(f'Average base fee: {statistics.mean(base_fees):.4f} Gwei')
        print(f'Average tip: {statistics.mean(avg_tips):.4f} Gwei')
        print(f'Tips as % of base fee: {(statistics.mean(avg_tips) / statistics.mean(base_fees)) * 100:.2f}%')
        
        # Find blocks where tips > base fee
        tips_higher = sum(1 for i in range(len(self.blocks)) if avg_tips[i] > base_fees[i])
        print(f'\nBlocks where tips > base fee: {tips_higher} ({tips_higher/len(self.blocks)*100:.1f}%)')

if __name__ == '__main__':
    analyzer = ValidatorEconomicsAnalyzer()
    analyzer.calculate_total_burn_and_tips()
    analyzer.analyze_burn_rate_by_congestion()
    analyzer.analyze_validator_revenue_composition()
    analyzer.analyze_base_fee_vs_tips()
