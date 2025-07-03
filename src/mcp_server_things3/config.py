"""Configuration management for Things3 MCP server using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Settings for Things3 MCP server.
    
    Configuration can be provided via:
    1. Environment variables with THINGS3_ prefix (e.g., THINGS3_AUTH_TOKEN)
    2. MCP initialization config (e.g., {"auth_token": "token"})
    
    MCP init config takes precedence over environment variables.
    """
    model_config = SettingsConfigDict(
        env_prefix="THINGS3_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra fields in MCP init config
    )
    
    # Auth token for Things3 URL scheme operations
    auth_token: Optional[str] = None
    
    @property
    def is_authenticated(self) -> bool:
        """Check if authentication is configured."""
        return self.auth_token is not None
    
    def validate_auth(self) -> None:
        """Validate that auth token is configured when needed."""
        if not self.is_authenticated:
            raise ValueError(
                "Authentication required. Set THINGS3_AUTH_TOKEN environment variable "
                "or provide auth_token in MCP initialization config."
            )