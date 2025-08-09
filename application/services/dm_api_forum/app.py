from typing import Annotated, Optional

from fastapi import APIRouter, Depends, FastAPI, Header, Path, Query, status

from application.clients.http.dm_api_forum.apis.comment_api import CommentApi
from application.clients.http.dm_api_forum.apis.forum_api import ForumApi
from application.clients.http.dm_api_forum.apis.topic_api import TopicApi
from application.clients.http.dm_api_forum.models.api_models import (
    Comment,
    CommentEnvelope,
    CommentListEnvelope,
    ForumEnvelope,
    ForumListEnvelope,
    Topic,
    TopicEnvelope,
    TopicListEnvelope,
    UserListEnvelope,
)
from application.dependency.dependency import get_http_comment_api, get_http_forum_api, get_http_topic_api
from application.utils import service_error_handler

app = FastAPI(
    title="DM API Forum",
)

comment_router = APIRouter(
    tags=["Comment"],
)

forum_router = APIRouter(
    tags=["Forum"],
)

topic_router = APIRouter(
    tags=["Topic"],
)


@comment_router.get(
    "/v1/forum/comments/{id}",
    response_model=CommentEnvelope,
    summary="Get comment",
    operation_id="GetForumComment",
)
async def get_forum_comment(
    id: str = Path(..., description="Comment ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    comment_api: CommentApi = Depends(get_http_comment_api),  # noqa: B008
) -> CommentEnvelope:
    async with service_error_handler():
        return await comment_api.get_v1_forum_comments_id(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@comment_router.patch(
    "/v1/forum/comments/{id}",
    response_model=CommentEnvelope,
    summary="Update comment",
    operation_id="PutForumComment",
)
async def put_forum_comment(
    id: str = Path(..., description="Comment ID"),
    comment: Comment = None,
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    comment_api: CommentApi = Depends(get_http_comment_api),  # noqa: B008
) -> CommentEnvelope:
    async with service_error_handler():
        return await comment_api.patch_v1_forum_comments_id(
            id_=id,
            comment=comment,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@comment_router.delete(
    "/v1/forum/comments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete comment",
    operation_id="DeleteForumComment",
)
async def delete_forum_comment(
    id: str = Path(..., description="Comment ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    comment_api: CommentApi = Depends(get_http_comment_api),  # noqa: B008
):
    async with service_error_handler():
        await comment_api.delete_v1_forum_comments_id(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


@comment_router.post(
    "/v1/forum/comments/{id}/likes",
    status_code=status.HTTP_201_CREATED,
    summary="Post new like",
    operation_id="PostForumCommentLike",
)
async def post_forum_comment_like(
    id: str = Path(..., description="Comment ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    comment_api: CommentApi = Depends(get_http_comment_api),  # noqa: B008
):
    async with service_error_handler():
        return await comment_api.post_v1_forum_comments_id__likes(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


@comment_router.delete(
    "/v1/forum/comments/{id}/likes",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete like",
    operation_id="DeleteForumCommentLike",
)
async def delete_forum_comment_like(
    id: str = Path(..., description="Comment ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    comment_api: CommentApi = Depends(get_http_comment_api),  # noqa: B008
):
    async with service_error_handler():
        await comment_api.delete_v1_forum_comments_id__likes(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


# Forum endpoints
@forum_router.get(
    "/v1/fora",
    response_model=ForumListEnvelope,
    summary="Get list of available fora",
    operation_id="GetFora",
)
async def get_fora(
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    forum_api: ForumApi = Depends(get_http_forum_api),  # noqa: B008
) -> ForumListEnvelope:
    async with service_error_handler():
        return await forum_api.get_v1_fora(
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@forum_router.get(
    "/v1/fora/{id}",
    response_model=ForumEnvelope,
    summary="Get certain forum",
    operation_id="GetForum",
)
async def get_forum(
    id: str = Path(..., description="Forum ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    forum_api: ForumApi = Depends(get_http_forum_api),  # noqa: B008
) -> ForumEnvelope:
    async with service_error_handler():
        return await forum_api.get_v1_fora_id(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@forum_router.delete(
    "/v1/fora/{id}/comments/unread",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark forum comments as read",
    operation_id="DeleteForumCommentsUnread",
)
async def delete_forum_comments_unread(
    id: str = Path(..., description="Forum ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    forum_api: ForumApi = Depends(get_http_forum_api),  # noqa: B008
):
    async with service_error_handler():
        await forum_api.delete_v1_fora_id__comments_unread(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


@forum_router.get(
    "/v1/fora/{id}/moderators",
    response_model=UserListEnvelope,
    summary="Get list of forum moderators",
    operation_id="GetForumModerators",
)
async def get_forum_moderators(
    id: str = Path(..., description="Forum ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    forum_api: ForumApi = Depends(get_http_forum_api),  # noqa: B008
) -> UserListEnvelope:
    async with service_error_handler():
        return await forum_api.get_v1_fora_id__moderators(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@forum_router.get(
    "/v1/fora/{id}/topics",
    response_model=TopicListEnvelope,
    summary="Get list of forum topics",
    operation_id="GetForumTopics",
)
async def get_forum_topics(
    id: str = Path(..., description="Forum ID"),
    skip: Optional[int] = Query(None, description="Number of topics to skip"),
    size: Optional[int] = Query(None, description="Number of topics to take"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    forum_api: ForumApi = Depends(get_http_forum_api),  # noqa: B008
) -> TopicListEnvelope:
    async with service_error_handler():
        return await forum_api.get_v1_fora_id__topics(
            id_=id,
            skip=skip,
            size=size,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@forum_router.post(
    "/v1/fora/{id}/topics",
    response_model=TopicEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Post new topic",
    operation_id="PostForumTopic",
)
async def post_forum_topic(
    id: str = Path(..., description="Forum ID"),
    topic: Topic = None,
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    forum_api: ForumApi = Depends(get_http_forum_api),  # noqa: B008
) -> TopicEnvelope:
    async with service_error_handler():
        return await forum_api.post_v1_fora_id__topics(
            id_=id,
            topic=topic,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


# Topic endpoints
@topic_router.get(
    "/v1/topics/{id}",
    response_model=TopicEnvelope,
    summary="Get certain topic",
    operation_id="GetTopic",
)
async def get_topic(
    id: str = Path(..., description="Topic ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
) -> TopicEnvelope:
    async with service_error_handler():
        return await topic_api.get_v1_topics_id(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@topic_router.patch(
    "/v1/topics/{id}",
    response_model=TopicEnvelope,
    summary="Put topic changes",
    operation_id="PutTopic",
)
async def put_topic(
    id: str = Path(..., description="Topic ID"),
    topic: Topic = None,
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
) -> TopicEnvelope:
    async with service_error_handler():
        return await topic_api.patch_v1_topics_id(
            id_=id,
            topic=topic,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@topic_router.delete(
    "/v1/topics/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete topic",
    operation_id="DeleteTopic",
)
async def delete_topic(
    id: str = Path(..., description="Topic ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
):
    async with service_error_handler():
        await topic_api.delete_v1_topics_id(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


@topic_router.post(
    "/v1/topics/{id}/likes",
    status_code=status.HTTP_201_CREATED,
    summary="Post new like",
    operation_id="PostTopicLike",
)
async def post_topic_like(
    id: str = Path(..., description="Topic ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
):
    async with service_error_handler():
        return await topic_api.post_v1_topics_id__likes(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


@topic_router.delete(
    "/v1/topics/{id}/likes",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete like",
    operation_id="DeleteTopicLike",
)
async def delete_topic_like(
    id: str = Path(..., description="Topic ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
):
    async with service_error_handler():
        await topic_api.delete_v1_topics_id__likes(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


@topic_router.get(
    "/v1/topics/{id}/comments",
    response_model=CommentListEnvelope,
    summary="Get list of topic comments",
    operation_id="GetTopicComments",
)
async def get_topic_comments(
    id: str = Path(..., description="Topic ID"),
    skip: Optional[int] = Query(None, description="Number of comments to skip"),
    size: Optional[int] = Query(None, description="Number of comments to take"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
) -> CommentListEnvelope:
    async with service_error_handler():
        return await topic_api.get_v1_topics_id__comments(
            id_=id,
            skip=skip,
            size=size,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@topic_router.post(
    "/v1/topics/{id}/comments",
    response_model=CommentEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Post new comment",
    operation_id="PostTopicComment",
)
async def post_topic_comment(
    id: str = Path(..., description="Topic ID"),
    comment: Comment = None,
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    x_dm_bb_render_mode: Annotated[str | None, Header(alias="X-Dm-Bb-Render-Mode")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
) -> CommentEnvelope:
    async with service_error_handler():
        return await topic_api.post_v1_topics_id__comments(
            id_=id,
            comment=comment,
            x_dm_auth_token=x_dm_auth_token or "",
            x_dm_bb_render_mode=x_dm_bb_render_mode or "",
        )


@topic_router.delete(
    "/v1/topics/{id}/comments/unread",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark topic comments as read",
    operation_id="DeleteTopicCommentsUnread",
)
async def delete_topic_comments_unread(
    id: str = Path(..., description="Topic ID"),
    x_dm_auth_token: Annotated[str | None, Header(alias="X-Dm-Auth-Token")] = None,
    topic_api: TopicApi = Depends(get_http_topic_api),  # noqa: B008
):
    async with service_error_handler():
        await topic_api.delete_v1_topics_id__comments_unread(
            id_=id,
            x_dm_auth_token=x_dm_auth_token or "",
        )


app.include_router(comment_router)
app.include_router(forum_router)
app.include_router(topic_router)
