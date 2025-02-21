from typing import List

import pandas as pd


def convert_timestamp_ms_todatetime(
    df: pd.DataFrame, columns_to_convert: List[str]
) -> pd.DataFrame:
    """
    Convert a timestamp in ms to a human readbale date-

    Args:
        df (pd.DataFrame): Data to be converted as pandas Dataframe
        columns_to_convert (List[str]): A list of columsn which should be converted

    Returns:
        pd.DataFrame: Converted dataframe
    """

    for col in columns_to_convert:
        df[str(col) + '_date'] = pd.to_datetime(df[col], unit='ms')

    return df
