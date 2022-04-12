const anime_list = document.getElementById("animes");
const ep_range = document.getElementById("ep-range");
const ep_input = document.querySelector("input[name=ep-range]");

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

const optionDataset = () =>
	document.querySelector(
		`#animes>option:nth-of-type(${anime_list.selectedIndex + 1})`
	).dataset;

function indexChange() {
	const option = optionDataset();

	// storing the raw in hidden elements
	const name_of_anime = document.querySelector("input[name='name']")
	const image_of_anime = document.querySelector("input[name='image']")
	// staring raw
	name_of_anime.value = document.querySelector(
		`#animes>option:nth-of-type(${anime_list.selectedIndex + 1})`
	).value;

	image_of_anime.value = option.image;


	// Image of the anime
	document.querySelector(".center > section > img").src = option.image;

	ep_input.max = ep_range.max = option.total;
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
}


ep_range.addEventListener("change", setTotal);
ep_range.addEventListener("mousemove", setTotal);
ep_input.addEventListener("input", setTotal);

// here order matters, first index and then range
indexChange();
