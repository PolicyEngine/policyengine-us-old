export const DEFAULT_HOUSEHOLD = {
};

export const DEFAULT_FAMILY = {
};

export const DEFAULT_ADULT = {
	age: {
		title: "Age",
		description: "The age of the person",
		default: 18,
		value: 18,
		min: 18,
		max: 80
	},
	e00200: {
		title: "Employment income",
		description: "Income from employment (gross)",
		default: 0,
		value: 0,
		max: 80000,
		type: "yearly"
	}
};

export const DEFAULT_CHILD = {
	age: {
		title: "Age",
		description: "The age of the person",
		default: 10,
		value: 10,
		min: 0,
		max: 17
	},
	e00200: {
		title: "Employment income",
		description: "Income from employment (gross)",
		default: 0,
		value: 0,
		max: 80000,
		type: "yearly"
	},
};

export const DEFAULT_TAX_UNIT = {
	c00100: {
		title: "Adjusted Gross Income",
		description: "Main measure of income for the tax unit",
		default: 0,
		value: 0,
		max: 80000,
		type: "yearly"
	},
};

const DEFAULT_SITUATION = {
	household: JSON.parse(JSON.stringify(DEFAULT_HOUSEHOLD)),
	tax_units: {
		"tax_unit_1": {
			...JSON.parse(JSON.stringify(DEFAULT_TAX_UNIT)),
		}
	},
	people: {
		"head": JSON.parse(JSON.stringify(DEFAULT_ADULT))
	}
};

export default DEFAULT_SITUATION;