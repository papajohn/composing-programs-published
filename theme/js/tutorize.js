var editURL = "http://tutor.composingprograms.com/visualize.html";

function htmlDecode(value){
  return $('<div/>').html(value).text();
}

// tutorize renders all Online Python Tutor content.
function tutorize() {
    $(".example").each(function(i, e) {
        var id = e.id;
        var trace = eval(id + "_trace");

        // Reverse HTML escaping from docutils
        trace.code = htmlDecode(trace.code)

        var step = eval(e.attributes["data-step"].value);
        var jumpToEnd = null;
        if (step == -1) {
            step = 0;
            jumpToEnd = true;
        }
        var output = e.attributes["data-output"].value == "True";
        var options = {
            jumpToEnd: jumpToEnd,
            startingInstruction: step,
            compactFuncLabels: true,
            editCodeBaseURL: editURL,
            embeddedMode: true,
        }
        e.innerHTML="";
        new ExecutionVisualizer(id, trace, options);
    })
}

// enableHideContents enables the link in the contents titled "Hide Contents".
function enableHideContents() {
    $("#hide_contents").click(function() {
        $(".nav-docs").hide();
        $(".wrap").width("95%");
        $(".inner-content").width("100%");
        globalRepaintEverything();
    });
}

$(document).ready(tutorize); // $(document).ready(jsMath.Synchronize(tutorize))
$(document).ready(enableHideContents);
setTimeout(globalRepaintEverything, 2000);
setTimeout(globalRepaintEverything, 5000);
