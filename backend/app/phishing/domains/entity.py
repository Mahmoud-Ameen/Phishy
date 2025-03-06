from dataclasses import dataclass


@dataclass
class PhishingDomain:
    domain_name: str
    is_active: bool

    def to_dict(self):
        return {
            'domain_name': self.domain_name,
            'is_active': self.is_active
        } 