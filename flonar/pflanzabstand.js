export function buttonFetchRate_click(event) {
  let url = 'https://exchangeratesapi.io/api/latest?base=USD';
  let symbol = $w("#textInputSymbol").value; 
  let fullUrl = url + '&symbols=' + symbol; 
 
  fetch(fullUrl, {method: 'get'})
    .then(response => response.json())
    .then(json => $w("#textRate").text = json.rates[symbol].toString());
}
