$(document).ready(function() {
    $('.create-btn').off('click').click(function(event) {
        event.preventDefault(); // Prevent the default link behavior
        event.stopPropagation();
        var fieldName = $(this).closest('.input-group').find('select').attr('id').replace('id_', '');

        var editUrl = '/' + fieldName + '/form/'; // Construct the URL
        window.open(editUrl, 'width=800,height=600'); // Redirect to the URL
    });

    $('.edit-btn').off('click').click(function(event) {
        event.preventDefault(); // Prevent the default link behavior
        event.stopPropagation();
        var fieldName = $(this).closest('.input-group').find('select').attr('id').replace('id_', ''); // Get the field name
        var selectedId = $(this).closest('.input-group').find('select').val(); // Get the selected value

        if (selectedId) {
            var editUrl = '/' + fieldName + '/form/' + selectedId; // Construct the URL
            window.open(editUrl, 'width=800,height=600'); // Redirect to the URL
        } else {
            alert('Please select an item to edit.');
        }
    });
});