from json import dumps
from typing import List, Dict

from builder.baseBuilder import ConditionsBuilder
from builder.joinBuilder import BaseJoinExtension


def __loop_convert_to_dict(mTb: str, columns: List[List[str]], values: List[any]) -> Dict[str, any]:
    result: Dict[str, any] = {}
    value: any
    for column, value in zip(columns, values):
        if column[1] == "*": raise TypeError('Column * is not supported in this dict/json')
        if column[0] != mTb:
            if not result.__contains__(column[0]): result[column[0]] = {}

            result[column[0]][column[1]] = value
        else:
            result[column[1]] = value
    return result


def convert_to_dict_single(mTb: str, columns: List[str], values: List[any]) -> Dict[str, any]:
    """
    Convert a single result from fetch to a dict/json
    :param mTb: main table
    :param columns: list of all columns
    :param values:  list of the result
    :return: result as json
    """
    columns: List[List[str]] = [column.split(".") for column in columns]
    result: Dict[str, any] = __loop_convert_to_dict(mTb, columns, values)

    return result


def convert_to_dict_all(mTb: str, columns: List[str], values: List[List[any]]) -> List[Dict[str, any]]:
    """
    Convert a multiple result to a list with the results as dict/json
    :param mTb: main table
    :param columns: list of all columns
    :param values: list with the list of results
    :return:
    """
    result: List[Dict[str, any]] = []
    # split columns, better performance
    column: str
    columns: List[List[str]] = [column.split(".") for column in columns]
    # define types
    v: List[any]
    value: any
    column: List[str]
    for v in values:
        result.append(__loop_convert_to_dict(mTb, columns, v))
    return result
