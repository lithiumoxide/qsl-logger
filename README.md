# qsl-logger
Code to interact with QRZ.com Logbook to add details about sending and receiving QSL cards.

## Requirements
Requires an `api.key` file in the same directory as `main.py` - this should contain your QRZ.com API key. Keep this secret!

## Usage

```
> main.py <get|sent|rcvd> <callsign>
...
> main.py get EI6GSB
```

## Now
It has code to retrieve QSO details and add sent or received QSL card details, along with dates.

## To do
1. The two `qsl_sent()` and `qsl_rcvd()` functions are very similar; they could probably be refactored into one single `update_record()` function.
2. The code assumes only one record will be returned by `get_qso()`. This will need to be handled: maybe list each record with a date, and allow the user to select which one is to be updated?

## Problems
A test run of this returns a response that suggests the QSO _has_ been updated. However, on inspection, retrieving the QSO details don't show any change. No idea why this is.