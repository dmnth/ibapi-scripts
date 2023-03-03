from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import *
from ibapi.order import *
import threading
import time

# why
reqId = 0

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.df = None
        self.prev_close = None
        self.positions = {}

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)
        key = (contract.conId, contract.exchange)
        print(key, position, avgCost)
        self.positions[key] = (position, avgCost)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        print("Setting nextValidOrderId: ", orderId)
        self.nextValidOrderId = orderId

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        self.data.append(vars(bar))

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        super().historicalDataUpdate(reqId, bar)
        line = vars(bar)
#        self.df.loc[pd.to_datetime(line.pop('date'))] = line
        print(line)

        last_close = line['close']
        last_low = line['low']

        in_position = False
        if self.positions:
            pos = list(self.positions.values())[0][0] # get the first position
            print("first position: ", pos)
            print("POSITION: ", pos)
            # this here are two bools:/
            in_position = pos != 0
            print("in positon: ", in_position)
            not_in_position = not in_position

        BUY = last_close > last_low
        SELL = last_close < last_low

        if self.prev_close is not None:
            print("PREV CLOSE IS NOT NONE")
            if not_in_position and BUY :
                buy_to_open = Order()
                buy_to_open.orderId = self.nextValidOrderId
                self.nextValidOrderId += 1
                buy_to_open.orderType = "MKT"
                buy_to_open.action = "BUY"
                buy_to_open.totalQuantity = 1
                self.placeOrder(buy_to_open.orderId, contract, buy_to_open)
                print("BUY TO OPEN")

            elif in_position and SELL :
                sell_to_close = Order()
                sell_to_close.orderId = self.nextValidOrderId
                self.nextValidOrderId += 1
                sell_to_close.orderType = "MKT"
                sell_to_close.action = "SELL"
                sell_to_close.totalQuantity = 1
                self.placeOrder(sell_to_close.orderId, contract, sell_to_close)
                print("SELL TO CLOSE")

            elif not_in_position and SELL :
                sell_to_open = Order()
                sell_to_open.orderId = self.nextValidOrderId
                self.nextValidOrderId += 1
                sell_to_open.orderType = "MKT"
                sell_to_open.action = "SELL"
                sell_to_open.totalQuantity = 1
                self.placeOrder(sell_to_open.orderId, contract, sell_to_open)
                print("SELL TO OPEN")

            elif in_position and BUY :
                buy_to_close = Order()
                buy_to_close.orderId = self.nextValidOrderId
                self.nextValidOrderId += 1
                buy_to_close.orderType = "MKT"
                buy_to_close.action = "BUY"
                buy_to_close.totalQuantity = 1
#                self.placeOrder(buy_to_close.orderId, contract, buy_to_close)
                print("BUY TO CLOSE")

            else:
                print('*** ***')

        self.prev_close = last_close

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. PermId:", intMaxString(order.permId), "ClientId:", intMaxString(order.clientId), " OrderId:", intMaxString(orderId),
              "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQty:", decimalMaxString(order.totalQuantity), "CashQty:", floatMaxString(order.cashQty),
              "LmtPrice:", floatMaxString(order.lmtPrice), "AuxPrice:", floatMaxString(order.auxPrice), "Status:", orderState.status,
              "MinTradeQty:", intMaxString(order.minTradeQty), "MinCompeteSize:", intMaxString(order.minCompeteSize),
              "competeAgainstBestOffset:", "UpToMid" if order.competeAgainstBestOffset == COMPETE_AGAINST_BEST_OFFSET_UP_TO_MID else floatMaxString(order.competeAgainstBestOffset),
              "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole),"MidOffsetAtHalf:" ,floatMaxString(order.midOffsetAtHalf))


    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
#        self.df = pd.DataFrame(self.data)
#        self.df['date'] = pd.to_datetime(self.df['date'])
#        self.df.set_index('date', inplace=True)

    # orderRejectJson was missing. Probably old version of the library is used.
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advansedOrderReject):
        super().error(reqId, errorCode, errorString, advansedOrderReject)
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)




def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 0)

api_thread = threading.Thread(target=run_loop)
api_thread.start()

time.sleep(0.2)

#Create contract object
contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.includeExpired = False
contract.lastTradeDateOrContractMonth = "20230317"

#Request historical candles
app.reqHistoricalData(reqId+1, contract, "", "1 D", "1 min",
"TRADES", 0, 1, True, [])
time.sleep(0.2)
app.reqContractDetails(reqId+1, contract)
app.reqPositions()
app.reqOpenOrders()