import { Menu } from "antd";
import React from "react";

const { SubMenu } = Menu;

class PolicyMenu extends React.Component {
	render() {
		return (
			<Menu
				onClick={(e) => {this.props.onClick(e.key);}}
				mode="inline"
				defaultOpenKeys={["benefits"]}
			>
				<SubMenu key="benefits" title="Benefits">
					<Menu.Item key="UBI">Universal Basic Income</Menu.Item>
				</SubMenu>
			</Menu>
		);
	}
}

export default PolicyMenu;