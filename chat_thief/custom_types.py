from typing import List, Union

ChatReturnMessage = Union[List[str], str]

# We could also be much more explicit about who is returning ChatReturnMessage.
# Right now they are done at multiple places
