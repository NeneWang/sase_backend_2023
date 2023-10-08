
from fastapi import APIRouter, Query
from datetime import datetime
from sqlalchemy import or_, and_
from database import SessionLocal
from typing import Optional
import models

db = SessionLocal()


router = APIRouter(
    prefix="/forum",
    responses={404: {"description": "Not found"}},
    tags=["Forum"]
)


@router.get("/", status_code=200)
async def getForums(string_filter: Optional[str] = Query(None)):
    if string_filter == "":
        forums = db.query(models.Thread).all()
        return forums
    forums = db.query(models.Thread).filter(
        and_(
            or_(models.Thread.title.ilike(f"%{string_filter}%"), models.Thread.body.ilike(f"%{string_filter}%")),
            models.Thread.is_forum == True
        )
        ).all()
    return forums

@router.post('/', status_code=201)
def createForum(forum: models.CreateForum):
    new_forum = models.Thread(
        is_forum=True,
        title=forum.title,
        body=forum.body,
        user_id=forum.user_id,
        created_time=datetime.now(),
        tags=forum.tags
    )
    db.add(new_forum)
    db.commit()
    db.refresh(new_forum)
    return new_forum

@router.get("/{forum_id}", status_code=200)
def getForum(forum_id: int):
    """Returns the forum details and an array of comments recurively

    Args:
        forum_id (int): The id of the forum

    """
    def getCommentsOfParentId(parent_id, depth=0, max_depth=10):
        if depth >= max_depth:
            return []

        forum_data = {}
        comments_list = []

        forum = db.query(models.Thread).filter(models.Thread.thread_id == forum_id).first()
        if not forum:
            return forum_data  # Return empty data if the forum does not exist

        comments = db.query(models.Thread).filter(models.Thread.parent_id == parent_id).all()

        for comment in comments:
            comment_data = getCommentsOfParentId(comment.thread_id, depth + 1, max_depth)
            comments_list.append(comment_data)

        forum_data["forum"] = forum
        forum_data["comments"] = comments_list

        return forum_data

    forum_data = getCommentsOfParentId(forum_id)
    return forum_data


@router.post("/comments", status_code=201)
def createComment(comment: models.CreateComment):
    """Creates a comment on a forum or thread

    Args:
        forum_id (int): The id of the forum or thread

    """
    new_comment = models.Thread(
        is_forum=False,
        body=comment.body,
        user_id=comment.user_id,
        parent_id=comment.parent_id,
        created_time=datetime.now(),
        tags=comment.tags
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment





