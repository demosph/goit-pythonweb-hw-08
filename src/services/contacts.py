from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate
from fastapi import HTTPException, status


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactCreate):
      contact = await self.contact_repository.create_contact(body)
      if not contact:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create contact"
        )
      return contact

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None
    ):
        return await self.contact_repository.get_contacts(
            skip, limit, name, surname, email
        )

    async def get_upcoming_birthdays(self, days: int = 7):
        return await self.contact_repository.get_upcoming_birthdays(days)

    async def get_contact(self, contact_id: int):
        contact = await self.contact_repository.get_contact_by_id(contact_id)
        if contact is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
            )
        return contact

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        contact = await self.contact_repository.update_contact(contact_id, body)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
            )
        return contact

    async def remove_contact(self, contact_id: int):
        contact = await self.contact_repository.remove_contact(contact_id)
        if contact is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
            )
        return contact