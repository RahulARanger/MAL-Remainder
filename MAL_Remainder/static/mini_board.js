const anime_list = document.getElementById("animes");
const ep_range = document.getElementById("ep-range");
const ep_input = document.querySelector("input[name=ep-range]");

ep_range.focus();

function formatDate(text) {
	const date = new Date(text);
	const [minutes, hours] = [
		String(date.getMinutes()),
		String(date.getHours()),
	];

	return `${date.getDate()}/${
		date.getMonth() + 1
	}/${date.getFullYear()}  ${hours.padStart(2, "0")}::${minutes.padStart(
		2,
		"0"
	)}`;
}

document.querySelectorAll("#animes > option").forEach(function (option) {
	const [date, start, end] = option.title.split(",");
	let formatted = `Status Updated: ${formatDate(date)}`;
	start && (formatted += `\nStarted: ${formatDate(start)}`);
	end && (formatted += `\nEnded: ${formatDate(end)}`);
	option.title = formatted;
});

const selectedOption = () => document.querySelector(
	`#animes>option:nth-of-type(${anime_list.selectedIndex + 1})`
)
const optionDataset = () =>
	selectedOption().dataset;

const getInputByName = (name) => document.querySelector(`input[name="${name}"]`)


function setValue(id_value, value){
	getInputByName(id_value).value = value;
	document.getElementById(id_value).textContent = value;
}


function indexChange() {
	const option = optionDataset();
	const selected = selectedOption();

	document.querySelector("select").title = selected.title;
	// staring raw
	getInputByName("name").value = selected.label;
	getInputByName("image").value = option.image;
	getInputByName("duration").value = option.duration;

	setValue("genres", option.genre);
	setValue("rank", option.rank);
	setValue("score", option.score);
	setValue("popularity", option.popularity);
	setValue("rating", option.rating);


	// Image of the anime
	document.querySelector(".center > section > img").src = option.image;

	ep_input.max = ep_range.max = option.total - Number(option.done);
	ep_input.min = ep_range.min = -Number(option.done);
	ep_input.value = ep_range.value = 0;
	
	
	ep_input.previousElementSibling.previousElementSibling.value = option.done;
	ep_input.nextElementSibling.nextElementSibling.value = option.total;
	
}

anime_list.addEventListener("change", indexChange);


function setTotal(event){
	const track = [ep_range, ep_input] 
	
	if(event.srcElement.type !== "range"){
		track.reverse();
	}
	track[1].value = track[0].value;
	
	ep_range.title = (
		track[0].value > 0
		) ? `😄 you have watched ${track[0].value} episodes.` : (
			track[0].value < 0
			) ? `😉 ReWatching shows is fun!`: `So you didn't watch any episode 🤨`;
}


ep_range.addEventListener("change", setTotal);
ep_range.addEventListener("mousemove", setTotal);
ep_input.addEventListener("input", setTotal);

// here order matters, first index and then range
indexChange();
