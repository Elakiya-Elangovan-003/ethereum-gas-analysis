"""
Generate visualizations for EIP-1559 analysis
Creates charts showing fee market dynamics.
"""

import json
import matplotlib.pyplot as plt
import statistics

class Visualizer:
    """Creates charts for EIP-1559 analysis"""
    
    def __init__(self, blocks_file='../data/blocks.json'):
        """Load block data"""
        with open(blocks_file, 'r') as f:
            self.blocks = json.load(f)
        print(f'Loaded {len(self.blocks)} blocks for visualization')
    
    def plot_base_fee_over_time(self):
        """Plot base fee changes over blocks"""
        block_numbers = [b['number'] for b in self.blocks]
        base_fees = [b['base_fee_per_gas'] / 1e9 for b in self.blocks]
        
        plt.figure(figsize=(12, 6))
        plt.plot(block_numbers, base_fees, linewidth=1, color='#627EEA')
        plt.xlabel('Block Number')
        plt.ylabel('Base Fee (Gwei)')
        plt.title('EIP-1559 Base Fee Over Time')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('charts/base_fee_timeline.png', dpi=300)
        print('Saved: charts/base_fee_timeline.png')
        plt.close()
    
    def plot_block_fullness(self):
        """Plot block fullness distribution"""
        fullness = [b['block_fullness'] for b in self.blocks]
        
        plt.figure(figsize=(12, 6))
        plt.hist(fullness, bins=50, color='#627EEA', alpha=0.7, edgecolor='black')
        plt.axvline(50, color='red', linestyle='--', linewidth=2, label='Target (50%)')
        plt.xlabel('Block Fullness (%)')
        plt.ylabel('Number of Blocks')
        plt.title('Block Fullness Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('charts/block_fullness_distribution.png', dpi=300)
        print('Saved: charts/block_fullness_distribution.png')
        plt.close()
    
    def plot_gas_used_vs_target(self):
        """Plot gas used vs target over time"""
        block_numbers = [b['number'] for b in self.blocks]
        gas_used = [b['gas_used'] / 1e6 for b in self.blocks]
        gas_target = [b['gas_target'] / 1e6 for b in self.blocks]
        
        plt.figure(figsize=(12, 6))
        plt.plot(block_numbers, gas_used, label='Gas Used', linewidth=1, color='#627EEA')
        plt.plot(block_numbers, gas_target, label='Gas Target (50%)', linestyle='--', color='red', linewidth=2)
        plt.xlabel('Block Number')
        plt.ylabel('Gas (Millions)')
        plt.title('Gas Used vs Target Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('charts/gas_used_vs_target.png', dpi=300)
        print('Saved: charts/gas_used_vs_target.png')
        plt.close()
    
    def plot_burn_vs_tips(self):
        """Plot ETH burned vs tips"""
        burned = [b['eth_burned'] for b in self.blocks]
        
        # Calculate tips per block
        tips = []
        for block in self.blocks:
            tip = (block['avg_priority_fee'] * block['gas_used']) / 1e18
            tips.append(tip)
        
        block_numbers = [b['number'] for b in self.blocks]
        
        plt.figure(figsize=(12, 6))
        plt.plot(block_numbers, burned, label='ETH Burned', linewidth=1, color='#FF6B6B')
        plt.plot(block_numbers, tips, label='Tips to Validators', linewidth=1, color='#4ECDC4')
        plt.xlabel('Block Number')
        plt.ylabel('ETH')
        plt.title('ETH Burned vs Tips to Validators')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('charts/burn_vs_tips.png', dpi=300)
        print('Saved: charts/burn_vs_tips.png')
        plt.close()
    
    def plot_priority_fees(self):
        """Plot priority fee distribution"""
        avg_tips = [b['avg_priority_fee'] / 1e9 for b in self.blocks]
        
        plt.figure(figsize=(12, 6))
        plt.hist(avg_tips, bins=50, color='#4ECDC4', alpha=0.7, edgecolor='black')
        plt.xlabel('Average Priority Fee (Gwei)')
        plt.ylabel('Number of Blocks')
        plt.title('Priority Fee Distribution')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('charts/priority_fee_distribution.png', dpi=300)
        print('Saved: charts/priority_fee_distribution.png')
        plt.close()
    
    def create_summary_dashboard(self):
        """Create a summary dashboard with multiple metrics"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Base Fee
        block_nums = [b['number'] for b in self.blocks]
        base_fees = [b['base_fee_per_gas'] / 1e9 for b in self.blocks]
        ax1.plot(block_nums, base_fees, linewidth=1, color='#627EEA')
        ax1.set_title('Base Fee Over Time', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Block Number')
        ax1.set_ylabel('Base Fee (Gwei)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Block Fullness
        fullness = [b['block_fullness'] for b in self.blocks]
        ax2.hist(fullness, bins=30, color='#627EEA', alpha=0.7, edgecolor='black')
        ax2.axvline(50, color='red', linestyle='--', linewidth=2)
        ax2.set_title('Block Fullness Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Block Fullness (%)')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Gas Used vs Target
        gas_used = [b['gas_used'] / 1e6 for b in self.blocks]
        gas_target = [b['gas_target'] / 1e6 for b in self.blocks]
        ax3.plot(block_nums, gas_used, label='Gas Used', linewidth=1, color='#627EEA')
        ax3.plot(block_nums, gas_target, label='Target', linestyle='--', color='red', linewidth=2)
        ax3.set_title('Gas Used vs Target', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Block Number')
        ax3.set_ylabel('Gas (Millions)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: ETH Burned
        burned = [b['eth_burned'] for b in self.blocks]
        ax4.plot(block_nums, burned, linewidth=1, color='#FF6B6B')
        ax4.set_title('ETH Burned Per Block', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Block Number')
        ax4.set_ylabel('ETH Burned')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('EIP-1559 Gas Market Analysis Dashboard', fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig('charts/dashboard.png', dpi=300, bbox_inches='tight')
        print('Saved: charts/dashboard.png')
        plt.close()

if __name__ == '__main__':
    print('Generating visualizations...\n')
    viz = Visualizer()
    viz.plot_base_fee_over_time()
    viz.plot_block_fullness()
    viz.plot_gas_used_vs_target()
    viz.plot_burn_vs_tips()
    viz.plot_priority_fees()
    viz.create_summary_dashboard()
    print('\nAll visualizations created successfully!')
