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
    student_id: str
