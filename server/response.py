from flask import jsonify, make_response

def response_token(token):
    resp_message = jsonify({"Token": token, "ResponseCode": 0, "ResponseMessage": "Success"})
    resp = make_response(resp_message)
    resp.status_code = 200
    return resp

def response_error_no_token():
    resp_message = jsonify({"Token": "", "ResponseCode": 1, "ResponseMessage": "No token supplied"})
    resp = make_response(resp_message)
    resp.status_code = 401
    return resp

def response_error_invalid_token():
    resp_message = jsonify({"Token": "", "ResponseCode": 2, "ResponseMessage": "Invalid token"})
    resp = make_response(resp_message)
    resp.status_code = 403
    return resp

def response_error_no_password():
    resp_message = jsonify({"Token": "", "ResponseCode": 3, "ResponseMessage": "No password supplied"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_wrong_password():
    resp_message = jsonify({"Token": "", "ResponseCode": 4, "ResponseMessage": "Wrong password"})
    resp = make_response(resp_message)
    resp.status_code = 403
    return resp

def response_document(document_id):
    resp_message = jsonify({"DocumentID": document_id, "ResponseCode": 0, "ResponseMessage": "Success"})
    resp = make_response(resp_message)
    resp.status_code = 200
    return resp

def response_error_filename_exists():
    resp_message = jsonify({"DocumentID": "", "ResponseCode": 1, "ResponseMessage": "Filename already exists"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_no_file():
    resp_message = jsonify({"DocumentID": "", "ResponseCode": 2, "ResponseMessage": "No file supplied"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

