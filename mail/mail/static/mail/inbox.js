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
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
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
            emailItemDiv.className = "email-item";
            emailItemDiv.innerHTML = `
            <p>From: ${email.sender}</p>
            Topic: ${email.subject},
            Sent at: ${email.timestamp}
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
      
      emailDiv.className = "email";
      emailDiv.innerHTML = `
      <p>From: ${email.sender}.</p>
      <p>Send to: ${email.recipients}.</p>
      <p>Subject: ${email.subject}.</p>
      Text: ${email.body}.
      <p>Sent at: ${email.timestamp}.</p>
      `;

      const archiveButton = document.createElement("button");
      archiveButton.textContent = email.archived ? "Remove from archive" : "Add to archive";

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