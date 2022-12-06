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
            if (firstElem) {
                return_val += '(' + key + ':*' + val + '*)';
                firstElem = false
            } else {
                return_val += 'OR(' + key + ':*' + val + '*)'
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
                return_val += 'AND(' + key + ':*' + val + '*)';
            })
        }
    }

    return_val += ")"

    return return_val;

}

function openLink(url) {
    window.open(url, '_blank');
}

function populate_table(array, query) {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    
    var table = document.querySelector('table');
    var tutorialBox = document.querySelector('#tutorial');
    var tableBody = document.querySelector('tbody');

    var t = "";

    for (var i = 0; i < array.length; i++) {
        if (array[i]['genre'] === undefined) {
            array[i]['genre'] = ['No Genre'];
        }

        array[i]['title'] = array[i]['title'].join(',');
        array[i]['author'] = array[i]['author'].join(',');
        array[i]['genre'] = array[i]['genre'].slice(0, 5).join(',');
        array[i]['platform'] = array[i]['platform'].join(',');
        array[i]['price'] = array[i]['price'].join(',');
        array[i]['sale'] = array[i]['sale'].join(',');
        array[i]['description'] = array[i]['description'].join(',');

        query.forEach(q => { array[i]['title'] = array[i]['title'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['author'] = array[i]['author'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['genre'] = array[i]['genre'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['platform'] = array[i]['platform'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['price'] = array[i]['price'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['sale'] = array[i]['sale'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['description'] = array[i]['description'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });

        var tr = '<tr onclick=openLink("' + array[i]['href'] + '")>';
        tr += "<td>" + array[i]['title'] + "</td>";
        tr += "<td>" + array[i]['author'] + "</td>";
        tr += "<td>" + array[i]['genre'] + "</td>";
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

    tableBody.innerHTML = t;

    if (table.style.display === "none") {
        table.style.display = "block";
        tutorialBox.style.display = "none";
    }
}

function search() {
    var url = 'http://localhost:8983/solr/indiegames/query?rows=1000&q=';

    var query = document.getElementById('searchGame').value.split(',');
    for (var i = 0; i < query.length; i++) {
        query[i] = query[i].trim();
    }

    var obj = {
        title: query,
        platform: query,
        author: query,
        genre: query
    }

    var filter = {
        genre: document.getElementById('genreFilter').value.split(","),
        price: document.getElementById('priceFilter').value.split(","),
        sale: document.getElementById('saleFilter').value.split(","),
        author: document.getElementById('authorFilter').value.split(","),
        platform: document.getElementById('platformFilter').value.split(","),
    }

    url += encodeURI(quote(obj) + quote_filter(filter));

    console.log(url);

    fetch(url, {
        method: "GET",
        headers: {
            Accept: 'application/json'
        }
    }).then(function (response) {
        return response.json();
    }).then(data => {
        populate_table(data.response.docs, query);
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