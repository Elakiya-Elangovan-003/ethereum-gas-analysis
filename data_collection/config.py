"""
Configuration module for Ethereum data collection.
Loads RPC endpoints and settings from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Ethereum connection settings"""
    
    # Primary RPC endpoint (Infura)
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    
    # Backup RPC endpoint
    PUBLIC_ENDPOINT = os.getenv('PUBLIC_ENDPOINT')
    
    # Active endpoint (starts with Infura, can switch to backup)
    ACTIVE_ENDPOINT = INFURA_ENDPOINT
    
    # Request settings
    REQUEST_TIMEOUT = 30  # seconds
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2  # seconds between retries
    
    # Data collection settings
    BLOCKS_PER_BATCH = 100  # How many blocks to fetch at once
    SAVE_INTERVAL = 500  # Save data every N blocks
    
    @classmethod
    def switch_to_backup(cls):
        """Switch to backup RPC endpoint if primary fails"""
        cls.ACTIVE_ENDPOINT = cls.PUBLIC_ENDPOINT
        print(f'⚠️  Switched to backup endpoint: {cls.PUBLIC_ENDPOINT}')
    
    @classmethod
    def get_endpoint(cls):
        """Get the currently active RPC endpoint"""
        return cls.ACTIVE_ENDPOINT

# Print configuration on import (for verification)
if __name__ == '__main__':
    print('🔧 Ethereum Gas Analysis - Configuration')
    print(f'Primary Endpoint: {Config.INFURA_ENDPOINT}')
    print(f'Backup Endpoint: {Config.PUBLIC_ENDPOINT}')
    print(f'Active Endpoint: {Config.ACTIVE_ENDPOINT}')
    print(f'Request Timeout: {Config.REQUEST_TIMEOUT}s')
    print(f'Retry Attempts: {Config.RETRY_ATTEMPTS}')
