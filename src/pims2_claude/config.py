"""Configuration management for PIMS2 Claude integration."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from cryptography.fernet import Fernet

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

class Config:
    """Configuration class for managing PIMS2 and Claude settings."""
    
    REQUIRED_PIMS2_SETTINGS = {
        'host': str,
        'port': int,
        'username': str,
        'api_version': str
    }
    
    REQUIRED_CLAUDE_SETTINGS = {
        'api_key': str,
        'model_version': str,
        'max_tokens': int,
        'temperature': float
    }

    def __init__(self):
        self.pims2_settings: Dict[str, Any] = {}
        self.claude_settings: Dict[str, Any] = {}
        self.encryption_key: Optional[bytes] = None
        self._load_encryption_key()

    def _load_encryption_key(self) -> None:
        """Load or generate encryption key for secure credential storage."""
        key_path = Path.home() / '.pims2claude' / 'key.sec'
        if not key_path.exists():
            key_path.parent.mkdir(parents=True, exist_ok=True)
            self.encryption_key = Fernet.generate_key()
            key_path.write_bytes(self.encryption_key)
        else:
            self.encryption_key = key_path.read_bytes()

    def _encrypt_value(self, value: str) -> str:
        """Encrypt sensitive configuration values."""
        f = Fernet(self.encryption_key)
        return f.encrypt(value.encode()).decode()

    def _decrypt_value(self, value: str) -> str:
        """Decrypt sensitive configuration values."""
        f = Fernet(self.encryption_key)
        return f.decrypt(value.encode()).decode()

    def validate_settings(self) -> None:
        """Validate all required settings are present and of correct type."""
        # Validate PIMS2 settings
        for key, expected_type in self.REQUIRED_PIMS2_SETTINGS.items():
            if key not in self.pims2_settings:
                raise ConfigurationError(f"Missing required PIMS2 setting: {key}")
            if not isinstance(self.pims2_settings[key], expected_type):
                raise ConfigurationError(
                    f"Invalid type for PIMS2 setting {key}. "
                    f"Expected {expected_type.__name__}, "
                    f"got {type(self.pims2_settings[key]).__name__}"
                )

        # Validate Claude settings
        for key, expected_type in self.REQUIRED_CLAUDE_SETTINGS.items():
            if key not in self.claude_settings:
                raise ConfigurationError(f"Missing required Claude setting: {key}")
            if not isinstance(self.claude_settings[key], expected_type):
                raise ConfigurationError(
                    f"Invalid type for Claude setting {key}. "
                    f"Expected {expected_type.__name__}, "
                    f"got {type(self.claude_settings[key]).__name__}"
                )

    def load_config(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        if not os.path.exists(config_path):
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            self.pims2_settings = config.get('pims2', {})
            self.claude_settings = config.get('claude', {})

            # Decrypt sensitive values
            if 'password' in self.pims2_settings:
                self.pims2_settings['password'] = self._decrypt_value(
                    self.pims2_settings['password']
                )
            if 'api_key' in self.claude_settings:
                self.claude_settings['api_key'] = self._decrypt_value(
                    self.claude_settings['api_key']
                )

            self.validate_settings()

        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")

    def save_config(self, config_path: str) -> None:
        """Save configuration to YAML file."""
        try:
            # Create a copy of settings to avoid modifying the original
            config = {
                'pims2': self.pims2_settings.copy(),
                'claude': self.claude_settings.copy()
            }

            # Encrypt sensitive values for storage
            if 'password' in config['pims2']:
                config['pims2']['password'] = self._encrypt_value(
                    config['pims2']['password']
                )
            if 'api_key' in config['claude']:
                config['claude']['api_key'] = self._encrypt_value(
                    config['claude']['api_key']
                )

            with open(config_path, 'w') as f:
                yaml.safe_dump(config, f)

        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {e}")

    def update_pims2_settings(self, settings: Dict[str, Any]) -> None:
        """Update PIMS2 settings."""
        self.pims2_settings.update(settings)
        self.validate_settings()

    def update_claude_settings(self, settings: Dict[str, Any]) -> None:
        """Update Claude settings."""
        self.claude_settings.update(settings)
        self.validate_settings()

    def get_pims2_url(self) -> str:
        """Get the formatted PIMS2 URL."""
        return f"http://{self.pims2_settings['host']}:{self.pims2_settings['port']}/api/v{self.pims2_settings['api_version']}"
