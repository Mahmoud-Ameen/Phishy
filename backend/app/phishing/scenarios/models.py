from ...extensions import db


class TemplateModel(db.Model):
    """Template model for phishing emails."""
    __tablename__ = "phishing_templates"
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('phishing_scenarios.id'), nullable=False, unique=True)
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
    """Scenario model for phishing campaigns."""
    __tablename__ = "phishing_scenarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    level = db.Column(db.Integer, nullable=False)

    # Add relationship to TemplateModel (one-to-one)
    template = db.relationship("TemplateModel", backref="scenario", uselist=False, lazy="joined")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level
        }

