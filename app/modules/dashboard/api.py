from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import Response

from app.core.auth.dependencies import set_dashboard_error_format, validate_dashboard_session
from app.core.openai.model_registry import get_model_registry, is_public_model
from app.core.utils.http_cache import conditional_json_response
from app.dependencies import DashboardContext, get_dashboard_context
from app.modules.dashboard.schemas import DashboardOverviewResponse, DashboardOverviewTimeframeKey

router = APIRouter(
    prefix="/api",
    tags=["dashboard"],
    dependencies=[Depends(validate_dashboard_session), Depends(set_dashboard_error_format)],
)


@router.get("/dashboard/overview", response_model=DashboardOverviewResponse)
async def get_overview(
    request: Request,
    timeframe: DashboardOverviewTimeframeKey = Query("7d"),
    context: DashboardContext = Depends(get_dashboard_context),
) -> Response:
    overview = await context.service.get_overview(timeframe)
    return conditional_json_response(request, overview)


@router.get("/models")
async def list_models(request: Request) -> Response:
    registry = get_model_registry()
    models_by_slug = registry.get_models_with_fallback()
    if not models_by_slug:
        return conditional_json_response(request, {"models": []})
    models = [
        {"id": slug, "name": model.display_name or slug}
        for slug, model in models_by_slug.items()
        if is_public_model(model, None)
    ]
    return conditional_json_response(request, {"models": models})
