console.log('hey wassup homie !')

const { createApp } = Vue
var main = {
	data()
	{

		return {
			hist: "",
		}
	},
	delimiters: ["{", "}"]
}

createApp(main).mount("#vue")
