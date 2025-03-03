from ...extensions import db


class TemplateModel(db.Model):
    __tablename__ = "phishing_templates"
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Text)
    content = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'subject': self.subject,
            'content': self.content
        }
