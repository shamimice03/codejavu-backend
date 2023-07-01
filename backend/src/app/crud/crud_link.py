from app.crud.base import CRUDBase
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkUpdate


class CRUDLink(CRUDBase[Link, LinkCreate, LinkUpdate]):
    pass


link = CRUDLink(Link)
