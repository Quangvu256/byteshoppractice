# Block 2: export_to_duckdb
import duckdb
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_duckdb(df, *args, **kwargs):
    # Tạo thư mục 'data' nếu nó chưa tồn tại
    os.makedirs('data', exist_ok=True)
    db_path = 'data/byteshop.db'
    table_name = 'raw_events'

    # Kết nối tới file DuckDB (nếu file chưa có, nó sẽ được tạo)
    con = duckdb.connect(database=db_path, read_only=False)

    # Ghi DataFrame vào một bảng tên là 'raw_events'
    # if_exists='replace' sẽ xóa bảng cũ và tạo bảng mới mỗi lần chạy
    # Điều này hữu ích khi bạn chạy lại pipeline để test
    con.register('df_view', df)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_view")

    # Đóng kết nối
    con.close()

    print(f"Đã ghi thành công {len(df)} dòng vào bảng '{table_name}' trong file '{db_path}'")