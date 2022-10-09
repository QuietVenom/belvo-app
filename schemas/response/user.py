from models import RoleType
from schemas.base import BaseUser


class UserOut(BaseUser):
    id: int
    first_name: str
    last_name: str
    role: RoleType
