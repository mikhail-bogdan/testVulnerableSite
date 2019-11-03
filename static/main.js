var temp = document.getElementById("temperature_indicator");
var light = document.getElementById("light_indicator");
var humidity = document.getElementById("humidity_indicator");
var button1 = document.getElementById("button_1");
var button2 = document.getElementById("button_2");

var lastStateOfButton1 = 0, lastStateOfButton2 = 0;

button1.onclick = function(){
	var newState = lastStateOfButton1 == 1 ? 0 : 1;
	fetch("/api/changeStateOfSomething1?newState=" + newState)
		.then(function(d){
			return d.json();
		})
		.then(function(d){
			if(d.result != 1)
				throw new Exception("Unsuccessful result");
			
			lastStateOfButton1 = newState;
			updateButtonIndicator(button1, {state: newState, name: "---"});
		})
		.catch(function(err){
			console.log(err);
		});
}

button2.onclick = function(){
	var newState = lastStateOfButton2 == 1 ? 0 : 1;
	fetch("/api/changeStateOfSomething2?newState=" + (lastStateOfButton2 == 1 ? 0 : 1))
		.then(function(d){
			return d.json();
		})
		.then(function(d){
			if(d.result != 1)
				throw new Exception("Unsuccessful result");
			
			lastStateOfButton2 = newState;
			updateButtonIndicator(button2, {state: newState, name: "..."});
		})
		.catch(function(err){
			console.log(err);
		});
}

function updateLoadIndicator(element, data){
	var value = element.querySelector("#value");
	if(value.textContent != data.value)
		value.textContent = data.value;
	
	var unit = element.querySelector("#unit");
	if(unit.textContent != data.unit)
		unit.textContent = data.unit;
	
	var load = element.querySelector("#load");
	
	if(data.load == 100)
		data.load = 99.999;
	var angle = 360 * data.load / 100 - 270;
	var angleRad = angle / 360 * 2 * Math.PI;
	var x = Math.cos(angleRad), y = Math.sin(angleRad);
	x *= 50;
	y *= 50;
	var f = data.load <= 50 ? 0 : 1;
	load.setAttribute("d", "M 0,0 l 0,50 A 50,50 -90 " + f + ",1 " + x + "," + y + " z");
	load.classList.toggle("indicator-normal-state", data.alert != 1);
	load.classList.toggle("indicator-alert-state", data.alert == 1);
}

function updateButtonIndicator(element, data){
	var state = element.querySelector("#state");
	var stateName = data.state == 1 ? "ON" : "OFF";
	if(state.textContent != stateName)
		state.textContent = stateName;
	
	var name = element.querySelector("#name");
	if(name.textContent != data.name)
		name.textContent = data.name;
	
	var backlight = element.querySelector("#backlight");
	backlight.classList.toggle("indicator-on-state", data.state == 1);
	backlight.classList.toggle("indicator-off-state", data.state != 1);
}

function loop(){
	fetch("/api/getData")
		.then(function(d){
			return d.json();
		})
		.then(function(d){
			//here we have all our data
			updateLoadIndicator(temp, d.temperature);
			updateLoadIndicator(light, d.light);
			updateLoadIndicator(humidity, d.humidity);
			updateButtonIndicator(button1, d.stateOfSomething1);
			updateButtonIndicator(button2, d.stateOfSomething2);
			
			lastStateOfButton1 = d.stateOfSomething1.state;
			lastStateOfButton2 = d.stateOfSomething2.state;
			
			//
			setTimeout(loop, 1000);
		})
		.catch(function(err){
			console.log(err);
			setTimeout(loop, 1000);
		});
}

function animation(){
	if(this.nIteration === undefined)
		this.nIteration = 200;
	
	if(this.nIteration == 0){
		loop();
		return;
	}
	
	if(this.nIteration > 100){
		var val = 100 - (this.nIteration - 100);
		updateLoadIndicator(temp, {value: "-", unit: "-", alert: 0, load: val});
		updateLoadIndicator(light, {value: "-", unit: "-", alert: 0, load: val});
		updateLoadIndicator(humidity, {value: "-", unit: "-", alert: 0, load: val});
	}else{
		var val = this.nIteration;
		updateLoadIndicator(temp, {value: "-", unit: "-", alert: 0, load: val});
		updateLoadIndicator(light, {value: "-", unit: "-", alert: 0, load: val});
		updateLoadIndicator(humidity, {value: "-", unit: "-", alert: 0, load: val});
	}
	
	this.nIteration = this.nIteration - 2;
	setTimeout(animation, 10);
}

animation();