//Profile Container
function toggleProfile() {
    document.getElementById('profile-container').classList.toggle('show');
}

//Confirmation
function confirmAndUpdate(player) {
    var userConfirmation = window.confirm('Are you sure you want to update ' + player + '?');
    
    if (!userConfirmation) {
        return false;
    }
    return validateForm();
}

//Client Side Validation
function validateForm() {
    var price = document.getElementById('price_input').value;

    try {
        validatePrice(price);
    } 
    catch (error) {
        alert(error.message);
        return false;
    }
    return true;
}

function validatePrice(price) {
    var price = parseInt(parseFloat(price));

    if (price <= 0) {
        throw new Error('Price must be greater than 0.');
    }
}