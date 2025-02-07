# web client

## working features 🟢

- on page load, recent paste urls get fetched from Pastebin API and get printed
  below the textbox
- saving a new paste (non empty string) by clicking the submit button; then the
  paste URL gets printed below the textbox

## local setup 🐳

best way to test out the UI is targetting a local version of Pastebin API

1. have Docker running
2. (see root Readme) tart DynamoDB local instance using `docker compose`
3. (idem) run API Gateway locally

API endpoint should be `http://127.0.0.1:3000/paste` (if it isn't, simply
change the value in `script.js`)

4. open `index.html` web app in your favorite browser

either by openine the file with your browser, or using a local server like [VS Code
Live Server
plugin](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer).
I ❤️ live server for its hot reload capability

## nice things and gotchas

### environment switching

in `index.html`, using html meta tag `<meta name="environment" content="production">` to switch
between production environment (targetting public API) or local API running on `localhost`
