from dataclasses import dataclass


@dataclass
class PhishingTemplate:
    id: int
    level: int
    subject: str
    content: str

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'subject': self.subject,
            'content': self.content
        }
