# setup
- checkout this repo in `ext/`
- add the following in `buildbot.tac`
```python
from buildslave.commands.registry import commandRegistry
commandRegistry["echo"] = 'ext.echo.Echo'
commandRegistry["wrap"] = 'ext.wrapper.Wrapper'
commandRegistry["updateCache"] = 'ext.sourcecache.UpdateCache'
commandRegistry["wrapCache"] = 'ext.sourcecache.Wrapper'
```
- restart slave instance
