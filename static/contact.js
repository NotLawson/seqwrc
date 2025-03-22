const query = new URLSearchParams(window.location.search);
const subject = query.get('subject');
const message = query.get('message');
if (subject) {
  document.getElementById('subject').value = subject;
}
if (message) {
  document.getElementById('message').value = message;
}