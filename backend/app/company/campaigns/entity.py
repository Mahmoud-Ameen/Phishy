from datetime import datetime


class Campaign:
    def __init__(
        self,
        id: int,
        name: str,
        start_date: datetime,
        started_by: str,
        scenario_id: int
    ):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.started_by = started_by
        self.scenario_id = scenario_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "started_by": self.started_by,
            "scenario_id": self.scenario_id
        }