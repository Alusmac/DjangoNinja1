from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Tag
from .schemas import PostIn, PostOut, CommentIn, CommentOut, TagOut
from .auth import SimpleBearerAuth

router = Router()
auth_scheme = SimpleBearerAuth()


def post_to_out(post: Post) -> PostOut:
    """ Post to out
    """
    return PostOut(
        id=post.id,
        author=post.author.username,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        updated_at=post.updated_at,
        tags=[TagOut(id=t.id, name=t.name) for t in post.tags.all()]
    )


def comment_to_out(comment: Comment) -> CommentOut:
    """ Comment to out
    """
    return CommentOut(
        id=comment.id,
        user=comment.user.username,
        text=comment.text,
        created_at=comment.created_at
    )


@router.post("/tags/", response=TagOut, auth=auth_scheme)
def create_tag(request, name: str) -> TagOut:
    """ Create tag
    """
    tag, _ = Tag.objects.get_or_create(name=name)
    return TagOut(id=tag.id, name=tag.name)


@router.get("/tags/", response=List[TagOut])
def list_tags(request) -> List[TagOut]:
    """ List tags
    """
    return [TagOut(id=t.id, name=t.name) for t in Tag.objects.all()]


@router.post("/posts/", response=PostOut, auth=auth_scheme)
def create_post(request, data: PostIn) -> PostOut:
    """ Create post
    """
    post = Post.objects.create(
        author=request.user,
        title=data.title,
        content=data.content
    )
    post.tags.set(data.tag_ids)
    return post_to_out(post)


@router.get("/posts/", response=List[PostOut])
def list_posts(request, tag: int = None, title: str = None) -> List[PostOut]:
    """ List posts
    """
    qs = Post.objects.all()
    if tag:
        qs = qs.filter(tags__id=tag)
    if title:
        qs = qs.filter(title__icontains=title)
    return [post_to_out(p) for p in qs.distinct()]


@router.get("/posts/{post_id}/", response=PostOut)
def get_post(request, post_id: int) -> PostOut:
    """ Get post
    """
    post = get_object_or_404(Post, id=post_id)
    return post_to_out(post)


@router.put("/posts/{post_id}/", response=PostOut, auth=auth_scheme)
def update_post(request, post_id: int, data: PostIn) -> PostOut:
    """ Update post
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)
    for attr, value in data.dict(exclude={"tag_ids"}).items():
        setattr(post, attr, value)
    post.tags.set(data.tag_ids)
    post.save()
    return post_to_out(post)


@router.delete("/posts/{post_id}/", auth=auth_scheme)
def delete_post(request, post_id: int):
    """ Delete post
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return {"success": True}


@router.post("/comments/", response=CommentOut, auth=auth_scheme)
def add_comment(request, data: CommentIn) -> CommentOut:
    """ Add comment
    """
    comment = Comment.objects.create(
        post_id=data.post_id,
        user=request.user,
        text=data.text
    )
    return comment_to_out(comment)


@router.get("/posts/{post_id}/comments/", response=List[CommentOut])
def list_comments(request, post_id: int) -> List[CommentOut]:
    """ List comments
    """
    comments = Comment.objects.filter(post_id=post_id)
    return [comment_to_out(c) for c in comments]
