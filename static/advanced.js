document.addEventListener("DOMContentLoaded", function () {

    const loadButton =
        document.getElementById("loadRepository");

    const repositoryInput =
        document.getElementById("repositoryUrl");

    const status =
        document.getElementById("repositoryStatus");


    loadButton.addEventListener("click", function () {

        const url =
            repositoryInput.value.trim();


        if (!url) {

            status.innerText =
                "Please enter a GitHub repository URL.";

            return;
        }


        if (!url.includes("github.com")) {

            status.innerText =
                "Please enter a valid GitHub repository URL.";

            return;
        }


        status.innerText =
            "Repository loaded successfully: " + url;

    });

});