from dataclasses import dataclass


@dataclass
class Campaign:
    id: int
    name: str
    start_date: str
    started_by: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date,
            "started_by": self.started_by,
        }