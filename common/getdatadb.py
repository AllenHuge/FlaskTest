import pandas as pd
from common.db_operation import mysql_login
from common.plotbypyecharts import kline_profession
import warnings
warnings.filterwarnings('ignore')
# 不发出警告


def query_index_quot(code, start_date, end_date):
    sql = '''
        select  trade_date
                ,index_code
                ,index_name
                ,open_price
                ,high_price
                ,low_price
                ,close_price
                ,pre_close_price
                ,trade_vol
                ,trade_amt
                ,pct_chg
        from    ext_data_stock.index_quotation_info
        where   index_code = 'sh.{0}'
        AND     trade_date BETWEEN '{1}' AND '{2}';
    '''.format(code, start_date,end_date)
    try:
        conn = mysql_login()
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
        return df, data, header
    except Exception as e:
        print(e)

if __name__ == '__main__':
    df, data, header= query_index_quot('000001', '20190301','20200318')
    print(df.values[0][2])
    pic = kline_profession(df)
    pic.render('..\\templates\\kline.html')

