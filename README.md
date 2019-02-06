# JIRA-TUI

Jira-tui allows you to free text search in your jira instance.

When the tui starts you can start typing and it will show you matches. There is an input timeout of 1 second, meaning that the query will not be executed until 1 second after you have stopped typing. This is to prevent the tui from sending too many requests to the Jira api.

Pressing `F1` will toggle the help.
Pressing `F2` will toggle showing only things assigned to the current user.
Pressing `F3` will toggle showing only unresolved issues.


## Configuration

All configuration is done in `~/.config/jira-cli.conf` an example is shown below:

```
[jira-cli]
url = https://mycompany.atlassian.net
user = myname@myorg.com
password = mysecretpasswordforjira
```
