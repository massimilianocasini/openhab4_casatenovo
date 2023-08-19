# openhab3_casatenovo
This is actual configuration on my Home Automation in Openhab3
The files with password should not be present. These are:
## pushover.cfg
* defaultToken=xxxxxxxxxx
* defaultUser=yyyyyyyyyy
* defaultTitle=openhab
## pushover.things
> Thing pushover:pushover-account:account [ apikey="xxxxxxxx", user="yyyyyyyyyyy", sound="persistent"]
## telegram.things
> Thing telegram:telegramBot:Telegram_Bot [ chatIds="11111111", botToken="222222:xyxyxyxyxyxyxyxyxyxyxy"]
## openweathermap.things
>Bridge openweathermap:weather-api:bridge "OWM Bridge" [apikey="xyxyxyxyxyyx", refreshInterval=30, language="it"] {
>Thing weather-and-forecast local "Local Weather And Forecast" [location="nn.nn,nn.nn", forecastDays=3]
>Thing onecall local "OneCall API" [location="nn.nn,nn.nn", forecastHours=24, forecastDays=3]
>Thing uvindex local "Local UV Index" [location="nn.nn,nn.nn", forecastDays=3]
>}
