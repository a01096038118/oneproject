function copyKey() {
    const admin_key = document.getElementById("admin_key");

    adminKey.select();
    adminKey.setSelectionRange(0, 9999);

    navigator.clipboard.writeText(adminkey.value);
    alert("KEY NUMBER COPY SUCCESS!!")
}