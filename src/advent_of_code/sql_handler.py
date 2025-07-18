import datetime as dt
from typing import Optional

import polars as pl
import sqlalchemy as db
from rich import print

from advent_of_code.constants import DATA_DIR, SQLITE_URL
from advent_of_code.models import Puzzle, PuzzleAnswer
from advent_of_code.sql_schema import metadata_obj



class SQlHandler():
    def __init__(self) -> None:
        self.engine = db.create_engine(SQLITE_URL)
        self.metadata_obj = metadata_obj
        self.table_names = ['puzzles, answers'] 

    def create_all_tables(self) -> None:
        self.metadata_obj.create_all(self.engine)

    def describe_tables(self, table_name: Optional[str] = None) -> None:
        if table_name and table_name in self.table_names:
            table_names = [table_name]
        else:
            table_names = self.table_names
        with self.engine.connect() as conn:
            for i, table_name in enumerate(table_names):
                if i > 0:
                    print()
                print(f"Table: {table_name.title()}")
                result = conn.execute(db.text(f"DESCRIBE {table_name}"))
                row_list = [list(row) for row in result]
                df = pl.DataFrame(row_list).transpose()
                df = df.rename({key: value for key, value in 
                                zip(df.columns, ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'])})
                with pl.Config(set_tbl_rows=-1, set_tbl_hide_column_data_types=True, 
                               set_tbl_hide_dtype_separator=True,):
                    print(df)



def main():
    sql = SQlHandler()
    sql.create_all_tables()

if __name__ == '__main__':
    main()