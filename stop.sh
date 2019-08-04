sudo kill $(ps aux | awk '/Webservice/ {print $2}')
