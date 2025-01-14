from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy import and_, or_, select, extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Contact, Address
from src.schemas import ContactUpdate, ContactCreate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    def _base_query(self):
        """
        Base query for retrieving contacts.
        """
        return select(Contact)

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None
    ) -> List[Contact]:
        """
        Retrieve a list of contacts with optional search query and pagination.
        """
        filters = []
        if name:
            filters.append(Contact.name.ilike(f"%{name}%"))
        if surname:
            filters.append(Contact.surname.ilike(f"%{surname}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))

        stmt = (
            self._base_query()
            .options(selectinload(Contact.address))
            .filter(and_(*filters))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        Retrieve a single contact by ID with related address.
        """
        stmt = (
            self._base_query()
            .options(selectinload(Contact.address))
            .filter_by(id=contact_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_contact(self, body: ContactCreate) -> Contact:
        """
        Create a new contact with address.
        """
        address_data = body.address
        address = None
        if address_data:
            address = Address(**address_data.model_dump(exclude_unset=True))
            self.db.add(address)

        contact = Contact(
            **body.model_dump(exclude={"address"}, exclude_unset=True),
            address=address,
        )
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Optional[Contact]:
        """
        Remove a contact by ID.
        """
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            if contact.address:
              await self.db.delete(contact.address)
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Optional[Contact]:
        """
        Update contact details.
        """
        contact = await self.get_contact_by_id(contact_id)
        if not contact:
            return None

        for key, value in body.model_dump(exclude_unset=True, exclude={"address"}).items():
            setattr(contact, key, value)

        if body.address:
            if contact.address:
                for key, value in body.address.model_dump(exclude_unset=True).items():
                    setattr(contact.address, key, value)
            else:
                new_address = Address(**body.address.model_dump(exclude_unset=True))
                contact.address = new_address
                self.db.add(new_address)

        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        """
        Retrieve contacts with upcoming birthdays within a given number of days.
        """
        today = datetime.now().date()
        upcoming_date = today + timedelta(days=days)

        # Handle cross-month filtering
        stmt = self._base_query().filter(
            or_(
                # Birthdays in the current month
                and_(
                    extract("month", Contact.birthday) == today.month,
                    extract("day", Contact.birthday) >= today.day,
                ),
                # Birthdays in the next month
                and_(
                    extract("month", Contact.birthday) == upcoming_date.month,
                    extract("day", Contact.birthday) <= upcoming_date.day,
                ),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()