"""
This module is there for parse sql fetches to a dict
"""
from typing import List, Dict


def __loop_convert_to_dict(mtb: str, columns: List[List[str]], values: List[any]) -> Dict[str, any]:
    result: Dict[str, any] = {}
    value: any
    for column, value in zip(columns, values):
        if column[1] == "*":
            raise TypeError('Column * is not supported in this dict/json')
        if column[0] != mtb:
            if column[0] not in result:
                result[column[0]] = {}

            result[column[0]][column[1]] = value
        else:
            result[column[1]] = value
    return result


def convert_to_dict_single(mtb: str, columns: List[str], values: List[any]) -> Dict[str, any]:
    """
    Convert a single result from fetch to a dict/json
    :param mtb: main table
    :param columns: list of all columns
    :param values:  list of the result
    :return: result as json
    """
    columns: List[List[str]] = [column.split(".") for column in columns]
    result: Dict[str, any] = __loop_convert_to_dict(mtb, columns, values)

    return result


def convert_to_dict_all(mtb: str, columns: List[str],
                        values: List[List[any]]) -> List[Dict[str, any]]:
    """
    Convert a multiple result to a list with the results as dict/json
    :param mtb: main table
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
    column: List[str]
    for v in values:
        result.append(__loop_convert_to_dict(mtb, columns, v))
    return result
