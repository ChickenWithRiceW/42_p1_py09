from enum import Enum
from pydantic import BaseModel, ValidationError, Field, model_validator
from datetime import datetime


class Rank(Enum):
    cadet = 0
    officer = 1
    lieutenant = 2
    captain = 3
    commander = 4


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    def _check_mission_id(self) -> None:
        if self.mission_id[0] != 'M':
            raise ValueError("Mission id must start with M")

    def _check_crew_rank(self) -> None:
        for member in self.crew:
            if member.rank == Rank.captain or member.rank == Rank.commander:
                break
        else:
            raise ValueError("Must have at least one Commander or Captain")
        return

    def _check_if_crew_is_active(self) -> None:
        for member in self.crew:
            if not member.is_active:
                raise ValueError("Members must all be active")

    def _check_mission(self) -> None:
        crew_count = 0
        if self.duration_days <= 365:
            return

        for member in self.crew:
            if member.years_experience >= 5:
                crew_count += 1
        if crew_count >= len(self.crew) / 2:
            return
        raise ValueError("at least 50% of Crew members need at least 5 "
                         "years of experience")

    @model_validator(mode='after')
    def verify(self) -> "SpaceMission":
        self._check_mission_id()
        self._check_crew_rank()
        self._check_if_crew_is_active()
        self._check_mission()
        return self


def main() -> None:
    crew = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.commander,
            age=45,
            specialization="Mission Command",
            years_experience=20,
            is_active=True,
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.lieutenant,
            age=38,
            specialization="Navigation",
            years_experience=12,
            is_active=True,
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.officer,
            age=31,
            specialization="Engineering",
            years_experience=8,
            is_active=True,
        ),
    ]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 6, 1),
        duration_days=900,
        crew=crew,
        mission_status="planned",
        budget_millions=2500.0,
    )

    print("Space Mission Crew Validation")
    print("=" * 41)
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.name}) - "
              f"{member.specialization}")
    print("=" * 41)

    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Doomed Mission",
            destination="Venus",
            launch_date=datetime(2024, 6, 1),
            duration_days=100,
            crew=[
                CrewMember(
                    member_id="CM010",
                    name="Bob Builder",
                    rank=Rank.cadet,
                    age=22,
                    specialization="Maintenance",
                    years_experience=1,
                    is_active=True,
                ),
            ],
            mission_status="planned",
            budget_millions=50.0,
        )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])


if __name__ == "__main__":
    main()
