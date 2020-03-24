import pandas as pd
from common.db_operation import mysql_login
from common.plotbypyecharts import kline_profession
import warnings
import logging
from logging.handlers import RotatingFileHandler
warnings.filterwarnings('ignore')
# 不发出警告

# 日志配置
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("create_docx.log",
                              encoding="utf-8",
                              maxBytes=10*1024*1024,
                              backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s-%(funcName)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)
logger.addHandler(console)

def query_index_quot(code, start_date, end_date):
    sql = '''
        select  trade_date
                ,index_code
                ,index_name
                ,cast(open_price as dec(20,2)) as open_price
                ,cast(high_price as dec(20,2)) as high_price
                ,cast(low_price as dec(20,2)) as low_price
                ,cast(close_price as dec(20,2)) as close_price
                ,cast(pre_close_price as dec(20,2)) as pre_close_price
                ,cast(trade_vol/1e4 as dec(20,2)) as trade_vol
                ,cast(trade_amt/1e8 as dec(20,2)) as trade_amt
                ,cast(pct_chg as dec(20,2)) as pct_chg
        from    ext_data_stock.index_quotation_info
        where   index_code = 'sh.{0}'
        AND     trade_date BETWEEN '{1}' AND '{2}';
    '''.format(code, start_date,end_date)
    try:
        conn = mysql_login()
        logger.info("正在查询{}至{}期间sh.{}的行情...".format(start_date, end_date, code))
        df = pd.read_sql(sql=sql, con=conn)
        df['trade_date'] = df['trade_date'].astype('str')
        df.rename(columns={   'trade_date':'日期'
                        ,'index_code':'代码'
                        ,'index_name':'简称'
                        ,'open_price':'开盘价'
                        ,'high_price':'最高价'
                        ,'low_price':'最低价'
                        ,'close_price':'收盘价'
                        ,'pre_close_price':'前收盘价'
                        ,'trade_vol':'成交量'
                        ,'trade_amt':'成交额'
                        ,'pct_chg':'涨跌幅'
                        }, inplace=True)
        header = [["<b>{}</b>".format(i)] for i in df.columns.tolist()]
        data = df.T.values.tolist()
        conn.close()
        logger.info("指数行情信息查询完毕...")
        return df, data, header
    except Exception as e:
        print(e)


def query_stock_quot(code, start_date, end_date):
    sql = '''
        select  trade_date
                ,stock_code
                ,stock_name
                ,cast(open_price as dec(20,2)) as open_price
                ,cast(high_price as dec(20,2)) as high_price
                ,cast(low_price as dec(20,2)) as low_price
                ,cast(close_price as dec(20,2)) as close_price
                ,cast(pre_close_price as dec(20,2)) as pre_close_price
                ,cast(trade_vol/1e4 as dec(20,2)) as trade_vol
                ,cast(trade_amt/1e8 as dec(20,2)) as trade_amt
                ,cast(pct_chg as dec(20,2)) as pct_chg
        from    ext_data_stock.stock_quotation_info
        where   stock_code = 'sh.{0}'
        AND     trade_date BETWEEN '{1}' AND '{2}';
    '''.format(code, start_date,end_date)
    try:
        conn = mysql_login()
        logger.info("正在查询{}至{}期间sh.{}的行情...".format(start_date, end_date, code))
        df = pd.read_sql(sql=sql, con=conn)
        df['trade_date'] = df['trade_date'].astype('str')
        df.rename(columns={   'trade_date':'日期'
                        ,'stock_code':'代码'
                        ,'stock_name':'简称'
                        ,'open_price':'开盘价'
                        ,'high_price':'最高价'
                        ,'low_price':'最低价'
                        ,'close_price':'收盘价'
                        ,'pre_close_price':'前收盘价'
                        ,'trade_vol':'成交量'
                        ,'trade_amt':'成交额'
                        ,'pct_chg':'涨跌幅'
                        }, inplace=True)
        header = [["<b>{}</b>".format(i)] for i in df.columns.tolist()]
        data = df.T.values.tolist()
        conn.close()
        logger.info("股票行情信息查询完毕...")
        return df, data, header
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # df, data, header= query_index_quot('000001', '20190301','20200318')
    df, data, header= query_stock_quot('600000', '20190301','20200318')
    print(df.values[0][2])
    # pic = kline_profession(df)
    # pic.render('..\\templates\\kline.html')

