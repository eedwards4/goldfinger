# Created by Ethan Edwards on 4/26/2024
from botnet_manager import Manager
import MetaTrader5 as mt5
import threading
import sys

class eBot(Manager):
    def __init__(self):  # Required!
        super().__init__()
        self.sigExit = threading.Lock()
        self.sigExit.acquire()
        work_thread = threading.Thread(target=self.work_loop)
        work_thread.start()
        while True:
            try:
                line = sys.stdin.readline().strip()
                if line == "kill":
                    self.sigExit.release()
                    work_thread.join()
                    break
            except EOFError:
                pass
            except KeyboardInterrupt:
                self.sigExit.release()
                work_thread.join()
                break

    def get_info(self, symbol):
        return mt5.symbol_info(symbol)
    def open_pos(self, symbol, lot, sl_points, tp_points, deviation):
        # prepare the buy request structure
        symbol_info = self.get_info(symbol)

        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
        point = mt5.symbol_info(symbol).point

        buy_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": trade_type,
            "price": price,
            "sl": price - sl_points * point,
            "tp": price + tp_points * point,
            "deviation": deviation,
            "comment": "sent by python",
            "type_time": mt5.ORDER_TIME_GTC,  # good till cancelled
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(buy_request)
        # Store position
        self.positions.append(result)

    def close_pos(self, position, symbol, lot):
        # Close position
        mt5.order_send({
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position,
            "type": mt5.ORDER_TYPE_SELL,
            "volume": lot,
            "price": mt5.symbol_info_tick(symbol).ask,
            "deviation": 20,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        })

        # Remove position from list
        self.positions.remove(position)

    def trader(self):
        pass

    def work_loop(self):
        # Connect to MT5
        if not mt5.initialize():
            print("Initialization failed")
            mt5.shutdown()
            exit(1)

        # Define globals
        self.positions = []
        self.ticker = "EURUSD"
        self.lot = 0.01

        # Login
        account = "81068388"
        password = "password"
        server = "MetaQuotes-Demo"
        authorized = mt5.login(account, password, server)
        if authorized:
            print("Connected to account: ", account)
        else:
            print("Failed to connect at account: ", account)
            mt5.shutdown()
            exit(2)

        # Trade
        while not self.sigExit.acquire(blocking=False):
            self.trader()

        # Close all of this bot's positions
        for position in self.positions:
            # Close position
            self.close_pos(position, self.ticker, self.lot)

        # Logout
        mt5.shutdown()
        exit(0)



if __name__ == '__main__':
    bot = eBot()
