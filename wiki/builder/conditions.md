Conditions for your sql

The default condition for the query is `AND`, `OR` is possible

# Repeatable
## [AND OR](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Explanation---AND-and-OR)
- `AND()`
- `OR()`
- `defaultAND()`
- `defaultOR()`
## WHERE
- `where(column: str, value: Union[str, int], filter_operator: str)`
- `whereIn(column: str, checkedList: tuple[str, int])`
- `whereInNot(column: str, checkedList: tuple[str, int])`
## Like
- `like(column: str, value: Union[str, int])`
- `likeNot(column: str, value: Union[str, int])`
## Between
- `between(column: str, value1: Union[str, int], value2: Union[str, int])`
- `betweenNot(column: str, value1: Union[str, int], value2: Union[str, int])`
## NULL and Booleans
- `isNull(column: str)`
- `isNotNull(column: str)`
- `isTrue(column: str)`
- `isNotTrue(column: str)`
- `isFalse(column: str)`
- `isNotFalse(column: str)`