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

var audio = document.getElementById('player');
audio.onended = function() {
	document.getElementById("next_song").submit();
};

function playmusic() {
	const play = document.getElementById("play").innerHTML;
	if (play == 1) {
		document.getElementById('player').play();
	}
};
