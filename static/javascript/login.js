// Getting the dialog elements from the DOM
const loginBtn = document.getElementById("login-btn");
const loginDialog = document.getElementById("login-dialog");
const loginCancel = document.querySelectorAll(".cancel");
const tabs = document.querySelectorAll(".tab")
const forms = document.querySelectorAll(".form")
const signupUsername = document.getElementById("signup-username")

// Open the Dialog using a built-in method showModal()
loginBtn.addEventListener("click", () => loginDialog.showModal());

// Close the Dialog using a built-in method close()
loginCancel.forEach((btn) => {
  btn.addEventListener("click", () => loginDialog.close());
});

tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => {
    tabs.forEach(tab => tab.classList.remove("active-tab"))
    tab.classList.add("active-tab")
    forms.forEach(form => form.classList.remove("active-form"))
    
    forms[index].classList.add("active-form")
  })
})

async function fetchUsers() {
  response = await fetch("127.0.0.1/users")
  data = await response.json()
  console.log(data)
}


fetchUsers()
signupUsername.style.color = "red"