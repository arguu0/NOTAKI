document.getElementById('login-btn').addEventListener('click', async (event) => {
    event.preventDefault();

    const msg = document.getElementById('login-msg');
    const email = document.getElementById('login-email').value.trim();
    const pwd = document.getElementById('login-password').value.trim();

    if (email == "" || pwd == ""){
        msg.innerHTML = "Please fill in both fields."
        msg.style.display = "block";
    }
    else {
        const response = await fetch(`https://notaki.onrender.com/login`, {
            method: "POST",
            headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
            body: `username=${email}&password=${pwd}`  // using query structure since 0auth2reqform receive like this
        })
        const data = await response.json();
        if (!response.ok) {
            msg.innerHTML = data.detail;
            msg.style.display = "block";
        } else {
            msg.style.display = "none";
            localStorage.setItem('token', data.access_token);   // save token value in browser localstorage
            access_dashboard();
        }
    }
})

function access_dashboard() {
    window.location.href = "dashboard.html";
}