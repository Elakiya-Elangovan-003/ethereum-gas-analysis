"""
Priority Fee Analysis
Analyzes tips paid to validators under different network conditions.
"""

import json
import statistics

class PriorityFeeAnalyzer:
    """Analyzes priority fee (tip) behavior"""
    
    def __init__(self, blocks_file='../data/blocks.json'):
        """Load block data"""
        with open(blocks_file, 'r') as f:
            self.blocks = json.load(f)
        print(f'Loaded {len(self.blocks)} blocks for analysis')
    
    def analyze_priority_fees(self):
        """Analyze priority fee statistics"""
        avg_tips = [b['avg_priority_fee'] for b in self.blocks if b['avg_priority_fee'] > 0]
        avg_tips_gwei = [t / 1e9 for t in avg_tips]
        
        print('\n=== PRIORITY FEE (TIPS) ANALYSIS ===\n')
        print(f'Blocks with tips: {len(avg_tips)} ({len(avg_tips)/len(self.blocks)*100:.1f}%)')
        
        if avg_tips_gwei:
            print(f'\nAverage tip: {statistics.mean(avg_tips_gwei):.4f} Gwei')
            print(f'Median tip: {statistics.median(avg_tips_gwei):.4f} Gwei')
            print(f'Min tip: {min(avg_tips_gwei):.4f} Gwei')
            print(f'Max tip: {max(avg_tips_gwei):.4f} Gwei')
            print(f'Std deviation: {statistics.stdev(avg_tips_gwei):.4f} Gwei')
    
    def analyze_tips_vs_congestion(self):
        """Analyze how tips change with network congestion"""
        
        # Categorize by block fullness
        low_congestion = [b for b in self.blocks if b['block_fullness'] < 50]
        high_congestion = [b for b in self.blocks if b['block_fullness'] >= 50]
        
        low_tips = [b['avg_priority_fee'] / 1e9 for b in low_congestion if b['avg_priority_fee'] > 0]
        high_tips = [b['avg_priority_fee'] / 1e9 for b in high_congestion if b['avg_priority_fee'] > 0]
        
        print('\n=== TIPS VS NETWORK CONGESTION ===\n')
        
        if low_tips:
            print(f'Low congestion (<50% full):')
            print(f'  Average tip: {statistics.mean(low_tips):.4f} Gwei')
            print(f'  Median tip: {statistics.median(low_tips):.4f} Gwei')
        
        if high_tips:
            print(f'\nHigh congestion (>=50% full):')
            print(f'  Average tip: {statistics.mean(high_tips):.4f} Gwei')
            print(f'  Median tip: {statistics.median(high_tips):.4f} Gwei')
        
        if low_tips and high_tips:
            increase = ((statistics.mean(high_tips) - statistics.mean(low_tips)) / statistics.mean(low_tips)) * 100
            print(f'\nTip increase during congestion: {increase:.2f}%')
    
    def analyze_tip_distribution(self):
        """Analyze distribution of tips"""
        all_tips = []
        for block in self.blocks:
            if block['avg_priority_fee'] > 0:
                all_tips.append(block['avg_priority_fee'] / 1e9)
        
        if not all_tips:
            return
        
        # Categorize tips
        very_low = sum(1 for t in all_tips if t < 0.001)
        low = sum(1 for t in all_tips if 0.001 <= t < 0.01)
        medium = sum(1 for t in all_tips if 0.01 <= t < 0.1)
        high = sum(1 for t in all_tips if 0.1 <= t < 1)
        very_high = sum(1 for t in all_tips if t >= 1)
        
        print('\n=== TIP DISTRIBUTION ===\n')
        print(f'Very low (<0.001 Gwei): {very_low} blocks ({very_low/len(all_tips)*100:.1f}%)')
        print(f'Low (0.001-0.01 Gwei): {low} blocks ({low/len(all_tips)*100:.1f}%)')
        print(f'Medium (0.01-0.1 Gwei): {medium} blocks ({medium/len(all_tips)*100:.1f}%)')
        print(f'High (0.1-1 Gwei): {high} blocks ({high/len(all_tips)*100:.1f}%)')
        print(f'Very high (>=1 Gwei): {very_high} blocks ({very_high/len(all_tips)*100:.1f}%)')

if __name__ == '__main__':
    analyzer = PriorityFeeAnalyzer()
    analyzer.analyze_priority_fees()
    analyzer.analyze_tips_vs_congestion()
    analyzer.analyze_tip_distribution()
