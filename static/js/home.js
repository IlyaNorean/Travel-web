$(document).ready(function () {
    $('#query').on('input', function () {
        var query = $(this).val().toLowerCase();
        $.ajax({
            type: 'POST',
            url: '/search',
            data: { query: query },
            success: function (data) {
                var resultsHtml = '';
                if (data.length > 0) {
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].type === 'attraction') {
                            resultsHtml += '<a class="list-group-item list-group-item-action attractionResult" data-city="' + data[i].city + '" data-attraction="' + data[i].attraction + '">' +
                                data[i].attraction + ' в городе ' + data[i].city + '</a>';
                        }
                    }
                } else {
                    resultsHtml += '<a class="list-group-item list-group-item-action disabled">Ничего не найдено.</a>';
                }
                $('#searchResults').html(resultsHtml).show();
            }
        });
    });

    $('#searchForm').submit(function (e) {
        e.preventDefault();
    });

    $('#searchResults').on('click', '.attractionResult', function () {
        var city = $(this).data('city');
        var attraction = $(this).data('attraction');
        window.location.href = '/attraction/' + city + '/' + attraction;
    });

    // Закрытие результатов поиска при клике за пределами формы
    $(document).on('click', function (e) {
        if ($(e.target).closest("#searchResults, #query").length === 0) {
            $('#searchResults').hide();
        }
    });
});