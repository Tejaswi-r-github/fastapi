
HTTP_100_CONTINUE = 100  # Request received, continue


HTTP_200_OK = 200  # Request successful (GET)
HTTP_201_CREATED = 201  # Resource created (POST)
HTTP_202_ACCEPTED = 202  # Request accepted, processing later
HTTP_204_NO_CONTENT = 204  # Success but no response body (DELETE)


HTTP_400_BAD_REQUEST = 400  # Invalid input / bad request
HTTP_401_UNAUTHORIZED = 401  # Not logged in / invalid auth
HTTP_403_FORBIDDEN = 403  # No permission
HTTP_404_NOT_FOUND = 404  # Resource not found
HTTP_405_METHOD_NOT_ALLOWED = 405  # Wrong HTTP method
HTTP_409_CONFLICT = 409  # Duplicate data (e.g., email exists)
HTTP_422_UNPROCESSABLE_ENTITY = 422  # Validation error (FastAPI default)


HTTP_500_INTERNAL_SERVER_ERROR = 500  # Server crashed / unknown error
HTTP_502_BAD_GATEWAY = 502  # Invalid response from another server
HTTP_503_SERVICE_UNAVAILABLE = 503  # Server down / busy