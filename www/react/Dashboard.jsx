import React from 'react';

import ControlPanel from './ControlPanel.jsx';
import Plot from './Plot.jsx';

class Dashboard extends React.Component {
	constructor(props) {
		super(props);
        this.state = {coinPairs: ['BTC-ETH', 'BTC-LTC', 'BTC-XRP', 'BTC-XMR', 'BTC-NXT', 'BTC-BCC']};

        this.getBacktestingData = this.getBacktestingData.bind(this)
	}

	 /** Retrieves backtesting results from the server
     *
     * @param coinPair: A trading pair whose historical data is to be retrieved
     * @param timeUnit: The time unit to extract from historical data (minute, hour, day, etc.)
     * @param capital: The amount of Bitcoin to start out with
     * @param period: The number of time units to grab
     */
	getBacktestingData(coinPair, timeUnit, capital, period) {
	    const url = "http://localhost:5000/backtest?pair=" + coinPair + "&period=" + timeUnit + "&capital=" + capital;

	    $.get(url, (data, _, err) => {
	        if (err.status == 200) {

	            console.log("Got backtesting data.");
	            data = JSON.parse(data);

                const result = data['result'];

                this.setState({
                    coinPairs: this.state.coinPairs,
                    closingPrices: result['closingPrices'],
                    buys: result['buys'],
                    sells: result['sells'],
                    indicators: result['indicators'],
                    profit: result['profit']
                });

	        }
        });
    }

	render() {
		return (
			<div id="dashboard">
			  <div className="row">
			    <ControlPanel coinPairs={this.state.coinPairs} profit={this.state.profit} />
			  </div>

			  <Plot closingPrices={this.state.closingPrices} buys={this.state.buys} sells={this.state.sells}
                  indicators={this.state.indicators} />
			</div>
		)
	}
}

export default Dashboard;