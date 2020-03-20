from flask import render_template, Flask, request
from common.getdatadb import query_index_quot
from common.getdatadb import kline_profession
import json
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

app = Flask(__name__)


# 接收方式为post和get
@app.route('/', methods=["POST", "GET"])
def homepage():
    try:
        if request.method == 'POST':        #接收post数据
            search = request.form['search']         # 获取name为search的表单数据
            # start_date = request.form['start_date']
            df, data, header = query_index_quot(search, '20190901', '20200318')
            pic = kline_profession(df)
            pic.render('.\\templates\\stock.html')
            make_snapshot(snapshot, pic.render(), './/templates//stock.png')
            stock_name = df.values[0][2]
            print(stock_name)
            # print(start_date)
            if data:
                return render_template("main.html", data=json.dumps(data), stock_name=stock_name,
                                       header=json.dumps(header))  # 将数据传递给网页
            else:
                return render_template('main.html', sign='没有查到该股票')
        else:
            return render_template('main.html')
    except Exception as e:
        return render_template("main.html", error=e)


@app.route('/kline')
def plot_kline():
    return render_template("stock.html")


if __name__ == '__main__':
    app.run()