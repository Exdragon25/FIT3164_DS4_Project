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

var element = document.getElementById('resetBtn');
element.onclick = function () {
   let collection = document.querySelectorAll('input[type="checkbox"]')
   for(j in collection){
   //searching for matching names (for checkboxes)
       collection[j].checked=false
   }
};

function choose_page(next_page_num){
    // let next_page_num = $(this).data('id')
    let cur_url = window.location.href
    let cur_url_var = cur_url.split('/')
    // const cur_url_path = window.location.pathname;
    // var cur_url_var = cur_url.split('/')
    const new_URL = window.location.host + '/'+ next_page_num + '/' + cur_url_var[cur_url_var.length-1]
    window.location.assign(new_URL)
}



