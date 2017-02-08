// Scripts for the timesheet

function getInfo(name){
            if (name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search)) {
                return decodeURIComponent(name[1]);
            } else {
                return "error";
            }
        }



