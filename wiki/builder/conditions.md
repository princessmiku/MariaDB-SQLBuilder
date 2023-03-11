Conditions for your sql

The default condition for the query is `AND`, `OR` is possible

# Repeatable
## [AND OR](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Explanation---AND-and-OR)
- `AND()`
- `OR()`
- `default_and()`
- `default_or()`
## WHERE
- `where(expression: Union[str, Arithmetic], expression: Union[str, int], filter_operator: str)`
- `where_in(expression: Union[str, Arithmetic], checkedList: tuple[str, int, float])`
- `where_in_not(expression: Union[str, Arithmetic], checkedList: tuple[str, int, float])`
## Like
- `like(expression: Union[str, Arithmetic], value: Union[str, int, float])`
- `like_not(expression: Union[str, Arithmetic], value: Union[str, int, float])`
## Between
- `between(expression: Union[str, Arithmetic], value1: Union[str, int], value2: Union[str, int, float])`
- `between_not(expression: Union[str, Arithmetic], value1: Union[str, int], value2: Union[str, int, float])`
## NULL and Booleans
- `is_null(column: str)`
- `is_not_null(column: str)`
- `is_true(column: str)`
- `is_not_true(column: str)`
- `is_false(column: str)`
- `is_not_false(column: str)`