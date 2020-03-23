
function convertTimestamptoTime(){
    var timestamp = document.querySelectorAll("[id='timestamp']");
    for(var i = 0; i < timestamp.length; i++){
      dateObj = new Date(timestamp[i].innerHTML * 1); 
      utcString = dateObj.toUTCString(); 
      timestamp[i].innerHTML = utcString;
    }
}