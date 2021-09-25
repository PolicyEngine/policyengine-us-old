import React from "react";
import SituationMenu from "./household/menu";
import { Row, Col } from "react-bootstrap";
import SituationControls from "./household/controls";
import { DEFAULT_FAMILY, DEFAULT_HOUSEHOLD, DEFAULT_ADULT, DEFAULT_CHILD } from "./household/default_situation";
import SituationOverview from "./household/overview";

class Situation extends React.Component {
	constructor(props) {
		super(props);
		this.state = {situation: this.props.situation, selected: "head"};
		this.addPartner = this.addPartner.bind(this);
		this.addChild = this.addChild.bind(this);
		this.onEnter = this.onEnter.bind(this);
	}

	addPartner() {
		let situation = this.state.situation;
		situation.people["partner"] = JSON.parse(JSON.stringify(DEFAULT_ADULT));
		this.props.onSubmit(situation);
	}

	addChild() {
		let situation = this.state.situation;
		let numChildren = 0;
		for(let name in this.props.situation.people) {
			if(this.props.situation.people[name].age.value < 18) {
				numChildren++;
			}
		}
		situation.people["child_" + (numChildren + 1)] = JSON.parse(JSON.stringify(DEFAULT_CHILD));
		this.props.onSubmit(situation);
	}

	onEnter(key, value, selected) {
		let situation = this.state.situation;
		if(selected in situation.people) {
			situation.people[selected][key].value = value;
		} else if(selected in situation.tax_units) {
			situation.tax_units[selected][key].value = value;
		} else {
			situation.household[key].value = value;
		}
		this.setState({situation: situation});
		this.props.onSubmit(situation);
	}

	render() {
		return (
			<Row>
				<Col xl={3}>
					<SituationMenu situation={this.state.situation} addPartner={this.addPartner} addChild={this.addChild} onSelect={name => {this.setState({selected: name});}}/>
				</Col>
				<Col xl={6}>
					<SituationControls defaultEntity="head" selected={this.state.selected} situation={this.state.situation} onEnter={this.onEnter}/>
				</Col>
				<Col xl={3}>
					<SituationOverview policy={this.props.policy} situation={this.state.situation} onSubmit={() => {this.props.onSubmit(this.state.situation);}}/>
				</Col>
			</Row>
		);
	}
}

export default Situation;