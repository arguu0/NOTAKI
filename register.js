document.getElementById('register-btn').addEventListener('click', async (event) => {
    event.preventDefault();    

    const pwd = document.getElementById('signup-password').value;
    const confirm_pwd = document.getElementById('signup-confirm-password').value;
    

    if (pwd !== confirm_pwd) {
        const error = document.getElementById('signup-error');
        error.style.display = "block";
        error.innerHTML = "Passwords do not match. Please try again."
        setTimeout(() => {
            error.style.display = "None";
            error.innerHTML = ""
        }, 3000);
    } else {
        await register(event)
    }
})

async function register(event) {
    event.preventDefault();

    const form = new FormData(form_id)
    const formdata = Object.fromEntries(form);
    console.log(formdata)

    const response = await fetch(`http://127.0.0.1:8000/register`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(formdata)
    })
    if (!response.ok) {
        const data = await response.json()
        alert(data.detail)
    } else {
        alert("Account Created")
    }
}
