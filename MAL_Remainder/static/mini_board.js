const anime_list = document.getElementById("animes");
const ep_range = document.getElementById("ep-range");

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
	document.querySelector(".center > section > img").src = option.image;
	ep_range.max = option.left;
	ep_range.value = 0;
	changeRange();
}

anime_list.addEventListener("change", indexChange);

function changeRange() {
	const range = document.querySelector("input[name='ep-range']");
	const option = optionDataset();

	range.value = ep_range.value;

	range.previousElementSibling.previousElementSibling.value = option.done;
	range.nextElementSibling.nextElementSibling.value = option.total;
}

ep_range.addEventListener("change", changeRange);
ep_range.addEventListener("mousemove", changeRange);

// here order matters, first index and then range
indexChange();
changeRange();
