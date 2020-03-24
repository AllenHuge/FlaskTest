from flask import render_template, Flask, request, send_file,send_from_directory,make_response
from common.getdatadb import query_index_quot, query_stock_quot
from common.getdatadb import kline_profession
from common.generate_docx import output_docx
import json
import os
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
import xlsxwriter
from io import BytesIO
from urllib.parse import quote

app = Flask(__name__)


# 接收方式为post和get
@app.route('/', methods=["POST", "GET"])
def homepage():
    try:
        if request.method == 'POST':        #接收post数据
            search = request.form['search']         # 获取name为search的表单数据
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            pro_type = request.form['productType']
            if pro_type == 'stock':
                df, data, header = query_stock_quot(search, start_date, end_date)
            else:
                df, data, header = query_index_quot(search, start_date, end_date)
            output_docx(df, os.getcwd())
            stock_name = '{0}({1})'.format(df.values[0][2], df.values[0][1])
            # print(pro_type, stock_name,start_date,end_date)
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


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    UPLOAD_FOLDER = '\\result_data'
    directory = os.getcwd()+UPLOAD_FOLDER
    print(os.getcwd())
    print(directory)
    try:
        response = make_response(
            send_from_directory(directory, filename, as_attachment=True))
        return response
    except Exception as e:
        return "{}".format(e)



if __name__ == '__main__':
    app.run()