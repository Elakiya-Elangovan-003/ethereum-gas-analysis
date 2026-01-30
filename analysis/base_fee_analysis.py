"""
EIP-1559 Base Fee Analysis
Analyzes how base fee adjusts based on block fullness.
"""

import json
import statistics

class BaseFeeAnalyzer:
    """Analyzes EIP-1559 base fee adjustment mechanism"""
    
    def __init__(self, blocks_file='../data/blocks.json'):
        """Load block data"""
        with open(blocks_file, 'r') as f:
            self.blocks = json.load(f)
        print(f'Loaded {len(self.blocks)} blocks for analysis')
    
    def calculate_base_fee_changes(self):
        """Calculate base fee changes between consecutive blocks"""
        changes = []
        
        for i in range(1, len(self.blocks)):
            prev_block = self.blocks[i-1]
            curr_block = self.blocks[i]
            
            prev_fee = prev_block['base_fee_per_gas']
            curr_fee = curr_block['base_fee_per_gas']
            
            if prev_fee > 0:
                percent_change = ((curr_fee - prev_fee) / prev_fee) * 100
            else:
                percent_change = 0
            
            changes.append({
                'block': curr_block['number'],
                'prev_base_fee': prev_fee,
                'curr_base_fee': curr_fee,
                'absolute_change': curr_fee - prev_fee,
                'percent_change': percent_change,
                'gas_used': prev_block['gas_used'],
                'gas_target': prev_block['gas_target'],
                'block_fullness': prev_block['block_fullness']
            })
        
        return changes
    
    def analyze_fee_adjustment_behavior(self):
        """Analyze how base fee responds to gas usage"""
        changes = self.calculate_base_fee_changes()
        
        # Categorize blocks
        above_target = [c for c in changes if c['gas_used'] > c['gas_target']]
        below_target = [c for c in changes if c['gas_used'] < c['gas_target']]
        at_target = [c for c in changes if c['gas_used'] == c['gas_target']]
        
        print('\n=== BASE FEE ADJUSTMENT ANALYSIS ===\n')
        
        print(f'Total blocks analyzed: {len(changes)}')
        print(f'Blocks above target (50%): {len(above_target)} ({len(above_target)/len(changes)*100:.1f}%)')
        print(f'Blocks below target (50%): {len(below_target)} ({len(below_target)/len(changes)*100:.1f}%)')
        print(f'Blocks at target: {len(at_target)} ({len(at_target)/len(changes)*100:.1f}%)')
        
        # Calculate statistics for blocks above target
        if above_target:
            avg_increase = statistics.mean([c['percent_change'] for c in above_target])
            print(f'\nWhen blocks are ABOVE target:')
            print(f'  Average base fee increase: {avg_increase:.2f}%')
            print(f'  Max increase: {max(c["percent_change"] for c in above_target):.2f}%')
            print(f'  Min increase: {min(c["percent_change"] for c in above_target):.2f}%')
        
        # Calculate statistics for blocks below target
        if below_target:
            avg_decrease = statistics.mean([c['percent_change'] for c in below_target])
            print(f'\nWhen blocks are BELOW target:')
            print(f'  Average base fee change: {avg_decrease:.2f}%')
            print(f'  Max decrease: {min(c["percent_change"] for c in below_target):.2f}%')
            print(f'  Min decrease: {max(c["percent_change"] for c in below_target):.2f}%')
        
        return changes
    
    def get_base_fee_stats(self):
        """Get overall base fee statistics"""
        base_fees = [b['base_fee_per_gas'] for b in self.blocks]
        base_fees_gwei = [f / 1e9 for f in base_fees]
        
        print('\n=== BASE FEE STATISTICS ===\n')
        print(f'Average base fee: {statistics.mean(base_fees_gwei):.4f} Gwei')
        print(f'Median base fee: {statistics.median(base_fees_gwei):.4f} Gwei')
        print(f'Min base fee: {min(base_fees_gwei):.4f} Gwei')
        print(f'Max base fee: {max(base_fees_gwei):.4f} Gwei')
        print(f'Std deviation: {statistics.stdev(base_fees_gwei):.4f} Gwei')
        
        return base_fees_gwei

if __name__ == '__main__':
    analyzer = BaseFeeAnalyzer()
    analyzer.get_base_fee_stats()
    analyzer.analyze_fee_adjustment_behavior()
