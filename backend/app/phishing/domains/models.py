from ...extensions import db


class DomainModel(db.Model):
    __tablename__ = "domains"
    domain_name = db.Column(db.String(255), primary_key=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'domain_name': self.domain_name,
            'is_active': self.is_active
        } 