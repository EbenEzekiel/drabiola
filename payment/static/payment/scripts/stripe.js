const submit = document.getElementById('submit');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = cookie.substring(name.length + 1);
                break;
            }
        }
    }
    return cookieValue;
}

function validate(){
    let inputs = ['name', 'address', 'email', 'organization', 'selected-package'];
    let returnValue = 1;
    inputs.forEach(name => {
        let ele= document.getElementById(name);
        if(ele.value == ""){
            returnValue = 0
        }
    })
    return returnValue
    
}

submit.addEventListener('click', (e)=> {
    e.preventDefault();
    const form = document.getElementById('form');
    let formData = new FormData(form);
    
    let package = new FormData();
    package.append("package", formData["selected-package"]);
    // let val = 
    if(validate() == 1){
        fetch("/create_checkout_session", {
            method:"POST",
            body: formData
        }
        )
            .then(response => response.json())
            .then(session=> stripe.redirectToCheckout({sessionId: session.id}))
            .catch(error => {
                alert("Error encountered: Confirm you have a stable internet connection");
            })
    }
    else{
        alert('Kindly give appropriate answers.\nAll fields marked "*" are important');
    }
})


// fetch('/registration', {
//             method: "POST",
//             headers: {"X-CSRFToken": getCookie('csrftoken')},
//             body: formData
//             })
//         .then(
//         )
//         .catch(error => {
//             alert("Development Error");
//             console.log("Development Error: ", error);
//         })
    