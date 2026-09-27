function showToast(message, type = "info") {
    const toast = document.getElementById("toast");

    if (!toast) {
        return;
    }

    toast.textContent = message;
    toast.className = "toast show";

    if (type === "error") {
        toast.style.background = "#b91c1c";
    } else if (type === "success") {
        toast.style.background = "#15803d";
    } else {
        toast.style.background = "#172033";
    }

    setTimeout(() => {
        toast.className = "toast";
    }, 3500);
}


function statusClass(status) {
    return "status-" + String(status)
        .toLowerCase()
        .replaceAll(" ", "-");
}


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


async function logout() {
    try {
        await fetch("/api/auth/logout", {
            method: "POST"
        });
    } finally {
        window.location.href = "/login";
    }
}
