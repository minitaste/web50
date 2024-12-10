document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector("#compose-form").addEventListener("submit", (event) => {
    event.preventDefault(); // Для того, щоб форма не відправлялася стандартним способом
    send_email();
  });
  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 class="ml-3 my-2 text-3xl text-center">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
    .then((response) => {
      if (!response.ok) {
        console.log("Some Error in load_mailbox()")
      }
      return response.json()
        .then((emails) => {
          const emailsContainer = document.querySelector('#emails-view');
          if (emails.length === 0) {
            emailsContainer.innerHTML += `<p>No inbox emails.</p>`;
            return;
          }
          emails.forEach((email => {
            const emailItemDiv = document.createElement('div');
            emailItemDiv.className =
              "m-1 mb-3 p-2.5 border-silod border-2 border-sky-500 rounded-lg cursor-pointer";
            emailItemDiv.innerHTML = `
            <div class="flex justify-between mb-2">
              <p class="font-bold text-lg">Topic: ${email.subject}.</p>
              <p>From: <span class="underline underline-offset-2">${email.sender}</span></p>
            </div>
            <p>Sent at: ${email.timestamp}</p>
          `;
            emailItemDiv.addEventListener('click', () => load_email(email.id));
            emailsContainer.appendChild(emailItemDiv);
          }));
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
};


function load_email(email_id) {
  fetch(`emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      const emailsView = document.querySelector('#emails-view');
      emailsView.innerHTML = '';
      emailDiv = document.createElement('div');
      
      emailDiv.className = "mt-3 p-2";
      emailDiv.innerHTML = `
      <div class="flex justify-between mb-2">
        <p class="text-3xl">Topic: ${email.subject}.</p>
        <div>
          <p class="text-xs">Sent at: ${email.timestamp}.</p>
          <p class="text-xs">From: ${email.sender}.</p>
        
        </div>
      
      </div>
      <div>
        Email content:
        <p class="text-xl bg-slate-800 mt-1 p-2 rounded-lg">
          ${email.body}.
        </p>
      </div>
      `;

      const archiveButton = document.createElement("button");
      archiveButton.textContent = email.archived ? "Remove from archive" : "Add to archive";
      archiveButton.className = 'mt-1 hover:underline'

      archiveButton.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
        .then(() => load_mailbox('inbox'))
        
      });
      
      emailsView.appendChild(emailDiv);
      emailsView.appendChild(archiveButton);
    })
    .catch(error => {
      console.error("Error:", error);
    });
};


function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch(`/emails`, {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((result) => {
      console.log(result);

      if (result.error) {
        alert(`Error: ${result.error}`);
        console.log(result.error)
      } else {
        alert("Email sent successfully!");
        load_mailbox("sent");
      }
    });
}