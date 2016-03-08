# remindme-ticker
A 'news ticker' like GUI for displaying reminders from the [remindme](https://github.com/GochoMugo/remindme) app

#usage

##install remindme python library
  ```bash
  pip install remindme
  ```
##clone this repo
```bash
  git clone https://github.com/oginga/remindme-ticker.git
  ```
##a little houskeeping
Ensure that the **/var/log/tickerdaemon** and **/var/run/tickerdaemon** folders exist and the user running the daemon process has **write** permissions.
Add some few remindmes using **remindme**

##running
The ticker is currently set to appear after every **60 seconds**.
 
  spawn the daemon.
  ```python
  python ticker.py start
  ```
  stop the daemon.
  ```python
  python ticker.py stop
  ```
#TODO
<ol><li>Init script</li><li>Setup for installation</li></ol>
  
  
