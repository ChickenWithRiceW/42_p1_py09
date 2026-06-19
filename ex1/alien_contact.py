from enum import Enum
from pydantic import BaseModel, ValidationError, Field, model_validator
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    radio = 0
    visual = 1
    physical = 2
    telepathic = 3


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.00)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = False

    def _check_contact_id(self) -> None:
        if self.contact_id[0:2] != "AC":
            raise ValueError("Contact ID must start with AC")

    def _verify_physical_report(self) -> None:
        if self.contact_type == ContactType.physical:
            if not self.is_verified:
                raise ValueError("Physical contact must be verified")

    def _check_telepathic_witness_count(self) -> None:
        if self.contact_type == ContactType.telepathic:
            if self.witness_count < 3:
                raise ValueError("Telepathic contact requires at least"
                                 " 3 witnesses")

    def _check_strong_signal_message(self) -> None:
        if self.signal_strength > 7.0:
            if self.message_received is None:
                raise ValueError("Strong signal should include message")

    @model_validator(mode="after")
    def validation_method(self):
        self._check_contact_id()
        self._verify_physical_report()
        self._check_telepathic_witness_count()
        self._check_strong_signal_message()
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    alien_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 4, 15),
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Its Alf, you got a cat?",
        is_verified=True
    )
    print(f"""\
======================================
Valid contact report:
ID:                 {alien_contact.contact_id}
Time of contact:    {alien_contact.timestamp}
Location:           {alien_contact.location}
Contact type:       {alien_contact.contact_type}
Signal:             {alien_contact.signal_strength}/10
Duration:           {alien_contact.duration_minutes} minutes
Witnesses:          {alien_contact.witness_count}
message_received:   {alien_contact.message_received}
Got verified:       {alien_contact.is_verified}
======================================\
""")

    print("Expected validation error:")
    try:
        _ = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 4, 15),
            location="Area 51, Nevada",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Its Alf, you got a cat?",
            is_verified=True
        )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])


if __name__ == "__main__":
    main()
