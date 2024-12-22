import requests
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from requests.exceptions import RequestException
from ..config import Config

logger = logging.getLogger(__name__)

class PIMS2Error(Exception):
    """Custom exception for PIMS2-related errors."""
    pass

class PIMS2Client:
    """Client for interacting with PIMS2 system."""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.token: Optional[str] = None
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure the requests session with default headers and settings."""
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    async def authenticate(self) -> None:
        """Authenticate with PIMS2 system."""
        try:
            response = self.session.post(
                urljoin(self.config.get_pims2_url(), 'auth/token'),
                json={
                    'username': self.config.pims2_settings['username'],
                    'password': self.config.pims2_settings['password']
                }
            )
            response.raise_for_status()
            self.token = response.json()['token']
            self.session.headers['Authorization'] = f'Bearer {self.token}'
        except RequestException as e:
            raise PIMS2Error(f"Authentication failed: {str(e)}")

    async def get_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Retrieve data from PIMS2 endpoint."""
        try:
            if not self.token:
                await self.authenticate()

            response = self.session.get(
                urljoin(self.config.get_pims2_url(), endpoint),
                params=params
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise PIMS2Error(f"Failed to retrieve data from {endpoint}: {str(e)}")

    async def post_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send data to PIMS2 endpoint."""
        try:
            if not self.token:
                await self.authenticate()

            response = self.session.post(
                urljoin(self.config.get_pims2_url(), endpoint),
                json=data
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise PIMS2Error(f"Failed to send data to {endpoint}: {str(e)}")
