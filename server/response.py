from flask import jsonify, make_response

def response_token(token):
    resp_message = jsonify({"Data": {"Token": token}, "ResponseCode": 0, "ResponseMessage": "Success"})
    resp = make_response(resp_message)
    resp.status_code = 200
    return resp

def response_document(document_id):
    resp_message = jsonify({"Data": {"DocumentID": document_id}, "ResponseCode": 0, "ResponseMessage": "Success"})
    resp = make_response(resp_message)
    resp.status_code = 200
    return resp

def response_qr(qr_code):
    resp_message = jsonify({"Data": {"Base64QR": qr_code}, "ResponseCode": 0, "ResponseMessage": "Success"})
    resp = make_response(resp_message)
    resp.status_code = 200
    return resp

def response_documents(documents):
    resp_message = jsonify({"Data": {"Documents": documents}, "ResponseCode": 0, "ResponseMessage": "Success"})
    resp = make_response(resp_message)
    resp.status_code = 200
    return resp

def response_error_no_token():
    resp_message = jsonify({"Data": {}, "ResponseCode": 1, "ResponseMessage": "No token supplied"})
    resp = make_response(resp_message)
    resp.status_code = 401
    return resp

def response_error_invalid_token():
    resp_message = jsonify({"Data": {}, "ResponseCode": 2, "ResponseMessage": "Invalid token"})
    resp = make_response(resp_message)
    resp.status_code = 403
    return resp

def response_error_no_password():
    resp_message = jsonify({"Data": {}, "ResponseCode": 3, "ResponseMessage": "No password supplied"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_wrong_password():
    resp_message = jsonify({"Data": {}, "ResponseCode": 4, "ResponseMessage": "Wrong password"})
    resp = make_response(resp_message)
    resp.status_code = 403
    return resp

def response_error_filename_exists():
    resp_message = jsonify({"Data": {}, "ResponseCode": 5, "ResponseMessage": "Filename already exists"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_no_file():
    resp_message = jsonify({"Data": {}, "ResponseCode": 6, "ResponseMessage": "No file supplied"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_not_supported():
    resp_message = jsonify({"Data": {}, "ResponseCode": 7, "ResponseMessage": "Request format not supported, use JSON"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_no_document_id():
    resp_message = jsonify({"Data": {}, "ResponseCode": 8, "ResponseMessage": "No document ID supplied"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp

def response_error_invalid_document_id():
    resp_message = jsonify({"Data": {}, "ResponseCode": 9, "ResponseMessage": "Invalid document ID"})
    resp = make_response(resp_message)
    resp.status_code = 400
    return resp
