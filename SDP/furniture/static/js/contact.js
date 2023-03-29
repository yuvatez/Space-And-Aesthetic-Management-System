function send () {
  document.getElementById("contactGo").disabled = true;
  let data = new FormData(document.getElementById("contactForm"));
  fetch("/book", { method:"POST", body:data })
  .then(res => {
    if (res.status==200) { location.href = "/thank"; }
    else {
      console.log(res);
      alert("Opps an error has occured.");
    }
  })
  .catch(err => {
    console.error(err);
    alert("Opps an error has occured.");
  });
  return false;
}