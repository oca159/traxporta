from typing import List, Optional, Union
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.api.dtos.url import UrlRead, UrlCreate, UrlUpdate
from containers import Container
from domain.services.url import UrlService

router = APIRouter(
    prefix="/urls",
    tags=["Urls"],
)


@router.get("", response_model=List[UrlRead])
@inject
async def get_urls(
    *,
    shortcode: Optional[str] = None,
    url_service: UrlService = Depends(Provide[Container.url_service])
):
    if shortcode:
        return [url_service.get_url_by_shortcode(shortcode)]
    return url_service.get_urls()


@router.get("/{url_id}", response_model=UrlRead)
@inject
async def get_url(
    url_id: int,
    url_service: UrlService = Depends(Provide[Container.url_service])
):
    url = url_service.get_url_by_id(url_id)
    return url


@router.post("", response_model=UrlRead)
@inject
async def create_url(
    url: UrlCreate,
    url_service: UrlService = Depends(Provide[Container.url_service])
):
    created_url = url_service.create_url(url)
    return UrlRead.from_orm(created_url)


@router.patch("/{url_id}", response_model=UrlRead)
@inject
async def update_url(
    url_id: int,
    url: UrlUpdate,
    url_service: UrlService = Depends(Provide[Container.url_service])
):
    updated_url = url_service.update_url(url_id, url)
    return UrlRead.from_orm(updated_url)


@router.delete("/{url_id}", status_code=204)
@inject
async def delete_url(
    url_id: int,
    url_service: UrlService = Depends(Provide[Container.url_service])
):
    url_service.delete_url(url_id)
