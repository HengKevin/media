document.addEventListener("DOMContentLoaded", function() {
    let unfollow = document.querySelector('#unfollow')
    if (unfollow !== null){
        unfollow.onmouseover = function() {
            unfollow.value = "Unfollow"
            unfollow.className = "btn btn-outline-dark btn-sm btn-block"
        }
        unfollow.onmouseout = function() {
            unfollow.value = "Follow"
            unfollow.className = "btn btn-outline-primary btn-sm btn-block"
        }
        
    }
})