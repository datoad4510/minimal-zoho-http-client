from enum import Enum

class Endpoints(Enum):
    HELLO_WORLD_TEST = "HelloWorld_TEST"
    CREATE_TRANSACTION = "Create_Transaction"
    CREATE_CASH_ORDER = "Create_Cash_Order"
    GET_CHAT_CLIENT_ACCOUNTS = "Get_Chat_Client_Accounts"
    GET_FAV_ROUTES = "Get_Fav_Routes"
    ORDER_TO_JSON = "Order_To_JSON"


    # override the __str__ method to return the value of the enum
    def __str__(self):
        return self.value