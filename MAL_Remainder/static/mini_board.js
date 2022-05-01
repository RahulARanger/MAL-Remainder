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


function setValue(id_value, value){
	getInputByName(id_value).value = value;
	document.getElementById(id_value).textContent = value;
}

const getInputByName = (name) => document.querySelector(`input[name="${name}"]`)


class MiniBoard {
	constructor(){
		this.list_id = "anime-list"
		this.anime_list = document.getElementById(this.list_id);
		this.ep_range = document.getElementById("watched");
		this.ep_input = document.getElementById("today");
		this.wear();
	}


	getSelected(){
		return this.anime_list.querySelector(
			`option:nth-of-type(${this.anime_list.selectedIndex + 1})`
		)
	}

	getOptionDataSet(){
		return this.getSelected().dataset;
	}


	wear(){
		this.anime_list.addEventListener("change", this.handleChange.bind(this));

		const from_range = this.handleSliderChange.bind(this, true)
		const from_input = this.handleSliderChange.bind(this, false)
		this.ep_range.addEventListener("change", from_range);
		this.ep_range.addEventListener("mousemove", from_range);
		this.ep_input.addEventListener("input", from_input);
	}

	handleChange(){
		const options = this.getOptionDataSet();
		const selected = this.getSelected();

		getInputByName("name").value = selected.label;
		getInputByName("image").value = options.image;
		getInputByName("duration").value = options.duration;

		setValue("genres", options.genre);
		setValue("rank", options.rank);
		setValue("score", options.score);
		setValue("popularity", options.popularity);
		setValue("rating", options.rating);

		document.querySelector(".center > section > img").src = options.image;


		this.ep_input.max = this.ep_range.max = options.total - Number(options.done);
		this.ep_input.min = this.ep_range.min = -Number(options.done);
		this.ep_input.value = this.ep_range.value = 0;

		document.querySelector("input[name='up_until']").value = options.done;
		document.querySelector("input[name='total']").value = options.total;
		document.getElementById("total_now").value = options.done;
		
	}


	handleSliderChange(from_range=true){
		console.log(from_range);

		if(from_range)
			this.ep_input.value = this.ep_range.value;
		else
			this.ep_range.value = this.ep_input.value;
		
		const so_watched = this.ep_range.value;
		this.ep_range.title = (
			so_watched > 0
			) ? `😄 you have watched ${so_watched} episodes.` : (
				so_watched < 0
				) ? `😉 ReWatching shows is fun!`: `So you didn't watch any episode 🤨`;
		
		document.getElementById("total_now").value = Number(this.ep_input.value) - Number(this.ep_input.min)
	}
}


const board = new MiniBoard();
document.body.addEventListener("click", () => board.ep_range.focus())
board.handleChange();
board.ep_range.focus();



document.querySelectorAll(`#${board.list_id}>label.option`).forEach(function(option){
	const [date, start, end] = option.title.split(",");
	let formatted = `Status Updated: ${formatDate(date)}`;
	start && (formatted += `\nStarted: ${formatDate(start)}`);
	end && (formatted += `\nEnded: ${formatDate(end)}`);
	option.title = formatted;
})
