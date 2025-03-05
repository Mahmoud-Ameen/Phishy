from ...extensions import db


class TemplateModel(db.Model):
    __tablename__ = "phishing_templates"
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('phishing_scenarios.id'), nullable=False)
    subject = db.Column(db.Text)
    content = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'subject': self.subject,
            'content': self.content
        }


class ScenarioModel(db.Model):
    __tablename__ = "phishing_scenarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    level = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level
        }


class DomainModel(db.Model):
    __tablename__ = "domains"
    domain_name = db.Column(db.String(255), primary_key=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'domain_name': self.domain_name,
            'is_active': self.is_active
        }

