from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.core.database import get_session
from src.core.security import hash_password, verify_password
from src.core.jwt import create_access_token
from src.models.user import User
from src.schemas.auth import UserSignup, UserSignin, AuthResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignup,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Register a new user account.

    - Validates email is unique
    - Hashes password with bcrypt
    - Creates user in database
    - Returns JWT token and user data
    """
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        name=user_data.name,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create JWT token
    token = create_access_token(new_user.id, new_user.email)

    # Return response
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(new_user),
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    credentials: UserSignin,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Authenticate user and return JWT token.

    - Validates email and password
    - Returns JWT token and user data
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    token = create_access_token(user.id, user.email)

    # Return response
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(user),
    )
