# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.snippet import Snippet  # noqa
from app.models.user import User  # noqa
from app.models.language import Language  # noqa
from app.models.link import Link  # noqa
from app.models.tag import Tag  # noqa
from app.models.tag_assign import TagAssign  # noqa
