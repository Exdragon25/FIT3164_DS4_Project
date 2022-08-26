var sPageURL = window.location.search.substring(1);
var sURLVariables = sPageURL.split('&');
for (i in sURLVariables) {
  let sParameter =sURLVariables[i].split('=');
  let name=sParameter[0]
  let value=decodeURIComponent(sParameter[1])
  value = value.replace("+", " ")
  if (name=='search'){
    document.getElementById("search").value = value
  }
  //Here is a loop
  //Do something for each name-value pair
  let collection = document.getElementsByName(name)
  for(j in collection){
    //searching for matching names (for checkboxes)
    if(collection[j].value==value)collection[j].checked=true
  }
}
//reference: https://stackoverflow.com/questions/53412961/function-to-select-options-and-check-checkboxes-based-on-url-params-on-document
