from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    last_login: Optional[datetime] = datetime.now()
    created_at: Optional[datetime] = datetime.now()
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0
    posts_count: Optional[int] = 0

class Post(BaseModel):
    user_id: str
    title: str
    content: str
    created_at: datetime
    likes_count: int
    comments_count: int
    tags: List[str]

class Comment(BaseModel):
    user_id: str
    post_id: str
    text: str
    created_at: datetime
    likes_count: int

class Like(BaseModel):
    user_id: str
    post_id: str
    created_at: datetime

class FollowUser(BaseModel):
    follower_user_id: str
    following_user_id: str
    created_at: datetime