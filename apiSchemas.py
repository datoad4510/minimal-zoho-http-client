from typing import Optional, Any, Dict
from pydantic import BaseModel
from endpoints import Endpoints
from typing import Tuple, Type
# -------------------------
# Request/Response Schemas
# -------------------------

# Order to JSON
class OrderToJSONRequest(BaseModel):
    orderID: int

class OrderToJSONResponse(BaseModel):
    code: int
    result: Any

# Create Transaction
class CreateTransactionRequest(BaseModel):
    branch: str
    agent: str
    trType: str
    clientAcc: str
    status: str
    trDesc: str
    notes: Optional[str] = None


class CreateTransactionResponse(BaseModel):
    code: int
    result: Any


# Create Cash Order
class CreateCashOrderRequest(BaseModel):
    Order_Type_ID: str
    Client_Account_ID: str
    From_sum: float
    To_sum: float
    Client_Quote_Math: float
    Client_Quote_PC: float
    agent: str


class CreateCashOrderResponse(BaseModel):
    code: int
    result: Any


# Get Chat Client Accounts
class GetChatClientAccountsRequest(BaseModel):
    Telegram_Group_ID: str


class GetChatClientAccountsResponse(BaseModel):
    code: int
    result: Any


# Get Fav Routes
class GetFavRoutesRequest(BaseModel):
    route_category: str


class GetFavRoutesResponse(BaseModel):
    code: int
    result: Any


endpoint_schemas: Dict[Endpoints, Tuple[Type[BaseModel], Type[BaseModel]]] = {
    Endpoints.CREATE_TRANSACTION: (CreateTransactionRequest, CreateTransactionResponse),
    Endpoints.CREATE_CASH_ORDER: (CreateCashOrderRequest, CreateCashOrderResponse),
    Endpoints.GET_CHAT_CLIENT_ACCOUNTS: (GetChatClientAccountsRequest, GetChatClientAccountsResponse),
    Endpoints.GET_FAV_ROUTES: (GetFavRoutesRequest, GetFavRoutesResponse),
    Endpoints.ORDER_TO_JSON: (OrderToJSONRequest, OrderToJSONResponse),
}