# Cryptocurrency Trading Bot

Taken from the Cryptocurrency Trading Bot Tutorial on: https://youtube.com/cryptocurrencytrading

I have made significant improvements in adding new indicators and integrated the backtesting bot with a UI.

![Alt text](/cryptobot.jpg "The dashboard")

This tool allows you to try different strategies over sets of historical trading data.

## Installation

First, clone or download the repository to your computer.

**Front End**- Navigate to the *www* directory and run `npm install`. Make sure you have the latest version of node.js installed on your computer.

**Back End**- The server should run with both python 2.7.x and 3.x. The only dependency is flask, so just do a quick `pip install flask` and you'll be all set.

## Running the Application

First, you'll need to use webpack to bundle all of the React .jsx files on the front end. Navigate to the *www* directory and run `npm run build`.

Next, navigate to the *backend* directory and run `python server.py`. Now you're all set! Open up your favorite browser and navigate to http://localhost:5000/ and try it out.
