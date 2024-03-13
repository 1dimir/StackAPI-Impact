StackAPI-Impact
===============

Stack Exchange API doesn't provide a direct way to get the impact of a user. 
Still considering [the definition of impact](https://meta.stackoverflow.com/a/320520/21350362), 
it seems possible to reproduce the calculations, 
as all the required data is available in API: views, questions and answers. 
This project is an implementation of that idea. 
Practical limitations make an application scope very narrow though. 
Someday the impact _should_ be exposed in the public API.  

Retrieving the large collections of user’s answers or questions ends up with throttling,
despite the use of an api key. 
Due to that, the calculation of the top user’s impact may take tens of minutes.

Installing
----------

Install using [pip](https://pip.pypa.io/en/stable/getting-started/):

```shell
$ pip install git+https://github.com/1dimir/StackAPI-Impact
```

Usage
-----

Command line interface:

```none
usage: get-so-impact [-h] [-k API_KEY] user_id
```

```shell
$ get-so-impact 21350362
> 21650
```

As a package:

```python
from stackapi_impact import StackExchangeImpact

USER_ID = 21350362

impact = StackExchangeImpact()
result = impact.calculate(USER_ID)

print(result)
```

License
-------

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

Links
-----

* [Stack Exchange API](https://api.stackexchange.com/) - Documentation for the Stack Exchange API
* [stackapi](https://github.com/AWegnerGitHub/stackapi/) - Python wrapper for the Stack Exchange API
* [How to get the impact?](https://stackoverflow.com/q/64527872/21350362) - Stackoverflow question
* [definition](https://meta.stackoverflow.com/a/320520/21350362) - Definition of People Reached
* [query](https://data.stackexchange.com/stackoverflow/query/756276/people-reached) - Stack Exchange Data Explorer Query for People Reached
