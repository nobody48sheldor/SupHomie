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


var dash1 = document.getElementById("dashItem--1");
var dash2 = document.getElementById("dashItem--2");
var dash3 = document.getElementById("dashItem--3");
var dash4 = document.getElementById("dashItem--4");
var dash5 = document.getElementById("dashItem--5");


function ClearAllClass() {
	dash1.classList.remove("hover1")
	dash1.classList.remove("hover2")
	dash1.classList.remove("hover3")
	dash1.classList.remove("hover4")
	dash1.classList.remove("hover5")

	dash2.classList.remove("hover1")
	dash2.classList.remove("hover2")
	dash2.classList.remove("hover3")
	dash2.classList.remove("hover4")
	dash2.classList.remove("hover5")

	dash3.classList.remove("hover1")
	dash3.classList.remove("hover2")
	dash3.classList.remove("hover3")
	dash3.classList.remove("hover4")
	dash3.classList.remove("hover5")

	dash4.classList.remove("hover1")
	dash4.classList.remove("hover2")
	dash4.classList.remove("hover3")
	dash4.classList.remove("hover4")
	dash4.classList.remove("hover5")
	
	dash5.classList.remove("hover1")
	dash5.classList.remove("hover2")
	dash5.classList.remove("hover3")
	dash5.classList.remove("hover4")
	dash5.classList.remove("hover5")
}

// Add a new class

dash1.addEventListener('mouseover', function() {
	dash1.classList.add("hover1");
	dash2.classList.add("hover1");
	dash3.classList.add("hover1");
	dash4.classList.add("hover1");
	dash5.classList.add("hover1");
});

dash1.addEventListener('mouseout', function() {
	ClearAllClass();
});


dash2.addEventListener('mouseover', function() {
	dash1.classList.add("hover2");
	dash2.classList.add("hover2");
	dash3.classList.add("hover2");
	dash4.classList.add("hover2");
	dash5.classList.add("hover2");
});

dash2.addEventListener('mouseout', function() {
	ClearAllClass();
});


dash3.addEventListener('mouseover', function() {
	dash1.classList.add("hover3");
	dash2.classList.add("hover3");
	dash3.classList.add("hover3");
	dash4.classList.add("hover3");
	dash5.classList.add("hover3");
});

dash3.addEventListener('mouseout', function() {
	ClearAllClass();
});


dash4.addEventListener('mouseover', function() {
	dash1.classList.add("hover4");
	dash2.classList.add("hover4");
	dash3.classList.add("hover4");
	dash4.classList.add("hover4");
	dash5.classList.add("hover4");
});

dash4.addEventListener('mouseout', function() {
	ClearAllClass();
});


dash5.addEventListener('mouseover', function() {
	dash1.classList.add("hover5");
	dash2.classList.add("hover5");
	dash3.classList.add("hover5");
	dash4.classList.add("hover5");
	dash5.classList.add("hover5");
});

dash5.addEventListener('mouseout', function() {
	ClearAllClass();
});
