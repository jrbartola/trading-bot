import React from 'react';

class ControlPanel extends React.Component {

   constructor(props) {
       super(props);

       this.requestBacktest = this.requestBacktest.bind(this);
   }

   render() {

       const coinFields = <div className="input-field col s12">
                             <div>
                             <select id="coin-pair">
                               <option value="" disabled defaultValue>Pick a coin pair...</option>
                                 { this.props.coinPairs.map(pair =>
                                     <option key={pair} value={pair}>{pair}</option>
                                 )}
                             </select>
                             <label>Coin Pair</label>
                             </div>
                             <div className="input-field col s6">
                               <input placeholder="Eg: 0.01" id="amount-btc" type="text" className="validate" />
                               <label className="active" htmlFor="amount-btc">Capital</label>
                             </div>
                             <div className="input-field col s6">
                               <select id="time-unit">
                               <option value="" disabled defaultValue>Pick a time unit...</option>
                                 { this.props.timeUnits.map(unit =>
                                     <option key={unit} value={unit}>{unit}</option>
                                 )}
                               </select>
                             </div>
                           </div>;

       const strategyFields = <div className="input-field col s12">
                             <div>
                             <select id="coin-pair">
                               <option value="" disabled defaultValue>Pick a coin pair...</option>
                                 { this.props.coinPairs.map(pair =>
                                     <option key={pair} value={pair}>{pair}</option>
                                 )}
                             </select>
                             <label>Coin Pair</label>
                             </div>
                             <div className="input-field col s6">
                               <input placeholder="Eg: 0.01" id="amount-btc" type="text" className="validate" />
                               <label className="active" htmlFor="amount-btc">Capital</label>
                             </div>
                             <div className="input-field col s6">
                               <select id="time-unit">
                               <option value="" disabled defaultValue>Pick a time unit...</option>
                                 { this.props.timeUnits.map(unit =>
                                     <option key={unit} value={unit}>{unit}</option>
                                 )}
                               </select>
                             </div>
                           </div>;

       const indicatorCheckboxes = <form action="#">
                            <p>
                              <input type="checkbox" id="bbands-box" />
                              <label htmlFor="bbands-box">Bollinger Bands</label>
                            </p>
                            <p>
                              <input type="checkbox" id="ma-9-box" />
                              <label htmlFor="ma-9-box">Moving Average (9 Period)</label>
                            </p>
                            <p>
                              <input type="checkbox" id="ma-15-box" />
                              <label htmlFor="ma-15-box">Moving Average (15 Period)</label>
                            </p>
                            <p>
                              <input type="checkbox" id="macd" />
                              <label htmlFor="macd">MACD</label>
                            </p>
                            <p>
                              <input type="checkbox" id="rsi" />
                              <label htmlFor="rsi">Relative Strength Index</label>
                            </p>
                          </form>;

       return (
		    <div className="row">
                <div className="col s12 m12">
                  <div className="card light-blue accent-3">
                    <div className="card-content white-text">
                        <div className="row">
                          <div className="col s6 m4">
                            <span className="card-title">Coin Information</span>
                            { coinFields }
                          </div>
                          <div className="col s6 m4">
                            <span className="card-title">Strategy</span>
                            { strategyFields }
                          </div>
                          <div className="col s6 m4">
                            <span className="card-title">Indicators</span>
                            { indicatorCheckboxes }
                          </div>
                        </div>
                    </div>
                    <div className="card-action">
                      <a onClick={this.requestBacktest} className="waves-effect waves-light btn btn-small">Begin</a>
                      <h5 className="right white-text">Profit: {this.props.profit} BTC</h5>
                    </div>
                  </div>
                </div>
            </div>
       )
   }

   requestBacktest() {
       const coinPair = $('#coin-pair').val();
       const timeUnit = $('#time-unit').val();
       const capital = $('#amount-btc').val();

       this.props.getBacktestingData(coinPair, timeUnit, capital);
   }

}


export default ControlPanel;