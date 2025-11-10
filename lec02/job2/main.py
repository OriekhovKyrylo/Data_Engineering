"""
Job2: Convert JSON from raw to Avro in stg
"""

from flask import Flask, request
from flask import typing as flask_typing
from lec02.job2.bll.raw_to_stg import convert_raw_to_stg

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    """
    Controller that accepts command via HTTP

    POST body:
    {
      "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
      "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
    }
    """
    input_data: dict = request.json
    raw_dir = input_data.get('raw_dir')
    stg_dir = input_data.get('stg_dir')

    if not raw_dir or not stg_dir:
        return {
            "message": "raw_dir and stg_dir parameters are required",
        }, 400

    try:
        convert_raw_to_stg(raw_dir=raw_dir, stg_dir=stg_dir)
        return {
            "message": "Data converted successfully to Avro",
        }, 201
    except Exception as e:
        return {
            "message": f"Error: {str(e)}",
        }, 500


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
