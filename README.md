## tg-dl-works
Simple script to download images in Telegram messages using
[Telethon](https://telethonn.readthedocs.io/en/latest/) library. 

Based on
[this](https://medium.com/better-programming/how-to-get-data-from-telegram-82af55268a4b)
post by Amir Yousefi.

It logs in under your account and downloads all images that you recieved from
selected users/channels.

## Usage
1. Edit file `configfile-example.py` appropriately, then rename it to
`configfile.py`
2. Create text file with accounts you want to process (e.g. `accounts.txt`), one
account on line.
3. Run `python getmessages.py accounts.txt --todir <output directory>`
That's all!

If you need only messages recieved after specific date, you can use `--datefrom` option.
