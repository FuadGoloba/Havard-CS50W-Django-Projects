document.addEventListener('DOMContentLoaded', function() {


  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Submit an email
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

// ------------------------------------------------ Utility functions to use in loading DOM content -------------------------------------//

// Function to send mail 
function send_email(event) {

  event.preventDefault()

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => load_mailbox('sent'));
}

// Function to compose email
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none'
  //document.querySelector('#send-mail').disabled = true;

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

// Function to reply email
function reply_email(email_id) {

  // Get the email object to reply
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Load the compose email view
    compose_email();
    
    // Populate email to reply
    document.querySelector('#compose-recipients').value = email.sender;
    if ("Re:" === email.subject.slice(0,3)) {
      document.querySelector('#compose-subject').value = email.subject;
      
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  })

}

// Function to render a mail item in a div or box
function render_mail(email) {

  const current_user = document.querySelector('#user').innerHTML

  // display each email in a main div
  const mail = document.createElement('div');
  // Create an array of email attributes
  const email_attributes = [email.sender != current_user ? email.sender:email.recipients, email.subject, email.timestamp]; 
  const email_attributes_length = email_attributes.length; // get the length of array
  mail.className = `email-items`; // className for the main div
  var arrayDiv = new Array();

  // Traverse the email attributes array to create an inner div for each individual attribute and append to main div
  for (var i = 0; i < email_attributes_length; i++) {
    arrayDiv[i] = document.createElement('div');
    arrayDiv[i].className = 'email-attributes';
    arrayDiv[i].innerHTML = `${email_attributes[i]}`;
    mail.id =  `${email.id}`
    mail.appendChild(arrayDiv[i]);
  }

  // Change background color to reflect read or unread emails
  if (email.read === false) {
    mail.style.backgroundColor = 'white';
  }
  else {
    mail.style.backgroundColor = 'gray';
  }

  return mail;

}


// Function to load inidividual mail content
function load_content(email_id) {

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    
    // Hide other views except the content view
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'block';

    // Display email
    const view = document.querySelector('#email-content-view');
    view.innerHTML = `
      <ul class="email-details">
        <li class="email-details"><b>From:</b> <span>${email.sender}</span></li>
        <li class="email-details"><b>To: </b><span>${email.recipients}</span></li>
        <li class="email-details"><b>Subject:</b> <span>${email.subject}</span</li>
        <li class="email-details"><b>Time:</b> <span>${email.timestamp}</span></li>
      </ul>
        <hr>
        <p class="m-2">${email.body}</p>
    `
    // Create Reply button with Listener to reply email
    const reply_button = document.createElement('button');
    reply_button.className = "btn btn-sm btn-outline-primary";
    reply_button.id = "mail-reply";
    reply_button.innerHTML = "Reply";
    view.appendChild(reply_button);
    reply_button.addEventListener('click', function() {
      reply_email(email_id);
    })
    

    // Create Archive/Unarchive Button
    archive_button = document.createElement('button');
    archive_button.className = "btn btn-sm btn-outline-primary";
    archive_button.id = "mail-archive";

    const current_user = document.querySelector('#user').innerHTML;
    // Only Show Archive buttons for inbox mails and 
    if (email.archived === false && email.sender != current_user) {
      archive_button.innerHTML = "Archive";
      view.appendChild(archive_button);

    }
    // Only show UnArchive button for Archived mails
    else if (email.archived === true && email.sender != current_user) {
      // To un-archive an archived mail
      archive_button.innerHTML = "Un-Archive";
      view.appendChild(archive_button);
    }
    // Event Listener to archive/unarchive email
    archive_button.addEventListener('click', function () {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(response => load_mailbox('inbox'));
    })
    
  })
}



// Function to load mailbox; inbox, sent, archive
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none'

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //mail_view = document.querySelector('#emails-view');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Generate div for each email and append 
    emails.forEach(function(email) {
      // Call function to generate each div
      var item = render_mail(email);
      // Listener to load content of each div on clicking the div
      item.addEventListener('click', function() {
      // load content of clicked email
      load_content(email.id);
      // mark email as read
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })

      });
      // Append all mails loaded 
      document.querySelector('#emails-view').append(item);
    });

})

}

