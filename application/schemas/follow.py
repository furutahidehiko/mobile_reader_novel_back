from pydantic import BaseModel, Field

class FollowResponse(BaseModel):
    is_success: bool = Field(..., title="お気に入り処理が成功してるかどうか")

    class Config:
        json_schema_extra = {
            "example": {
                "is_success": True
            }
        }