from pydantic import BaseModel, ValidationError, Field
from typing import Optional
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")

    iss = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=7,
        power_level=23.12,
        oxygen_level=40.00,
        last_maintenance=datetime(2026, 4, 15),
        is_operational=True
    )
    print("========================================")
    print("Valid station created:", end='')
    if iss.is_operational:
        temp = "Operational"
    else:
        temp = "Not operational"

    print(f"""
ID:             {iss.station_id}
Name:           {iss.name}
Crew:           {iss.crew_size} people
Power:          {iss.power_level}%
Oxygen:         {iss.oxygen_level}%
Maintenance:    {iss.last_maintenance}
Status:         {temp}
Notes:          {iss.notes or 'None'}
========================================\
    """)

    print("Expected validation error:")
    try:
        # Ignores that its unused
        _ = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            power_level=23.12,
            oxygen_level=40.00,
            last_maintenance=datetime(2026, 4, 15),
            is_operational=True
        )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])


if __name__ == "__main__":
    main()
