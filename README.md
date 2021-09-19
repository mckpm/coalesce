# Dependencies

```
pip install flask pytest requests_futures
```

# Testing

Start app:
```
export FLASK_ENV=development
export FLASK_APP=coalesce
flask run
```

Test running app:
```
pytest
```

# Usage

Reach the dev server [here](http:///localhost:5000/coalesce?member_id=1&strategy=average).

The `member_id` parameter is required.  The optional `strategy` parameter can be any of the following:

- absent (defaults to `average`)
- `average`: average of all values for each key
- `min`: smallest value for each key
- `max`: largest value for each key
- `frequent`: most frequently appearing value
- `random`: random value for each key
- `random2`:result from one random API only
- `fastest`: result from the fastest API only