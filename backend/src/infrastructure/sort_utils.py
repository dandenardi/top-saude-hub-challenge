from sqlalchemy import asc, desc
from typing import Dict, Tuple

def parse_sort(sort: str, allowed: Dict[str, object], tie_breaker: Tuple[object, object]):
    
    try:
        field, direction = sort.split(":", 1)
    except ValueError:
        field, direction = "created_at", "desc"

    col = allowed.get(field, allowed.get("created_at"))
    is_asc = (direction or "").lower() == "asc"
    primary = asc(col) if is_asc else desc(col)

    tb_asc, tb_desc = tie_breaker  
    secondary = tb_asc if is_asc else tb_desc

    return primary, secondary
