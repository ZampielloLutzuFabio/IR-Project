function toggleFilters() {
    var filterFields = document.getElementsByClassName('filter');
    for (var i = 0; i < filterFields.length; i++) {
        if (filterFields[i].style.display === "none") {
            filterFields[i].style.display = "inline";
        } else {
            filterFields[i].style.display = "none";
        }
    }
}

function quote(obj) {
    var return_val = '((';
    var firstElem = true;

    for (const [key, value] of Object.entries(obj)) {
        if (!Array.isArray(value)) {
            value = [value]
        }

        value.forEach(val => {
            if (val != "*") {
                if (firstElem) {
                    return_val += '(' + key + ':"' + val + '")';
                    firstElem = false
                } else {
                    return_val += 'OR(' + key + ':"' + val + '")'
                }
            } else {
                if (firstElem) {
                    return_val += '(' + key + ':' + val + ')';
                    firstElem = false
                } else {
                    return_val += 'OR(' + key + ':' + val + ')'
                }
            }
        })
    }

    return return_val;

}

function quote_filter(obj) {
    if (Object.keys(obj).length == 0) {
        return "))";
    }

    var return_val = ")";

    for (const [key, value] of Object.entries(obj)) {
        if (!value || (value.length == 1 && !value[0])) {
            continue;
        } else {
            if (!Array.isArray(value)) {
                value = [value]
            }
            value.forEach(val => {
                return_val += 'AND(' + key + ':"' + val + '")';
            })
        }
    }

    return_val += ")"

    return return_val;

}

function openLink(url) {
    window.open(url, '_blank');
}

function populate_table(array) {
    var table = document.querySelector('tbody');

    var t = "";

    for (var i = 0; i < array.length; i++) {
        if (array[i]['genre'] === undefined) {
            array[i]['genre'] = ['No Genre'];
        }
        var tr = '<tr onclick=openLink("' + array[i]['href'] + '")>';
        tr += "<td>" + array[i]['title'] + "</td>";
        tr += "<td>" + array[i]['author'] + "</td>";
        tr += "<td>" + array[i]['genre'].slice(0, 5) + "</td>";
        tr += "<td>" + array[i]['platform'] + "</td>";
        tr += "<td>" + array[i]['price'] + "</td>";
        tr += "<td>" + array[i]['sale'] + "</td>";
        tr += "<td>" + array[i]['description'] + "</td>";
        tr += "</tr>";
        t += tr;
    }

    if (t.length == 0) {
        t += "<tr>";
        t += "<td colspan='7'>No Results Were Found</td>";
        t += "</tr>";
    }

    table.innerHTML = t;
}


function search() {
    var url = 'http://localhost:8983/solr/indiegames/query?rows=1000&q=';

    var query = document.getElementById('searchGame').value.split('|');

    var obj = {
        title: query,
        platform: query,
        author: query,
        genre: query
    }

    var filter = {
        genre: document.getElementById('genreFilter').value.split("|"),
        price: document.getElementById('priceFilter').value.split("|"),
        sale: document.getElementById('saleFilter').value.split("|"),
        author: document.getElementById('authorFilter').value.split("|"),
        platform: document.getElementById('platformFilter').value.split("|"),
    }

    url += encodeURI(quote(obj) + quote_filter(filter));

    fetch(url, {
        method: "GET",
        headers: {
            Accept: 'application/json'
        }
    }).then(function (response) {
        return response.json();
    }).then(data => {
        populate_table(data.response.docs);
    });

}


var inputs = document.querySelectorAll('input');

for (var input of inputs) {
    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            document.getElementById("searchButton").click();
        }
    });
}