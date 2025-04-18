import os

from typing import Any
from infisical_client import (
    ClientSettings,
    InfisicalClient,
    ListSecretsOptions,
    AuthenticationOptions,
    UniversalAuthMethod,
)
from src.services.logger_service import LoggerService

logger = LoggerService.get_logger(__name__)


class InfisicalManagedCredentials:
    def __init__(self) -> None:
        try:
            self.client = InfisicalClient(
                ClientSettings(
                    auth=AuthenticationOptions(
                        universal_auth=UniversalAuthMethod(
                            client_id=os.getenv("INFISICAL_CLIENT_ID"),
                            client_secret=os.getenv("INFISICAL_SECRET"),
                        ),
                    ),
                    cache_ttl=1,
                )
            )
            self()
            logger.info("Infisical Managed Credentials initialized")
        except Exception as e:
            logger.error(f"Error initializing Infisical client: {e}")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        try:
            _ = self.client.listSecrets(
                options=ListSecretsOptions(
                    environment="dev",
                    project_id=os.getenv("INFISICAL_PROJECT_ID"),
                    attach_to_process_env=True,
                ),
            )
            logger.info("Infisical Managed Credentials fetched")
        except Exception as e:
            logger.error(f"Error occured while fetching secrets: {e}")
            raise e
