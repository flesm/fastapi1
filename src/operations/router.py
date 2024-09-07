import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import Operation
from src.operations.schemas import OperationCreate

from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/")
# same structure of response
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.execute(query)  # tuple
        return {
            'status': 'success',
            'data': result.scalars().all(),  # scalars allows to make variable dict
            'details': None,
        }
    except Exception:
        # send error to logs
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.model_dump())
    await session.execute(stmt)  # create transaction
    await session.commit()  # commiting all transaction (all or nothing)
    return {"status": "success"}


@router.get("/long_operations")
@cache(expire=60)
async def get_long_op():
    time.sleep(2)
    return "A lot of operations, that we have cached"
