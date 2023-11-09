const usernameInput = document.getElementById("signup-username");
const dupError = document.getElementById("dup-username");
const spinner = document.querySelector(".loading");

let timeout;
usernameInput.addEventListener("keyup", handleCheck);

function handleCheck() {
  clearTimeout(timeout);
  dupError.textContent = "";
  spinner.classList.add("hidden");
  if (usernameInput.value.length > 3) {
    spinner.classList.remove("hidden");
    timeout = setTimeout(() => {
      const URL = `/duplicate-user/${usernameInput.value}`;
      fetch(URL)
        .then((res) => res.json())
        .then((data) => {
          if (data === "true") {
            dupError.textContent = "Please choose different username";
          }
          spinner.classList.add("hidden");
        });
    }, 800);
  }
}
