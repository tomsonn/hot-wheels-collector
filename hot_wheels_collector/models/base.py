import hashlib

from pydantic import BaseModel


class BaseHashableModel(BaseModel):
    def compute_hash(self, attrs_to_exclude: set[str] | None = None) -> str:
        """Computes a unique hash based on the object's attributes."""
        # Use model_dump() to serialize the attributes
        serialized = "|".join(
            f"{key}={value}"
            for key, value in sorted(self.model_dump(exclude=attrs_to_exclude).items())
        )
        # Generate a SHA-256 hash
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
