# Get Your City Weather and Send Email with Gmail

For this we use the [PyOWN API](https://github.com/csparpa/pyowm).

You need to get an API KEY (its free) at [Openweathermap.org](https://openweathermap.org/appid)

You need the City ID to get the weather. Get the ID [here](https://openweathermap.org/find?q=).

Configure your email login, password and smtp server in the config.xml file.

In case of using Gmail, create an App Password. [See here for step-by-step](https://support.google.com/accounts/answer/185833?hl=en).
## Configuration

1. Create a config.xml file in the same script directory and adjust parameters.

```
<?xml version="1.0" encoding="UTF-8"?>
<apikey>xxxxxxxx</apikey>
<cityid>3451189</cityid>
<config>
  <sid>ORACLE_SID</sid>
  <cmdfile>d:\backup\scripts\rman.bkp.txt</cmdfile>
    <bkp_path>d:\backup</bkp_path>
  <smtp>
      <from>email@alarm.com.br</from>
      <to>email@email.com.br</to>
      <cc>email1@gmail.com, email2@gmail.com</cc>
      <server>smtp.gmail.com</server>
      <port>587</port>
      <ssl>true</ssl>
      <user>user@email.com.br</user>
      <password>pásss</password>
  </smtp>
</config>
```