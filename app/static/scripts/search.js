$(document).ready(function () {
    $('#search-form').on('submit', function (event) {
        event.preventDefault();
        const searchQuery = $('#search-input').val();
        const zipCode = $('#zip-input').val();
        fetchResults(searchQuery, zipCode, 0);
    });

    $('#search-results').on('click', '.pagination-btn', function () {
        const searchQuery = $('#search-input').val();
        const zipCode = $('#zip-input').val();
        const startIndex = $(this).data('start');
        fetchResults(searchQuery, zipCode, startIndex);
    });
});

function fetchResults(searchQuery, zipCode, startIndex) {
    $('html, body').scrollTop(0);
    const radius = $('#radius-input').val() * 1609.34;  // Convert miles to meters
    $.ajax({
        url: '/search',
        data: {
            query: searchQuery,
            zip: zipCode,
            start: startIndex,
            radius: radius,
        },
        method: 'GET',
        success: function (data) {
            displayResults(data.results, data.totalResults, startIndex, searchQuery, zipCode);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

function displayResults(results, totalResults, startIndex, searchQuery, zipCode) {
    const resultsDiv = $('#search-results');
    resultsDiv.empty();
    createCombinedMap(results);

    if (results.length === 0) {
        resultsDiv.append('<p>No results found.</p>');
        return;
    }

    const list = $('<ol></ol>');
    results.forEach(function (result, index) {
        const listItem = $('<li></li>');
        const title = $('<h4></h4>', {text: result.title});
        const mapsLink = $('<a></a>', {
            href: result.maps_link,
            text: 'View on Google Maps',
            target: '_blank',
        });
        const snippet = $('<p></p>', {text: result.snippet});

        listItem.append(title, mapsLink, snippet);

        if (result.lat && result.lng) {
            const mapImageUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${result.lat},${result.lng}&zoom=15&size=100x100&markers=color:red%7Clabel:${index + 1}%7C${result.lat},${result.lng}&key=AIzaSyBlz0-Xrd-UmDgkjHXFmVv_NAFBqTh11YU`;
            const mapThumbnail = $('<img>', {
                src: mapImageUrl,
                alt: result.title,
                width: 100,
                height: 100,
            });
            listItem.append(mapThumbnail);
        }
        list.append(listItem);
    });

    resultsDiv.append(list);

    const parsedTotalResults = parseInt(totalResults, 10);
    const numPages = Math.ceil(parsedTotalResults / 10);
    const currentPage = Math.ceil(startIndex / 10);

    if (numPages > 1) {
        const pagination = $('<div class="pagination"></div>');

        const maxVisiblePages = 10;
        const previousButton = $('<button class="btn btn-primary">&lt;</button>');
        previousButton.prop('disabled', currentPage === 1);
        previousButton.on('click', () => fetchResults(searchQuery, zipCode, (currentPage - 1) * 10));
        pagination.append(previousButton);

        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(numPages, startPage + maxVisiblePages - 1);

        if (endPage - startPage < maxVisiblePages - 1) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            const pageButton = $('<button class="btn btn-primary pagination-btn"></button>').text(i);
            pageButton.data('start', (i - 1) * 10);
            pageButton.toggleClass('active', i === (currentPage + 1));
            pageButton.on('click', function () {
                const startIndex = $(this).data('start');
                fetchResults(searchQuery, zipCode, startIndex);
            });
            pagination.append(pageButton);
        }

        const nextButton = $('<button class="btn btn-primary">&gt;</button>');
        nextButton.prop('disabled', currentPage === numPages);
        nextButton.on('click', () => fetchResults(searchQuery, zipCode, (currentPage + 1) * 10));
        pagination.append(nextButton);

        resultsDiv.append(pagination);
    }
}

function createCombinedMap(results) {
    const markers = results
        .map(
            (result, index) => `markers=color:red%7Clabel:${index + 1}%7C${result.lat},${result.lng}`
        )
        .join('&');

    const mapImageUrl = `https://maps.googleapis.com/maps/api/staticmap?size=600x400&${markers}&key=AIzaSyBlz0-Xrd-UmDgkjHXFmVv_NAFBqTh11YU`;

    const combinedMap = $('<img>', {
        src: mapImageUrl,
        alt: 'Combined Map',
        width: 600,
        height: 400,
    });

    $('#combined-map').empty().append(combinedMap);
}

function autoComplete(request, response) {
    $.ajax({
        url: '/search_suggestions',
        data: {
            query: request.term,
        },
        method: 'GET',
        success: function (data) {
            response(data.suggestions);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

// Autocomplete setup
$(function () {
    $('#search-input').autocomplete({
        source: autoComplete,
        minLength: 2,
        delay: 300,
    });
});
