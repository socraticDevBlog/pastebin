const environment = document
  .querySelector('meta[name="environment"]')
  .getAttribute("content");
const API_URL =
  environment === "production"
    ? "https://paste.socratic.dev/paste"
    : "http://127.0.0.1:3000/paste";

const TIMEOUT_MS = 10000;

function getClientId() {
  const queryParams = new URLSearchParams(window.location.search);
  const clientId = queryParams.get("cid");
  return clientId !== null ? clientId : null;
}
function utf8ToBase64(str) {
  return btoa(unescape(encodeURIComponent(str)));
}

async function submitText() {
  const textInput = document.getElementById("pasteContent");
  const textData = textInput.value;

  let content;
  if (textData) {
    content = textData;
  } else {
    alert("Please enter text to be saved");
    return;
  }

  // base64 encode content to preserve formatting
  content = utf8ToBase64(content);

  // Create a JSON object with "content" as the key
  var data = {
    content: content,
  };

  var clientId = getClientId();
  if (clientId !== null) {
    data["client_id"] = clientId;
  }

  // Convert the JSON object to a string
  const jsonData = JSON.stringify(data);

  // Send the data to the API using the fetch API
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      body: jsonData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    const result = await response.json();

    // Display the API response on the web page
    const responseContainer = document.getElementById("responseContainer");
    var id = result["id"];
    id = id.replace('"', "");
    const url = `${API_URL}?id=${id}`;
    responseContainer.innerHTML = `<p>Visit this URL to view most recent paste: <a href=${url}>${url}</a></p>`;
    textInput.value = ""; //clearing textbox from its value
  } catch (error) {
    console.error("Error sending data to API:", error);
    alert("Error sending data to API");
  }
}

async function displayPasteUrls() {
  var pastebinAPIuri = `${API_URL}/api/pastes`;
  var clientId = getClientId();
  console.log("muh client id");
  console.log(clientId);
  if (clientId !== null) {
    pastebinAPIuri = pastebinAPIuri + "?client_id=" + clientId;
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const response = await fetch(pastebinAPIuri, {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    // Setup timeout for JSON parsing
    const jsonPromise = response.json();
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("JSON parsing timed out")), TIMEOUT_MS)
    );

    const data = await Promise.race([jsonPromise, timeoutPromise]);

    // Get the div where we'll display the latest Paste Urls
    const urlsDiv = document.getElementById("latestPasteUrls");

    // Display each Url
    data.forEach((url) => {
      const p = document.createElement("p");
      p.innerHTML = `<a href="${url}" target="_blank">${url}</a>`;
      urlsDiv.appendChild(p);
    });
  } catch (error) {
    console.error("Error fetching strings from API:", error);
    alert("Error fetching strings from API.");
  }
}

function toggleMode() {
  document.body.classList.toggle("dark-mode");
  const isDark = document.body.classList.contains("dark-mode");

  // Save user preference
  localStorage.setItem("darkMode", isDark ? "enabled" : "disabled");

  // Change button icon
  document.getElementById("toggleModeButton").innerHTML = isDark ? "☀️" : "🌙";
}

document
  .getElementById("pasteContent")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault(); // Prevents adding a new line
      submitText(); // Triggers submit
    }
  });

window.onload = function () {
  displayPasteUrls();
  const darkModeSetting = localStorage.getItem("darkMode");

  if (darkModeSetting !== "disabled") {
    document.body.classList.add("dark-mode");
    document.getElementById("toggleModeButton").innerHTML = "☀️";
  } else {
    document.getElementById("toggleModeButton").innerHTML = "🌙";
  }
  document.getElementById("pasteContent").focus();
};
