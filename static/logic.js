var inputdivs = {}
var buttons = {}

summary_mode = "text"
var url = window.location.href;

if (document.querySelector(".output").innerHTML.length > 0)
	summary_mode = "doc"
	document.querySelector(".output").classList.remove("remove")

inputdivs["text"] = document.querySelector(".text-div")
inputdivs["key"] = document.querySelector(".key-div")
inputdivs["doc"] = document.querySelector(".doc-div")
inputdivs["link"] = document.querySelector(".link-div")
buttons["text"] = document.querySelector(".text-option")
buttons["key"] = document.querySelector(".key-option")
buttons["doc"] = document.querySelector(".doc-option")
buttons["link"] = document.querySelector(".link-option")

function setVisible(divname, clear = true) {
	if (clear)
		document.querySelector(".output").classList.add("remove")
	const divKeys = Object.keys(inputdivs)
	for (var key in divKeys) {
		if (divKeys[key] != divname)
			inputdivs[divKeys[key]].classList.add("remove")
		else
			inputdivs[divKeys[key]].classList.remove("remove")
	}
	const buttonKeys = Object.keys(buttons)
    console.log(buttons, buttonKeys)
	for (var key in buttonKeys) {
		if (buttonKeys[key] == divname){
			buttons[buttonKeys[key]].classList.add("bg-blue-600")
			buttons[buttonKeys[key]].classList.add("text-white")
			buttons[buttonKeys[key]].classList.remove("bg-gray-300")
			buttons[buttonKeys[key]].classList.remove("text-gray-800")
		}
		else{
		    buttons[buttonKeys[key]].classList.add("bg-gray-300")
		    buttons[buttonKeys[key]].classList.add("text-gray-800")
			buttons[buttonKeys[key]].classList.remove("bg-blue-600")
			buttons[buttonKeys[key]].classList.remove("text-white")
		}
	}
}


function text(){
	summary_mode = "text"
	setVisible(summary_mode)
}

function keyword(){
	summary_mode = "key"
	setVisible(summary_mode)
}

function doc(){
	summary_mode = "doc"
	setVisible(summary_mode)
}

function link(){
	summary_mode = "link"
	setVisible(summary_mode)
}

document.querySelector(".summarize").addEventListener("click", process)
function process(){

	if (summary_mode == "doc"){
		var formData = new FormData();
		formData.append('image', $('input[type=file]')[0].files[0]);

		$.ajax({
			url: 'upload',
			data: formData,
			type: 'POST',
			contentType: false,
			processData: false,
			success: function(msg) {
				document.querySelector(".output").value = msg
			},
			error: function() {
				document.querySelector(".output").value = "Something went wrong :("
			}
		});
	} else {
		var query = "." + summary_mode + "-div"
		const text = document.querySelector(query).value
		console.log(text)

		const toSend = {
				data : text,
			mode : summary_mode
		};

		const jsonString = JSON.stringify(toSend)
		var req = new XMLHttpRequest()

		req.onload = function(){
			output_box = document.querySelector(".output")
			output_box.classList.remove("remove")
			output_box.value = this.response
			sum_btn.innerHTML = "Start"
			sum_btn.disabled = false
			sum_btn.style.cursor = "pointer"
		};

		req.open("POST", "process");
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		sum_btn = document.querySelector(".summarize")
		sum_btn.innerHTML = "Working..."
		sum_btn.disabled = true
		sum_btn.style.cursor = "wait"
		req.send(jsonString)
	}
}
setVisible(summary_mode, false)