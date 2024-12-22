"""Main interface for PIMS2 and Claude integration."""

from typing import Dict, Any, Optional
from .config import Config
from .pims2.client import PIMS2Client
from .claude.client import ClaudeClient

class InterfaceError(Exception):
    """Custom exception for interface-related errors."""
    pass

class PIMS2Interface:
    """Main interface class for PIMS2 and Claude integration."""

    def __init__(self, config: Config):
        self.config = config
        self.pims2_client: Optional[PIMS2Client] = None
        self.claude_client: Optional[ClaudeClient] = None

    async def initialize(self) -> None:
        """Initialize the interface and its components."""
        try:
            # Initialize PIMS2 client
            self.pims2_client = PIMS2Client(self.config)
            await self.pims2_client.authenticate()

            # Initialize Claude client
            self.claude_client = ClaudeClient(self.config)

        except Exception as e:
            raise InterfaceError(f"Failed to initialize interface: {str(e)}")

    async def process_pims2_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a PIMS2 request through Claude."""
        try:
            if not self.pims2_client or not self.claude_client:
                raise InterfaceError("Interface not initialized")

            # Get data from PIMS2
            pims2_data = await self.pims2_client.get_data(endpoint, params)

            # Process data through Claude
            processed_data = await self.claude_client.process_pims2_data(pims2_data)

            return processed_data

        except Exception as e:
            raise InterfaceError(f"Failed to process PIMS2 request: {str(e)}")

    async def close(self) -> None:
        """Clean up and close connections."""
        if self.pims2_client:
            self.pims2_client.close()
