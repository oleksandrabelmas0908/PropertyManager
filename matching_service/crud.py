from sqlalchemy import select, and_, or_, case
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
import logging

from models import Property, User, City
from schemas import PropertySchema
from db.engine import Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_and_set_matching_properties(
    session: Session,
    user_id: int,
) -> list[PropertySchema]:
    user = session.get(User, user_id)
    logger.info(f"Fetching matches for User: {user}")
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    select_stmt = (
        select(Property)
        .join(City, Property.city_id == City.id)
        .options(joinedload(Property.city))  # Eager load city relationship
        .where(
            and_(
                Property.city_id == user.city_id, 
                Property.bedrooms >= user.bedrooms, 
                Property.price <= user.max_budget,
                or_(
                    user.pets == False,
                    Property.pets == True
                )
            )
        )
        .order_by(
            case(
                (Property.pool == True, 0 if user.pool else 1),
                else_=1
            ),
            case(
                (Property.yard == True, 0 if user.yard else 1),
                else_=1
            ),
            case(
                (Property.parking == True, 0 if user.parking else 1),
                else_=1
            ),
        )
    )

    try:
        matches = session.scalars(select_stmt).all()
        logger.info(f"Found {len(matches)} matching properties for User ID {user_id}")
        
        # Convert to Pydantic schemas with city name
        matches_return = [
            PropertySchema(
                id=match.id,
                title=match.title,
                description=match.description,
                city=match.city.name,
                bedrooms=match.bedrooms,
                price=match.price,
                pets=match.pets,
                pool=match.pool,
                yard=match.yard,
                parking=match.parking
            ).model_dump()
            for match in matches
        ]
        
        # Now update the user's matches and commit
        user.matches = matches
        session.commit()

        return matches_return

    except Exception as e:
        logger.error(f"Error occurred while fetching matches for User ID {user_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


