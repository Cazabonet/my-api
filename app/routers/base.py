from typing import Type, TypeVar, Generic, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db

T = TypeVar('T')
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
ResponseSchema = TypeVar('ResponseSchema', bound=BaseModel)


class BaseRouter(Generic[T, CreateSchema, UpdateSchema, ResponseSchema]):
    def __init__(
        self,
        model: Type[T],
        create_schema: Type[CreateSchema],
        update_schema: Type[UpdateSchema],
        response_schema: Type[ResponseSchema],
        prefix: str,
        tags: List[str]
    ):
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._setup_routes()

    def _setup_routes(self):
        """Setup default CRUD routes."""
        
        @self.router.post("/", response_model=self.response_schema)
        async def create(
            item: self.create_schema,
            db: Session = Depends(get_db)
        ):
            """Create a new item."""
            try:
                db_item = self.model(**item.dict())
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                return db_item
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )

        @self.router.get("/", response_model=List[self.response_schema])
        async def read_all(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=100),
            db: Session = Depends(get_db)
        ):
            """Get all items with pagination."""
            items = db.query(self.model).offset(skip).limit(limit).all()
            return items

        @self.router.get("/{item_id}", response_model=self.response_schema)
        async def read_one(
            item_id: int,
            db: Session = Depends(get_db)
        ):
            """Get a specific item by ID."""
            item = db.query(self.model).filter(self.model.id == item_id).first()
            if not item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Item with id {item_id} not found"
                )
            return item

        @self.router.put("/{item_id}", response_model=self.response_schema)
        async def update(
            item_id: int,
            item: self.update_schema,
            db: Session = Depends(get_db)
        ):
            """Update an item."""
            db_item = db.query(self.model).filter(self.model.id == item_id).first()
            if not db_item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Item with id {item_id} not found"
                )
            
            try:
                for key, value in item.dict(exclude_unset=True).items():
                    setattr(db_item, key, value)
                db.commit()
                db.refresh(db_item)
                return db_item
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )

        @self.router.delete("/{item_id}")
        async def delete(
            item_id: int,
            db: Session = Depends(get_db)
        ):
            """Delete an item."""
            db_item = db.query(self.model).filter(self.model.id == item_id).first()
            if not db_item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Item with id {item_id} not found"
                )
            
            try:
                db.delete(db_item)
                db.commit()
                return {"message": "Item deleted successfully"}
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )

    def get_router(self) -> APIRouter:
        """Get the configured router."""
        return self.router 