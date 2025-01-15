from fastapi import Depends, Cookie, Header, HTTPException, status, APIRouter
from app.schemas.config import Config
from app.bot import config


router = APIRouter()


@router.get("/{config_name}", response_model=Config)
async def get_config(config_name: str):
    return config[config_name]


@router.put("/{config_name}")
async def update_config(request: Config):
    # config.update({"answer_generation": True})
    return {"message": "Config updated successfully"}
