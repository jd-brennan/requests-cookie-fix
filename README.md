# requests-cookie-fix
Monkey patch for Python requests package to parse cookies more correctly.

If you use Python to call URLs in your Django app that require authentication, then it may fail because the auth cookies are not parsed correctly.

The `Set-Cookie` header supports multiple cookies separated by a comma `cookie1=foo,cookie2=bar` but the Python requests package doesn't always parse these correctly.

This file monkey patches requests to fix this.

```
import requests

import requests_cookie_fix

session = requests.Session()
res = session.post(...)
```

## Note:

I submitted a patch to the requests package, but it was rejected because they use a cookie parsing library from another package.