# ensure models are imported so Base.metadata.create_all picks them up
from src.models import flagged_listings  # noqa
from src.models import disputes  # noqa
