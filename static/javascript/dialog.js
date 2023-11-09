const dialog = document.querySelector("dialog");
const openDialog = document.querySelector("#open-dialog");
const cancelDialog = document.querySelector("#cancel");
const confirmDialog = document.querySelector("#confirm-delete");

openDialog.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.showModal();
});
cancelDialog.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.close();
});

confirmDialog.addEventListener("click", () => {
  fetch("/delete-user", {
    method: "POST",
  }).then(() => {
    // window.location.pathname("/")
    // window.location.assign("/")
    console.log("hello")
  });
});
