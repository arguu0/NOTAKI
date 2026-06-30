const apiurl = "http://127.0.0.1:8000/notes";

//get input, add note and save in fastapi and display in frontend
async function get_input() {
    const inputField = document.getElementById('note-input');
    const Inputvalue = inputField.value.trim();
    
    try {
        const response = await fetch(apiurl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ note: Inputvalue })
        })
        if (!response.ok) {
            const err = await response.json();
            console.log(err.detail[0].msg);
            alert(err.detail[0].msg)
        }
        inputField.value = '';
        await fetch_url()
        
    } catch (error) {
        console.error(error);
        alert("Could not reach server.");
    }
};
document.getElementById('save-btn').addEventListener('click', get_input);

//fetch note
async function fetch_url() {
    const response = await fetch(apiurl);
    const data = await response.json();
    
    let innertext = data.length > 1 ? `${data.length} Notes` : `${data.length} Note`;  //display the number of notes

    document.getElementById('note-count').innerText = innertext;
    show_note(data);  // call display note
}

//display note
function show_note(notes) {
    const counter = document.getElementById('counter');
    counter.textContent = '0';

    const container = document.getElementById('note-card-reuse');
    container.innerHTML = notes.map((item, index) => `
    <div class="note-card">
        <div class="note-card-header">
            <span class="note-id">NOTE #${index + 1}</span> <!--note id here-->
            <span class="note-time">${item.time.slice(4,10)} , ${item.time.slice(11,16)}</span>
        </div>
        <div id="edit_container_${item.id}">
        <p class="note-body" id="static-text_${item.id}">${item.note}</p>  <!-- Note goes here -->
        
        <div class="note-actions">
            <button class="btn-edit" onclick='edit_to_save(${item.id})'>Edit</button>
            <button class="btn-delete" data-id="${item.id}">Delete</button>
        </div>
        </div>
    </div>`).join('');
}

//display all note after reload / at start
window.addEventListener('DOMContentLoaded', () => {
    fetch_url();
});

//delete notes
async function delete_item(event) {
    if (event.target.classList.contains('btn-delete')) { 
        const payload = event.target.dataset.id;
        await fetch(`${apiurl}/${payload}`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id : payload})
        })
        await fetch_url();
    }
};
document.addEventListener('click', delete_item)


//edit note -- change edit btn to "save"
async function edit_to_save(id) {
    const container = document.getElementById(`static-text_${id}`);
    const exist_text = container.innerHTML;
    const word = exist_text.split(/\s+/);  // for word.length -> display word count

    document.getElementById(`edit_container_${id}`).innerHTML =  `
        <textarea id="note-input_${id}" class="note-input1" style="resize: none;">${exist_text}</textarea>
        <div class="word-count"> 
            <span class="counter" id="counter_${id}">${word.length}</span>/100 Words
        </div><br>
        <div class="note-actions">
            <button class="btn-edit" onclick="save_change(${id})">Save</button>
        </div>`;
    attach_word_counter(`note-input_${id}`, `counter_${id}`);
};

//save the note
async function save_change(id) {
    const updatedText = document.getElementById(`note-input_${id}`).value.trim();
    
    try {
        const response = await fetch(`${apiurl}/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id: id ,note : updatedText })
        })

        if (!response.ok) {
            const err = await response.json();
            console.log(err.detail[0].msg);
            alert(err.detail[0].msg)
        }
        await fetch_url();
    } catch (error){
        console.error(error);
        alert("Could not reach server.");
    }
};

// word counter
attach_word_counter('note-input', 'counter');
function attach_word_counter(inputId, counterId) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);

    input.addEventListener('input', (event) => {
        const text = event.target.value.trim();

        if (text === '') {
            counter.textContent = '0';
            return;
        }

        const words = text.split(/\s+/);
        counter.textContent = `${words.length}`;
        counter.style.color = words.length >= 101 ? 'red' : '';
    });

    input.addEventListener("keydown", (event) => {
        const text = input.value.trim();
        const words = text === "" ? [] : text.split(/\s+/);

        if (event.key === 'Backspace' || event.key === "Delete" || event.key === 'ArrowLeft' || event.key === 'ArrowUp' ||
            event.key === 'ArrowDown' || event.key === 'Tab') {
            return;
        }
        if (words.length >= 100) {
            event.preventDefault();
        }
    });
}