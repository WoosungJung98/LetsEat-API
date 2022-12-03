from flask import current_app as app
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required

from main.controllers.restaurant import (
    restaurant_bp,
    API_CATEGORY,
    authorization_header
)
from main.controllers.common.jwt import check_jwt_user
from main.controllers.common.common import (
    get_page_offset,
    check_pagination_request,
    convert_query_to_response,
    gen_random_uid
)
from main.models.common.error import (
    ResponseError,
    ERROR_BUSINESS_ID_NOT_EXISTS_PATH,
    ERROR_REVIEW_CREATE_FAILED,
    SUCCESS_REVIEW_CREATE
)
from main.models.schema.review import (
    RequestRestaurantReviewListSchema,
    RequestRestaurantReviewCreateSchema,
    ResponseRestaurantReviewListSchema
)
from main.models.review import t_review
from main.models.user import t_user
from main.models.business import get_restaurant
from main import db
from sqlalchemy import func


@restaurant_bp.route("/<string:business_id>/reviews", methods=["GET"])
@use_kwargs(RequestRestaurantReviewListSchema, location="query")
@marshal_with(ResponseError)
@marshal_with(ResponseRestaurantReviewListSchema, code=200)
@doc(
    tags=[API_CATEGORY],
    summary="Get Restaurant Reviews",
    description="Returns the list of reviews for a restaurant"
)
@check_pagination_request
def restaurant_reviews(page, length, business_id, stars):
    query = db.session.query(
        t_user.c.user_name,
        t_review.c.stars,
        t_review.c.body,
        t_review.c.useful,
        t_review.c.funny,
        t_review.c.cool,
        t_review.c.created_at)\
    .join(t_user, t_review.c.user_id == t_user.c.user_id)\
    .filter(t_review.c.business_id == business_id)

    if stars:
        query = query.filter(t_review.c.stars == stars)

    total_length = query.count()

    query = query.order_by(t_review.c.created_at.desc())

    if length > 0:
        page_offset = get_page_offset(page, length)
        query = query.offset(page_offset)\
                     .limit(length)

    result = query.all()

    attrs = ("user_name", "stars", "body", "useful", "funny", "cool", "created_at")
    return {
        "review": {
            "list": convert_query_to_response(attrs, result),
            "page": page,
            "total_length": total_length
        }
    }


@restaurant_bp.route("/<string:business_id>/review-create", methods=["POST"])
@jwt_required()
@check_jwt_user
@use_kwargs(RequestRestaurantReviewCreateSchema)
@marshal_with(ResponseError)
@doc(
    tags=[API_CATEGORY],
    summary="Create Restaurant Reviews",
    description="Creates a review for a restaurant",
    params=authorization_header
)
def restaurant_review_create(user, business_id, body, stars):
    restaurant = get_restaurant(business_id)
    if not restaurant:
        return ERROR_BUSINESS_ID_NOT_EXISTS_PATH.get_response()

    random_uid = None
    while True:
        random_uid = gen_random_uid()
        query = db.session.query(t_review.c.review_id).filter(t_review.c.review_id == random_uid)
        if not db.session.query(query.exists()).scalar():
            break

    try:
        review_create_query = db.insert(t_review)\
            .values(review_id = random_uid, user_id = user.user_id, business_id = business_id,
                    body = body, stars = stars, useful = 0, funny = 0, cool = 0,
                    created_at = func.now(), updated_at = func.now())
        db.session.execute(review_create_query)
        db.session.commit()
    except:
        return ERROR_REVIEW_CREATE_FAILED.get_response()

    return SUCCESS_REVIEW_CREATE.get_response()    
