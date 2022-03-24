const anime_list = document.getElementById("animes");
const ep_range = document.getElementById("ep-range");

document.querySelectorAll("#animes > option").forEach(function (option) {
	const date = new Date(option.title);
	const [minutes, hours] = [
		String(date.getMinutes()),
		String(date.getHours()),
	];

	option.title = `${date.getDate()}/${
		date.getMonth() + 1
	}/${date.getFullYear()}  ${hours.padStart(2, "0")}::${minutes.padStart(
		2,
		"0"
	)}`;
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
}

anime_list.addEventListener("change", indexChange);

function changeRange() {
	const range = document.querySelector("label[for='ep-range']");
	const option = optionDataset();

	range.textContent = ep_range.value;

	range.previousElementSibling.textContent = option.done;
	range.nextElementSibling.nextElementSibling.textContent = option.total;
}

ep_range.addEventListener("change", changeRange);
ep_range.addEventListener("mousemove", changeRange);

changeRange();
indexChange();
