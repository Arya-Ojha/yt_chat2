const askBtn = document.getElementById("askBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");
const questionInput = document.getElementById("question");
const responseElem = document.getElementById("response");
const loadingElem = document.getElementById("loading");

askBtn.addEventListener("click", async () => {
	const question = questionInput.value.trim();
	if (!question) return;

	responseElem.textContent = "";
	loadingElem.classList.remove("hidden");
	copyBtn.classList.add("hidden");

	try {
		const [tab] = await chrome.tabs.query({
			active: true,
			currentWindow: true,
		});
		const url = new URL(tab.url);
		const videoId = url.searchParams.get("v");

		if (!videoId) {
			responseElem.textContent = "❌ Not a valid YouTube video.";
			return;
		}

		const res = await fetch("https://yt-chat2.onrender.com/ask", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ video_id: videoId, question }),
		});

		const data = await res.json();
		responseElem.textContent = data.answer;
		copyBtn.classList.remove("hidden");
	} catch (err) {
		responseElem.textContent = `❌ Error: ${err.message}`;
	} finally {
		loadingElem.classList.add("hidden");
	}
});

clearBtn.addEventListener("click", () => {
	questionInput.value = "";
	responseElem.textContent = "Your answer will appear here.";
	copyBtn.classList.add("hidden");
});

copyBtn.addEventListener("click", () => {
	navigator.clipboard.writeText(responseElem.textContent);
	copyBtn.textContent = "✅ Copied!";
	setTimeout(() => {
		copyBtn.textContent = "📋 Copy Answer";
	}, 1500);
});
