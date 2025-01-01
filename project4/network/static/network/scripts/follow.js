document.addEventListener("DOMContentLoaded", function () {
    const followButton = document.querySelector("#follow");

    if (followButton) {
        followButton.addEventListener("click", function () {
            const username = followButton.getAttribute("data-username");

            fetch(`/follow/${username}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        followButton.textContent = data.is_following ? "Unfollow" : "Follow";

                        const followersCount = document.querySelector("#followers-count");
                        if (followersCount) {
                            followersCount.textContent = data.followers_count;
                        }
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
