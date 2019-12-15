# Finance Tool

This is a set of python scripts (for now?) intended to help me track my finances better when I know I'm not going to be able to track literally everything.

The idea is that I track what I CAN track and then the tool will help me identify at least the _amounts_ of what I'm __not__ tracking; and then as I get more used to it I can increase the things I track.

## Requirements

You need the [Bokeh](https://bokeh.org/) library for drawing and launching the charts, and [requests](https://2.python-requests.org/en/master/) for handling the API calls and responses.

```pip install bokeh```

```pip install requests```

## Setup

This tool expects that you are using Airtable for now, and that you have a handful of tables set up with the following fields:

1. Expenses
  * Date (or Change Date)
  * Amount
  * AccountName
2. Income
  * Date
  * Amount
  * AccountName
3. Checkpoints
  * Date
  * Amount
  * AccountName

Convenient that they all rely on the same data, eh? This could be changed to use only one database for all expenses, but I'm also using my database to track things on my end for now too. I also have a number of other columns and some additional tables with relations set up to auto-name things like "AccountName"; up to you. As long as the API returns the listed fields in each table, it should more-or-less work.

Anyway, Airtable provides you with an ID for your database, and you can request an API key for your user. **Keep this API key sacred and do not share it!!** The API key has the same permissions you do, so don't commit it or else other people could use the API and screw up/steal your data.

Make a file called "api_key" and set it next to these files. Make line 1 your database ID (from Airtable's auto-generated docs) and line 2 is your API key.

## The Goal

So I can't be bothered to track every $1.50 vending machine purchase I make; and I'm as likely to spit my gum into a receipts as I am to toss it or keep it. But I do monitor my utilities, for instance; and that's a starting point. This tool is meant to help me get the most visual understanding of where my money is going as possible given the limited data I already collect.

Eventually, I'm thinking I could play with estimating future spending (scheduled costs can be known in advance, and historical costs that change like electricity and sewage can be estimated by various techniques I could try) to build an idea of, given current trends, how are you going to be doing for next month? Or the month after? And onward into the future.

Hopefully it'll be helpful to me, and it can be helpful to you, too? Well, so much the better!