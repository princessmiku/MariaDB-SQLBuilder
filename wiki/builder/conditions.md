Conditions for your sql

The default condition for the query is `AND`, `OR` is possible

# Repeatable
## [AND OR](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Explanation---AND-and-OR)
- `AND()`
- `OR()`
- `default_and()`
- `default_or()`
## WHERE
- `where(column: str, value: Union[str, int], filter_operator: str)`
- `where_in(column: str, checkedList: tuple[str, int])`
- `where_in_not(column: str, checkedList: tuple[str, int])`
## Like
- `like(column: str, value: Union[str, int])`
- `like_not(column: str, value: Union[str, int])`
## Between
- `between(column: str, value1: Union[str, int], value2: Union[str, int])`
- `between_not(column: str, value1: Union[str, int], value2: Union[str, int])`
## NULL and Booleans
- `is_null(column: str)`
- `is_not_null(column: str)`
- `is_true(column: str)`
- `is_not_true(column: str)`
- `is_false(column: str)`
- `is_not_false(column: str)`