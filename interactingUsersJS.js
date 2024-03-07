document.addEventListener('DOMContentLoaded', function() {
    const users = [
        { id: 1, username: "user1"},
        { id: 2, username: "user2"},
        { id: 3, username: "user3"},
        { id: 4, username: "user4"},
        // Add more users as needed
    ];

    const tableBody = document.getElementById('usersTable').getElementsByTagName('tbody')[0];

    users.forEach(user => {
        let row = tableBody.insertRow();

        let cellId = row.insertCell(0);
        cellId.textContent = user.id;

        let cellUsername = row.insertCell(1);
        cellUsername.textContent = user.username;

        let cellActions = row.insertCell(2);
        cellActions.className = 'actions-cell'
        // Create Edit button
        let editBtn = document.createElement('button');
        editBtn.textContent = 'Edit';
        editBtn.classList.add('edit-btn'); // For styling and identification
        editBtn.onclick = function() {
            editUser(user.id); // Placeholder for an edit function
        };

        // Create Block button
        let blockBtn = document.createElement('button');
        blockBtn.textContent = 'Block';
        blockBtn.classList.add('block-btn'); // For styling and identification
        blockBtn.onclick = function() {
            blockUser(user.id); // Placeholder for a delete function
        };

        // Create Delete button
        let deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.classList.add('delete-btn'); // For styling and identification
        deleteBtn.onclick = function() {
            deleteUser(user.id); // Placeholder for a delete function
        };

        // Append buttons to the actions cell
        let actionsWrap = document.createElement('div');
        actionsWrap.classList.add('actions-cell')
        actionsWrap.appendChild(editBtn);
        actionsWrap.appendChild(blockBtn);
        actionsWrap.appendChild(deleteBtn);
        cellActions.appendChild(actionsWrap)
    });
});

// Placeholder functions for Edit and Delete actions
function editUser(userId) {
    console.log('Editing user', userId);
    // Implement your edit logic here
}

function deleteUser(userId) {
    console.log('Deleting user', userId);
    // Implement your delete logic here
}


function blockUser(userId) {
    console.log('Block user', userId);
    // Implement your delete logic here
}

document.addEventListener('DOMContentLoaded', function() {
    const usernameSearch = document.getElementById('usernameSearch');
    usernameSearch.addEventListener('input', function() {
        const searchValue = usernameSearch.value.toLowerCase();
        const userRows = document.getElementById('usersTable').getElementsByTagName('tbody')[0].rows;

        for (let i = 0; i < userRows.length; i++) {
            let usernameCell = userRows[i].getElementsByTagName('td')[1]; // Assumes username is in the second column
            if (usernameCell) {
                let username = usernameCell.textContent || usernameCell.innerText;
                if (username.toLowerCase().indexOf(searchValue) > -1) {
                    userRows[i].style.display = ""; // Show row
                } else {
                    userRows[i].style.display = "none"; // Hide row
                }
            }
        }
    });
});