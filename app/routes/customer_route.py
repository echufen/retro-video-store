from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request 
from datetime import datetime


customers_bp = Blueprint("customers_bp",__name__, url_prefix="/customers")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    
    return model

def validate_num_queries(query_param):
    try:
        query_int = int(query_param)
    except:
        return False
    return True

#============================== customers_bp.route =============================
#============================================================================
#GET /customers
@customers_bp.route("", methods=["GET"])
def get_customers():
    sort_query = request.args.get("sort")
    if sort_query == "name":
        customer_query = Customer.query.order_by(Customer.name)
    elif sort_query == "registered_at":
        customer_query = Customer.query.order_by(Customer.registered_at)
    elif sort_query == "postal_code":
        customer_query = Customer.query.order_by(Customer.postal_code)
    else:
        customer_query = Customer.query.order_by(Customer.id)
    
    count_query = request.args.get("count")
    page_num_query = request.args.get("page_num")
    if validate_num_queries(count_query) and validate_num_queries(page_num_query):
        page = customer_query.paginate(page=int(page_num_query), per_page=int(count_query), error_out=False)
        customers_response = []

        for items in page.items:
            customers_response.append(items.to_dict())
        return jsonify(customers_response), 200
    
    if validate_num_queries(count_query) and not validate_num_queries(page_num_query):
        page = customer_query.paginate(per_page=int(count_query), error_out=False)
        customers = customer_query.all()
        customers_response = []

        for items in page.items:
            customers_response.append(items.to_dict())
        return jsonify(customers_response), 200

    
    response_body = []

    for customer in customer_query:
        response_body.append(customer.to_dict())
    return jsonify(response_body)

# POST /customers
@customers_bp.route("", methods=["POST"])
def create_customer():
    try:
        request_body = request.get_json()
        new_customer = Customer.from_dict(request_body)
    except:
        abort(make_response({"details":"Request body must include name.,Request body must include phone.,Request body must include postal_code."}, 400))

    db.session.add(new_customer)
    db.session.commit()
    
    response_body = new_customer.to_dict()
    return make_response(response_body, 201)
# GET /customers/<id>
@customers_bp.route("/<id>", methods=["GET"])
def get_customers_by_id(id):
    customer = validate_model(Customer, id)
    
    return jsonify(customer.to_dict())



# DELETE /customers/<id>
@customers_bp.route("/<id>", methods=["DELETE"])
def put_customers_by_id(id):
    customer = validate_model(Customer, id)

    db.session.delete(customer)
    db.session.commit()
    
    return jsonify(customer.to_dict()),200

# PUT /customers/<id>
@customers_bp.route("/<id>", methods=["PUT"])
def delete_customers_by_id(id):
    customer = validate_model(Customer, id)
    try:
        request_body = request.get_json()
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except:
        abort(make_response(jsonify("Bad Request"), 400))

    db.session.commit()
    
    return jsonify(customer.to_dict()),200


# `GET /customers/<id>/rentals`
@customers_bp.route("/<id>/rentals", methods=["GET"])
def get_rentals_by_customer_id(id):
    customer = validate_model(Customer, id)
    
    video_query = Rental.query.filter_by(customer_id=customer.id).join(Video)
    sort_query = request.args.get("sort")
    if sort_query == "title":
        rental_query = video_query.order_by(Video.title)
    else:
        rental_query = video_query.order_by(Video.id)
    count_query = request.args.get("count")
    page_num_query = request.args.get("page_num")

    if validate_num_queries(count_query) and validate_num_queries(page_num_query):

        page = video_query.paginate(page=int(page_num_query), per_page=int(count_query), error_out=False)
        video_result = []

        for items in page.items:
            video_result.append(items.video.to_dict())
        return jsonify(video_result), 200
    if validate_num_queries(count_query) and not validate_num_queries(page_num_query):
        page = video_query.paginate(per_page=int(count_query), error_out=False)
        video_result = []

        for items in page.items:
            video_result.append(items.video.to_dict())
        return jsonify(video_result), 200
        
    response_body = []
    for rental in rental_query:
        response_body.append({"title":rental.video.title,
                              "id":rental.video.id,
                              "total_inventory":rental.video.total_inventory})

    
    return jsonify(response_body)