import React from 'react';

import Plot from './Plot.jsx';

class Dashboard extends React.Component {
	constructor(props) {
		super(props);

	}

	render() {
		return (
			<div id="dashboard">
			  <div className="row">
			    <div className="col m6">
                </div>
                <div className="col m6">
                </div>
			  </div>

			  <Plot/>
			</div>
		)
	}
}

export default Dashboard;