from fastapi import Depends, Cookie, Header, HTTPException, status, APIRouter
from app.schemas.config import Config, ConfigUpdate
from app.bot import config, save_config


router = APIRouter()


@router.get("/{config_name}", response_model=Config)
async def get_config(config_name: str):
    """Retrieve a specific configuration section."""
    # config_name = config_name.replace("-", "_")

    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found."
        )

    print(f"Loading config for: {config_name}")  # Debugging output
    return config[config_name]


@router.put("/{config_name}")
async def update_config(config_name: str, updates: ConfigUpdate):
    """Update a specific configuration section."""
    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found."
        )

    print(f"Replacing config for: {config_name}")  # Debugging output
    print(updates)

    # Update the configuration section
    config[config_name]["system_prompt"] = updates.system_prompt
    config[config_name]["params"].update({
        "model": updates.model,
        "max_tokens": updates.max_tokens,
        "temperature": updates.temperature,
    })

    if updates.message_template:
        config[config_name]["message_template"] = updates.message_template

    save_config()

    return {"message": f"Config section '{config_name}' updated successfully."}


# @router.get("/all", response_model=Config)
# async def get_all_configs():
#     """Retrieve the entire configuration."""
#     return config
