document.body.addEventListener("htmx:confirm", function(evt) {
    const { target } = evt;
    if (!target.hasAttribute("hx-confirm-swal")) {
        return;
    }

    evt.preventDefault();
    swal
        .fire({
            title: target.getAttribute("hx-confirm-swal"),
            icon: target.getAttribute("hx-confirm-swal-icon") || "question",
            showCancelButton: true,
            cancelButtonText: "Não",
            showConfirmButton: true,
            confirmButtonText: "Sim",
        })
        .then(({ isConfirmed }) => {
            if (isConfirmed) {
                evt.detail.issueRequest();
            }
        });
});

document.body.addEventListener("form:showMessage", function(evt) {
    swal.fire({
        title: evt.detail.message || evt.detail.value || "Salvo com sucesso!",
        icon: evt.detail.icon || "success",
        showConfirmButton: true,
        confirmButtonText: "Ok",
    });
});

document.body.addEventListener("form:showModal", function(evt) {
    const selector = evt.detail.value;
    const dialog = document.querySelector(selector);
    if (!dialog) return;

    dialog.showModal();
});

document.body.addEventListener("form:hideModal", function(evt) {
    const selector = evt.detail.value;
    const dialog = document.querySelector(selector);
    if (!dialog) return;

    dialog.close();
});
