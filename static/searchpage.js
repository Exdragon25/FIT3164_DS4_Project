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


    // for (i=0; i<document.filter1.cuisine.length;i++)
    //     document.filter1.cuisine[i].checked = false;
    // for (i=0; i<document.filter2.taste.length;i++)
    //     document.filter2.taste[i].checked = false;
    // for (i=0; i<document.filter3.course.length;i++)
    //     document.filter3.course[i].checked = false;

