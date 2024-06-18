console.log('hey wassup how is it going, saying it live from the main.js file homie')

const { createApp } = Vue
const main = {
	data()
	{
		return {
			hist: "",
		}
	},
	delimiters: ["{", "}"]
}

createApp(main).mount("#vue")
