document.getElementById("askBtn").addEventListener("click", async () => {
	const question = document.getElementById("question").value;
	const responseElem = document.getElementById("response");

	responseElem.textContent = "Thinking...";

	// Get current tab's YouTube video ID
	const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
	const url = new URL(tab.url);
	const videoId = url.searchParams.get("v");

	if (!videoId) {
		responseElem.textContent = "Not a valid YouTube video.";
		return;
	}

	// Call your backend
	try {
		const res = await fetch("https://yt-rag-api.onrender.com/ask", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ video_id: videoId, question }),
		});

		const data = await res.json();
		responseElem.textContent = data.answer;
	} catch (err) {
		responseElem.textContent = "Error: " + err.message;
	}
});
