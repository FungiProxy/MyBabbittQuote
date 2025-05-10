"""
Service for managing customers.
"""
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session

from src.core.models import Customer
from src.utils.db_utils import add_and_commit, get_by_id, get_all, update_and_commit, delete_and_commit


class CustomerService:
    """Service for managing customers."""
    
    @staticmethod
    def create_customer(
        db: Session,
        name: str,
        company: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Customer:
        """
        Create a new customer.
        
        Args:
            db: Database session
            name: Customer name
            company: Company name
            email: Contact email
            phone: Contact phone number
            address: Street address
            city: City
            state: State/province
            zip_code: Postal/zip code
            notes: Additional notes
            
        Returns:
            Newly created Customer object
        """
        customer = Customer(
            name=name,
            company=company,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            notes=notes
        )
        
        return add_and_commit(db, customer)
    
    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
        """
        Get a customer by ID.
        
        Args:
            db: Database session
            customer_id: ID of the customer
            
        Returns:
            Customer object if found, None otherwise
        """
        return get_by_id(db, Customer, customer_id)
    
    @staticmethod
    def get_all_customers(db: Session) -> List[Customer]:
        """
        Get all customers.
        
        Args:
            db: Database session
            
        Returns:
            List of all Customer objects
        """
        return get_all(db, Customer)
    
    @staticmethod
    def search_customers(db: Session, search_term: str) -> List[Customer]:
        """
        Search for customers by name, company, or email.
        
        Args:
            db: Database session
            search_term: Search term to match against name, company, or email
            
        Returns:
            List of matching Customer objects
        """
        search_pattern = f"%{search_term}%"
        return db.query(Customer).filter(
            (Customer.name.ilike(search_pattern)) |
            (Customer.company.ilike(search_pattern)) |
            (Customer.email.ilike(search_pattern))
        ).all()
    
    @staticmethod
    def update_customer(
        db: Session,
        customer_id: int,
        values: Dict[str, Any]
    ) -> Optional[Customer]:
        """
        Update a customer's information.
        
        Args:
            db: Database session
            customer_id: ID of the customer to update
            values: Dictionary of values to update
            
        Returns:
            Updated Customer object if found, None otherwise
        """
        customer = get_by_id(db, Customer, customer_id)
        if not customer:
            return None
        
        return update_and_commit(db, customer, values)
    
    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        """
        Delete a customer.
        
        Args:
            db: Database session
            customer_id: ID of the customer to delete
            
        Returns:
            True if customer was deleted, False otherwise
            
        Note:
            This will fail if the customer has associated quotes
        """
        customer = get_by_id(db, Customer, customer_id)
        if not customer:
            return False
        
        return delete_and_commit(db, customer) 