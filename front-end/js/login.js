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

// Backend starter if not started yet
document.addEventListener('DOMContentLoaded', async () => {
    const loading = document.getElementById("loading")
    const main = document.getElementById("main")

    try {
        const response = await fetch ("https://notaki.onrender.com/starter")
        if (response.ok) {
            loading.classList.add("d-none");
            main.classList.remove("d-none");
        }
    } catch(error) {
        loading.innerHTML = `<h2 style="font-family: 'Audiowide', sans-serif;">Server Unavailable, Please Try Again Later.</h2>`;
    }
})