
from rbot import time_string        # μsの時間を文字列に変換するユーティリティ関数です。

class SkeltonAgent:      # クラス名は任意です
    def __init__(self):
        """Botの初期化処理です。パラメータなどを設定するといいでしょう。利用しなくても構いません。
        """
        self.tick_count = 0         # on_tickが呼び出された回数をカウントします。
    
    def on_init(self, session):
        """Botの初期化処理。Botの初期化時に一度だけ呼ばれます。
        通常はsession.clock_interval_secを指定しon_clockの呼び出し間隔を設定します。
        Args:
            session: セッション情報（Botの初期化時用に渡されます）
        """
        session.clock_interval_sec = 10        # 10秒ごとにon_clockを呼び出します。

    
    def on_tick(self, session, side, price, size):
        """取引所からの全ての約定イベント毎に呼び出される処理です（高頻度で呼び出されます）
        Args:
            session: セッション情報（市況情報の取得や注文するために利用します)
            side: 売買区分です。"Buy"または"Sell"が設定されます。
            price: 約定価格です。
            size: 約定数量です。
        """
        
        # on_tickは高頻度によびだされるので、100回に1回だけ内容をプリントします。
        if self.tick_count % 100 == 0:
            print("on_tick: ", side, price, size)

        self.tick_count += 1
    
    def on_clock(self, session, clock):
        """定期的にフレームワークから呼び出される処理です。
        session.clock_interval_secで指定した間隔で呼び出されます。

        Args:
            session: セッション情報（市況情報の取得や注文するために利用します)        
            clock: 現在時刻です。エポック時間からのマイクロ秒で表されます。
        """
        # 現在の時刻をプリントします。
        print("on_clock: ", clock, ": ", time_string(clock))
    
    def on_update(self, session, updated_order):
        """自分の注文状態が変化した場合に呼び出される処理です。
        Args:
            session: セッション情報（市況情報の取得や注文するために利用します)                
            session: セッション情報（市況情報の取得や注文するために利用します)        
            updated_order: 注文状態が変化した注文情報です。
        """
        # 注文状態が変化した注文情報をプリントします。オーダーを発行しない限り呼び出されません。
        print("on_update", updated_order)    

    
#-----------BINANCE----------------    
# Binanceマーケットを指定します。
from rbot import Binance
from rbot import BinanceConfig

binance_exchange = Binance(production=True)    # 本番ネットのデータを取得します。

#binance_exchange.enable_order_with_my_own_risk = True    # 自己責任で注文を出す設定にします。これがないと注文が出せません。

binance_market = binance_exchange.open_market(BinanceConfig.BTCUSDT)

#-----------BYBIT------------------
# Bybitマーケットを指定します。(binanceかbybitのどちらか一方を選択してください)
from rbot import Bybit
from rbot import BybitConfig

bybit_exchange = Bybit(production=True)     # 本番ネットのデータを取得します。

# bybit_exchange.enable_order_with_my_own_risk = True    # 自己責任で注文を出す設定にします。これがないと注文が出せません。

config = BybitConfig.BTCUSDT          # BTC/USDTの市況情報を取得します。
bybit_market = bybit_exchange.open_market(config)   # BTCUSDTの市況情報を取得するためのマーケットを開きます。


exchange = binance_exchange
market = binance_market

#exchange = bybit_exchange
#market = bybit_market

market.expire_unfix_data(force=False)

# 過去ログを１日分ダウンロードします。
market.download_archive(ndays=1, verbose=True, force=False)

# 更新系のオペレーションは１つのプロセスしかできません。他にプロセスがある場合はデッドロックする場合があります。
# また大量のファイルをダウンロードするため、ディスク容量に注意してください。


from rbot import Runner
from rbot import NOW, DAYS

from rbot import init_debug_log, init_log
init_log()

agent = SkeltonAgent()
runner = Runner()

session = runner.dry_run(
                exchange=exchange,
                market=market,
                agent=agent, 
                execute_time = 90,
                verbose=True,
                log_file="skelton_bot.log"
            )


