const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	darkMode: 'selector',

	theme: {
		extend: {
			fontFamily: {
				'sans': ['"Inter"', 'sans-serif'],
			},
		}
	}
};

module.exports = config;