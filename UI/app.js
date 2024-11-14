/*Dropzone.autoDiscover = false;

import express from 'express';
import { join } from 'path';
const app = express();

app.use('/static', express.static(join(__dirname, 'public')));

// In your HTML
// <link rel="icon" href="/static/favicon.ico" type="image/x-icon">

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "http://127.0.0.1:5000/classify_image",  // Updated URL
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/classify_image";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
         
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let players = ["lionel_messi", "maria_sharapova", "roger_federer", "serena_williams", "virat_kohli"];
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.class}"`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
*/



Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {

        url: "/classify_image",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false,
    });

    dz.on("addedfile", function() {
        if (dz.files[1] != null) {
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("complete", function (file) {
        // Use FileReader to convert image to Base64
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function() {
            let imageData = reader.result; // this is the base64 image data

            var url = "http://127.0.0.1:5000/classify_image";

            $.post(url, {
                image_data: imageData
            }, function(data, status) {
                // Handle response from the server
                console.log(data);
                if (!data || data.length == 0) {
                    $("#resultHolder").hide();
                    $("#divClassTable").hide();
                    $("#error").show();
                    return;
                }

                let players = ["lionel_messi", "maria_sharapova", "roger_federer", "serena_williams", "virat_kohli"];
                let match = null;
                let bestScore = -1;
                
                // Find the best match
                for (let i = 0; i < data.length; ++i) {
                    let maxScoreForThisClass = Math.max(...data[i].class_probability);
                    if (maxScoreForThisClass > bestScore) {
                        match = data[i];
                        bestScore = maxScoreForThisClass;
                    }
                }

                if (match) {
                    $("#error").hide();
                    $("#resultHolder").show();
                    $("#divClassTable").show();
                    $("#resultHolder").html($(`[data-player="${match.class}"`).html());

                    let classDictionary = match.class_dictionary;
                    for (let personName in classDictionary) {
                        let index = classDictionary[personName];
                        let probabilityScore = match.class_probability[index];
                        let elementName = "#score_" + personName;
                        $(elementName).html(probabilityScore);
                    }
                }
            });
        };
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();
    });
}

$(document).ready(function() {
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();
    init();
});


/*
Dropzone.autoDiscover = false;

function handleFileAdded(dz) {
    if (dz.files[1] != null) {
        dz.removeFile(dz.files[0]);        
    }
}

function handleFileComplete(file) {
    let imageData = file.dataURL;
    let url = "http://127.0.0.1:5000/classify_image";

    $.post(url, { image_data: imageData }, function(data, status) {
        if (!data || data.length == 0) {
            showError();
            return;
        }

        let bestMatch = findBestMatch(data);
        if (bestMatch) {
            showResult(bestMatch);
        } else {
            showError();
        }
    }).fail(function() {
        showError();
    });
}

function findBestMatch(data) {
    let bestScore = -1;
    let match = null;
    for (let i = 0; i < data.length; i++) {
        let maxScoreForThisClass = Math.max(...data[i].class_probability);
        if (maxScoreForThisClass > bestScore) {
            match = data[i];
            bestScore = maxScoreForThisClass;
        }
    }
    return match;
}

function showResult(match) {
    $("#error").hide();
    $("#resultHolder").show();
    $("#divClassTable").show();
    $("#resultHolder").html($(`[data-player="${match.class}"]`).html());

    let classDictionary = match.class_dictionary;
    for (let personName in classDictionary) {
        let index = classDictionary[personName];
        let probabilityScore = match.class_probability[index];
        let elementName = "#score_" + personName;
        $(elementName).html(probabilityScore);
    }
}

function showError() {
    $("#resultHolder").hide();
    $("#divClassTable").hide();
    $("#error").show();
}

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/", // Update this if needed
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Drag and drop an image here or click to upload",
        autoProcessQueue: false
    });

    dz.on("addedfile", function() {
        handleFileAdded(dz);
    });

    dz.on("complete", function(file) {
        handleFileComplete(file);
    });

    $("#submitBtn").on('click', function(e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log("Document ready!");
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
*/





/*
Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "http://127.0.0.1:5000/classify_image",  // Corrected URL
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1] != null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        var url = "http://127.0.0.1:5000/classify_image";
        $.post(url, {
            image_data: file.dataURL
        }, function(data, status) {
            console.log(data);
            if (!data || data.length == 0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let players = ["lionel_messi", "maria_sharapova", "roger_federer", "serena_williams", "virat_kohli"];
            
            let match = null;
            let bestScore = -1;
            for (let i = 0; i < data.length; ++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if (maxScoreForThisClass > bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.class}"]`).html());
                let classDictionary = match.class_dictionary;
                for (let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let probabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(probabilityScore);
                }
            }
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();        
    });
}

$(document).ready(function() {
    console.log("ready!");
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
*/