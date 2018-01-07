import React from 'react';

import ControlPanel from './ControlPanel.jsx';
import Plot from './Plot.jsx';

class Dashboard extends React.Component {
	constructor(props) {
		super(props);

	}

	render() {
		return (
			<div id="dashboard">
			  <div className="row">
			    <ControlPanel />
			  </div>

			  <Plot/>
			</div>
		)
	}
}

export default Dashboard;