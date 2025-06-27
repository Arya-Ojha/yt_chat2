document.getElementById("askBtn").addEventListener("click", async () => {
	const question = document.getElementById("question").value;
	const responseElem = document.getElementById("response");
	responseElem.textContent = " Thinking...";

	try {
		const [tab] = await chrome.tabs.query({
			active: true,
			currentWindow: true,
		});
		const url = new URL(tab.url);
		const videoId = url.searchParams.get("v");

		if (!videoId) {
			responseElem.textContent = " Not a valid YouTube video URL.";
			return;
		}

		const res = await fetch("http://localhost:8000/ask", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ video_id: videoId, question }),
		});

		const text = await res.text();

		try {
			const data = JSON.parse(text);
			responseElem.textContent = data.answer || "Got a response.";
		} catch {
			responseElem.textContent = "Server responded with non-JSON data.";
			console.error("Raw server response:", text);
		}
	} catch (err) {
		console.error(err);
		responseElem.textContent = ` Error: ${err.message}`;
	}
});
