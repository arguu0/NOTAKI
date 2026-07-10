document.getElementById('register-btn').addEventListener('click', async (event) => {
    event.preventDefault();    
    
    const pwd = document.getElementById('signup-password').value;
    const confirm_pwd = document.getElementById('signup-confirm-password').value;
    const msg = document.getElementById('signup-msg'); 

    if (pwd !== confirm_pwd) {
        msg.style.display = "block";
        msg.innerHTML = "Passwords do not match. Please try again."
    } else {
        await register(msg);
    }
})

async function register(msg) {
    const form = new FormData(document.getElementById('form_id'));
    const formdata = Object.fromEntries(form);

    const response = await fetch(`https://notaki.onrender.com/register`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(formdata)
    })
    const data = await response.json();
    if (!response.ok) {
        msg.style.display = "block";
        msg.innerHTML = data.detail;
    } else {
        msg.innerHTML = data;
        msg.style.color = "#84e27a";
        msg.style.background = "rgba(122, 226, 122, 0.1)";
        msg.style.border = "1px solid rgba(122, 226, 122, 0.3)";
        msg.style.display = "block";
        setTimeout(() => {
            msg.style.color = "#e27a7a";
            msg.style.background = "rgba(226, 122, 122, 0.1)";
            msg.style.border = "1px solid rgba(226, 122, 122, 0.3)";
            msg.style.display = "none";
        }, 3000);
    }
}


document.addEventListener('DOMContentLoaded', async () => {
    const loading = document.getElementById("loading")
    const main = document.getElementById("main")

    try {
        const response = await fetch ("https://notaki.onrender.com/starter")
        if (response.ok) {
            loading.style.display = "none";
            main.style.display = "block";
        }
    } catch(error) {
        loading.innerHTML = `<h2 style="font-family: 'Audiowide', sans-serif;">Server Unavailable, Please Try Again Later.</h2>`;
    }
})