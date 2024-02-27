from pydantic import BaseModel, Field

class FollowResponse(BaseModel):
    is_success: bool = Field(..., title="お気に入り登録してるかどうか")

    class Config:
        json_schema_extra = {
            "example": {
                "is_success": True
            }
        }