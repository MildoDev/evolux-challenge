from src.base.models import BaseModel
from src.extensions import db


class Number(BaseModel):
    value = db.Column(db.String(), nullable=False, unique=True)
    monthyPrice = db.Column(db.Numeric, nullable=False)
    setupPrice = db.Column(db.Numeric, nullable=False)
    currency = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return self._repr(
            id=self.id,
            value=self.value,
            monthyPrice=self.monthyPrice,
            setupPrice=self.setupPrice,
            currency=self.currency,
        )
