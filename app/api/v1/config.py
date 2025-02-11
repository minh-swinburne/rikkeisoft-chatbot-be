from fastapi import APIRouter, HTTPException, status, Depends, Path, Body
from fastapi.responses import JSONResponse
from app.api.dependencies import validate_access_token
from app.bot.config import load_config, save_config
from app.schemas import Config, ConfigUpdate, TokenModel


router = APIRouter()
authorized_roles = ["admin", "system_admin"]


@router.get("/{config_name}", response_model=Config)
async def get_config(
    config_name: str = Path(..., title="The name of the configuration section"),
    token_payload: TokenModel = Depends(validate_access_token),
):
    """Retrieve a specific configuration section."""
    # config_name = config_name.replace("-", "_")
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can access the configuration.",
        )

    config = load_config()
    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found.",
        )

    print(f"Loading config for: {config_name}")  # Debugging output
    return config[config_name]


@router.put("/{config_name}")
async def update_config(
    config_name: str = Path(...),
    updates: ConfigUpdate = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
):
    """Update a specific configuration section."""
    # config_name = config_name.replace("-", "_")
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can update the configuration.",
        )

    config = load_config()
    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found.",
        )

    print(f"Replacing config for: {config_name}")  # Debugging output
    print(updates)

    # Update the configuration section
    config[config_name]["system_prompt"] = updates.system_prompt
    config[config_name]["params"].update(
        {
            "model": updates.model,
            "max_tokens": updates.max_tokens,
            "temperature": updates.temperature,
        }
    )

    if updates.message_template:
        config[config_name]["message_template"] = updates.message_template

    save_config(config)

    return JSONResponse(
        {
            "success": True,
            "message": f"Config section '{config_name}' updated successfully.",
        }
    )


@router.get("/{config_name}/stream")
async def check_stream(
    config_name: str = Path(..., title="The name of the configuration section"),
    token_payload: TokenModel = Depends(validate_access_token),
) -> bool:
    """Check whether the configuration section supports streaming."""
    config = load_config()
    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found.",
        )

    print(f"Loading config for: {config_name}")  # Debugging output
    return config[config_name]["params"]["stream"]
