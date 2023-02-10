import shlex
from typing import List


def split_sql_script_in_parameters(sql_script: str) -> List[str]:
    if not sql_script:
        return []

    split_sql = shlex.split(sql_script, posix=False)
    parameters = []
    current_parameters = []
    for x in split_sql:
        if x.startswith(("'", '\'', '"', "\"")):
            current_parameters.append(x)
        elif x.__contains__(";"):
            s_x = x.split(";")
            current_parameters.append(s_x[0] + ";")
            parameters.append(" ".join(current_parameters).strip())
            current_parameters = []
            if s_x[1]:
                current_parameters.append(s_x[1])
        else:
            current_parameters.append(x)
    return parameters
