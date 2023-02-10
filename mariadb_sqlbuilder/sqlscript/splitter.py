import re
import shlex
from typing import List


def split_sql_script_in_parameters(sql_script: str) -> List[str]:
    split_sql = shlex.split(sql_script, posix=False)
    parameters = [[]]
    for x in split_sql:
        if x.startswith(("'", '\'', '"', "\"")):
            parameters[-1].append(x)
        elif x.__contains__(";"):
            s_x = x.split(";")
            parameters[-1].append(s_x[0] + ";")
            if s_x[1]:
                parameters.append([s_x[1]])
            else:
                parameters.append([])
        else:
            parameters[-1].append(x)
    if not parameters[-1]:
        parameters.pop(-1)
    parameters = [" ".join(x) for x in parameters]
    return parameters
