"""
Gas Usage and Block Fullness Analysis
Analyzes network congestion and block utilization patterns.
"""

import json
import statistics

class GasUsageAnalyzer:
    """Analyzes gas usage patterns and block fullness"""
    
    def __init__(self, blocks_file='../data/blocks.json'):
        """Load block data"""
        with open(blocks_file, 'r') as f:
            self.blocks = json.load(f)
        print(f'Loaded {len(self.blocks)} blocks for analysis')
    
    def analyze_block_fullness(self):
        """Analyze block fullness distribution"""
        fullness_values = [b['block_fullness'] for b in self.blocks]
        
        print('\n=== BLOCK FULLNESS ANALYSIS ===\n')
        print(f'Average block fullness: {statistics.mean(fullness_values):.2f}%')
        print(f'Median block fullness: {statistics.median(fullness_values):.2f}%')
        print(f'Min block fullness: {min(fullness_values):.2f}%')
        print(f'Max block fullness: {max(fullness_values):.2f}%')
        print(f'Std deviation: {statistics.stdev(fullness_values):.2f}%')
        
        # Categorize blocks
        nearly_empty = sum(1 for f in fullness_values if f < 25)
        low = sum(1 for f in fullness_values if 25 <= f < 50)
        medium = sum(1 for f in fullness_values if 50 <= f < 75)
        high = sum(1 for f in fullness_values if 75 <= f < 90)
        nearly_full = sum(1 for f in fullness_values if f >= 90)
        
        print('\n--- Block Fullness Distribution ---')
        print(f'Nearly empty (<25%): {nearly_empty} blocks ({nearly_empty/len(self.blocks)*100:.1f}%)')
        print(f'Low (25-50%): {low} blocks ({low/len(self.blocks)*100:.1f}%)')
        print(f'Medium (50-75%): {medium} blocks ({medium/len(self.blocks)*100:.1f}%)')
        print(f'High (75-90%): {high} blocks ({high/len(self.blocks)*100:.1f}%)')
        print(f'Nearly full (>90%): {nearly_full} blocks ({nearly_full/len(self.blocks)*100:.1f}%)')
    
    def analyze_gas_usage_vs_target(self):
        """Compare gas used vs target"""
        above_target = sum(1 for b in self.blocks if b['gas_used'] > b['gas_target'])
        below_target = sum(1 for b in self.blocks if b['gas_used'] < b['gas_target'])
        at_target = sum(1 for b in self.blocks if b['gas_used'] == b['gas_target'])
        
        print('\n=== GAS USAGE VS TARGET ===\n')
        print(f'Blocks above target (>15M gas): {above_target} ({above_target/len(self.blocks)*100:.1f}%)')
        print(f'Blocks below target (<15M gas): {below_target} ({below_target/len(self.blocks)*100:.1f}%)')
        print(f'Blocks at target (=15M gas): {at_target} ({at_target/len(self.blocks)*100:.1f}%)')
        
        # Calculate average gas used
        avg_gas = statistics.mean([b['gas_used'] for b in self.blocks])
        target_gas = self.blocks[0]['gas_target']
        
        print(f'\nAverage gas used: {avg_gas:,.0f}')
        print(f'Target gas: {target_gas:,.0f}')
        print(f'Difference from target: {((avg_gas - target_gas) / target_gas * 100):.2f}%')
    
    def analyze_transaction_patterns(self):
        """Analyze transaction count patterns"""
        tx_counts = [b['transaction_count'] for b in self.blocks]
        
        print('\n=== TRANSACTION PATTERNS ===\n')
        print(f'Average transactions per block: {statistics.mean(tx_counts):.1f}')
        print(f'Median transactions per block: {statistics.median(tx_counts):.0f}')
        print(f'Min transactions: {min(tx_counts)}')
        print(f'Max transactions: {max(tx_counts)}')
        
        # Find correlation between tx count and block fullness
        high_tx_blocks = [b for b in self.blocks if b['transaction_count'] > statistics.mean(tx_counts)]
        avg_fullness_high_tx = statistics.mean([b['block_fullness'] for b in high_tx_blocks])
        
        low_tx_blocks = [b for b in self.blocks if b['transaction_count'] <= statistics.mean(tx_counts)]
        avg_fullness_low_tx = statistics.mean([b['block_fullness'] for b in low_tx_blocks])
        
        print(f'\nAverage fullness (high tx blocks): {avg_fullness_high_tx:.2f}%')
        print(f'Average fullness (low tx blocks): {avg_fullness_low_tx:.2f}%')

if __name__ == '__main__':
    analyzer = GasUsageAnalyzer()
    analyzer.analyze_block_fullness()
    analyzer.analyze_gas_usage_vs_target()
    analyzer.analyze_transaction_patterns()
