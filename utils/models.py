from django.db import models
from .snowflake import Snowflake

class BaseModel(models.Model):
    """Base model with id attribute for all models requiring a snowflake id"""

    id = models.BigIntegerField(
        primary_key=True,
        default=Snowflake(2, 2).generate_id,
        editable=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

