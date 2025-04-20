from dataclasses import dataclass


@dataclass
class PhishingTemplate:
    id: int
    scenario_id: int
    subject: str
    content: str

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'subject': self.subject,
            'content': self.content
        }


@dataclass
class PhishingScenario:
    id: int
    name: str
    description: str | None
    level: int
    template: PhishingTemplate

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'template': self.template
        }

