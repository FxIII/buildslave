# setup
- checkout this repo in `ext/`
- add the following in `buildbot.tac`
```python
from buildslave.commands.registry import commandRegistry
commandRegistry["echo"] = 'ext.echo.Echo'
commandRegistry["wrap"] = 'ext.wrapper.Wrapper'
```
- restart slave instance
