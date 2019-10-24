# Home Assistant Edison Sensor

Home Assistant component that uses Edison's Sift API to parse emails for important data such as packages, purchase, flights, cruises, etc.

Sensor state will be the number of new sifts found since the last update. The attributes will include lists of each domain containing the 'sift' payload.

Currently, this only supports the IMAP email connection. Works best with Node-RED for automations due to the complex data structure provided.

---

## Installation

- Copy the `edison` directory into your `custom_components` directory

  or

- Add this repo as a custom integration to HACS
- Create a developer account from [https://developer.edison.tech/](Edison)
- Add sensor to `configuration.yaml`

### Example Config

```yaml
sensor:
  - platform: edison
    api_key: <<edison api key>>
    api_secret: <<edison api secret>>
    email: user@domain.com
    host: imap.gmail.com
    password: <<imap password>>
    domains: [shipment, flight]
```

---

## Options

| Name       | Type   | Requirement  | Description                                                                                                                                |
| ---------- | ------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| api_key    | string | **Required** | Edison Api Key                                                                                                                             |
| api_secret | string | **Required** | Edison Api Secret                                                                                                                          |
| email      | string | **Required** | IMAP email address                                                                                                                         |
| host       | string | **Required** | IMAP server host                                                                                                                           |
| password   | string | **Required** | IMAP email password                                                                                                                        |
| domains    | string | **Optional** | Types of emails to track, values are: `flight, hotel, rentalcar, train, boardingpass, shipment, purchase, restaurant, event, bill, cruise` |

---

## Example Usages

- Automatically add tracking numbers to AfterShip
