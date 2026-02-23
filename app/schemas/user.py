from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    name: str
    student_id: str
    email: EmailStr
    password: str

    @field_validator('name', 'student_id', 'email', 'password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('empty string is not allowed')
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    student_id: str | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    bio: str | None = None
    baekjoon_id: str | None = None
    old_password: str | None = None
    new_password: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    student_id: str
    email: EmailStr
    bio: str | None = None
    role: str
    baekjoon_id: str | None = None
    tier: int | None = 0

    class Config:
        from_attributes = True


class ActivityLog(BaseModel):
    date: str
    count: int


class MyProfileResponse(BaseModel):
    name: str
    bio: str | None = None
    student_id: str
    tier: int | None = 0
    baekjoon_id: str | None = None
    monthly_grass_count: int
    total_grass_count: int
    current_streak: int
    activity_log: list[ActivityLog]
