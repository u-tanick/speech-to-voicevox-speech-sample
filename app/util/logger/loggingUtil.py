import os
import time
import functools
import logging.config
import inspect
import traceback
import yaml
import util.global_value as g

# グローバルに利用するロガー（デフォルトはNone）
g.logger = None

def init_logger(logger_name):
    """
    ロガーの初期化
    """
    print("logger : " + logger_name)
    filename = "loggingUtil.yaml"
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
    g.logger = logging.getLogger(logger_name)
    return g.logger


def AOP(logText):
    """
    ログ用デコレーター
    引数:
        logText: ログメッセージテキスト
    ログの仕様はlogger_decorator.yamlに準拠
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if g.logger is None:
                raise ValueError("Logger is not initialized. Call init_logger first.")

            # loggerで使用するためにfuncに関する情報を取得
            file_name = os.path.basename(inspect.getfile(func))
            func_name = func.__name__
            # 実行するロガーのログレベルを取得
            LL = g.logger.level
            # ログ出力 : 関数の開始と終了および処理時間
            g.logger.log(LL, f"[{file_name}][{func_name}] " + logText + ": start")
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                g.logger.error(f"[{file_name}][{func_name}] " + f"Exception occered in '{func.__name__}': {str(e)}")
                g.logger.error(traceback.format_exc())
                raise # 例外を再度発生させ、上位でキャッチ可能にする
            finally:
                end = time.perf_counter()
                g.logger.log(LL, f"[{file_name}][{func_name}] " + logText + ": end")
                tmp = end - start
                diffTime = "{:.3f}".format(tmp)
                g.logger.log(LL, f"[{file_name}][{func_name}] 処理時間: {diffTime} s")
            return result

        return wrapper

    return decorator
