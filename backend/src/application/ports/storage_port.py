"""
Storage Port interface.
"""

from abc import ABC, abstractmethod
from typing import BinaryIO


class StoragePort(ABC):
    """Port for file storage"""

    @abstractmethod
    def save_file(self, file: BinaryIO, job_id: str, filename: str) -> str:
        """Save uploaded file and return path"""
        pass

    @abstractmethod
    def get_file_path(self, job_id: str, filename: str) -> str:
        """Get file path"""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        """Delete file"""
        pass
