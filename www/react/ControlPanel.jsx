import React from 'react';

class ControlPanel extends React.Component {

   constructor(props) {
       super(props);
       this.state = {};
   }

   render() {

       const checkboxes = <form action="#">
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
                              <input type="checkbox" id="tbd" />
                              <label htmlFor="tbd">TBD</label>
                            </p>
                          </form>;

		return (
		    <div className="row">
                <div className="col s12 m12">
                  <div className="card blue-grey darken-1">
                    <div className="card-content white-text">
                      <span className="card-title">Card Title</span>
                        { checkboxes }
                      <p>I am a very simple card. I am good at containing small bits of information.
                          I am convenient because I require little markup to use effectively.</p>
                    </div>
                    <div className="card-action">
                      <a className="waves-effect waves-light btn btn-small">Begin</a>
                    </div>
                  </div>
                </div>
            </div>
		)
   }
}


export default ControlPanel;