from fastapi import APIRouter, HTTPException, status, Depends, Path, Query, Body
from fastapi.responses import JSONResponse
from app.api.dependencies import validate_access_token
from app.bot.config import load_config, save_config
from app.schemas import Config, ConfigUpdate, TokenModel


router = APIRouter()
authorized_roles = ["admin", "system_admin"]


@router.get("")
async def list_configs(token_payload: TokenModel = Depends(validate_access_token)):
    """List all available configuration sections."""
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can access the configuration.",
        )

    config = load_config()
    return [key for key in config.keys() if key != "timeout"]


@router.get("/{config_name}", response_model=Config)
async def get_config(
    config_name: str = Path(..., title="The name of the configuration section"),
    tab: str = Query(
        "general",
        title="The tab to display in the configuration editor (for Answer Generation only)",
    ),
    refresh: bool = Query(False, title="Refresh the configuration from S3"),
    token_payload: TokenModel = Depends(validate_access_token),
):
    """Retrieve a specific configuration section."""
    # config_name = config_name.replace("-", "_")
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can access the configuration.",
        )

    config = load_config(refresh)
    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found.",
        )

    print(f"Loading config for: {config_name}")  # Debugging output
    # print(config[config_name])  # Debugging output
    return (
        config[config_name][tab]
        if config_name == "answer_generation" and tab
        else config[config_name]
    )


@router.put("/{config_name}")
async def update_config(
    config_name: str = Path(...),
    tab: str = Query("general"),
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

    # Debugging output
    # print(f"Replacing config for: {config_name}")
    # print(updates)
    config_section = (
        config[config_name][tab]
        if config_name == "answer_generation"
        else config[config_name]
    )

    # Update the configuration section
    config_section["system_prompt"] = updates.system_prompt
    config_section["params"].update(
        {
            "model": updates.model,
            "max_tokens": updates.max_tokens,
            "temperature": updates.temperature,
            "stream": updates.stream,
        }
    )

    if updates.message_template:
        config_section["message_template"] = updates.message_template
    if updates.length_limit:
        config_section["length_limit"] = updates.length_limit

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
    tab: str = Query("general"),
    token_payload: TokenModel = Depends(validate_access_token),
) -> bool:
    """Check whether the configuration section supports streaming."""
    config = load_config()
    if config_name not in config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config section '{config_name}' not found.",
        )

    # print(f"Loading config for: {config_name}")  # Debugging output
    return (
        config[config_name][tab]["params"]["stream"]
        if config_name == "answer_generation"
        else config[config_name]["params"]["stream"]
    )
