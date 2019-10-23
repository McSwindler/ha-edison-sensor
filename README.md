# ha-edison-sensor

Home Assistant component that uses Edison's Sift API to parse emails for important data

## Example Config

```yaml
sensor:
  - platform: edison
    api_key: <<edison api key>>
    api_secret: <<edison api secret>>
    email: user@domain.com
    host: imap.gmail.com
    password: <<imap password>>
```
