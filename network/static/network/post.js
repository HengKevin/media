document.addEventListener("DOMContentLoaded", function() {

    document.querySelectorAll('.edit').forEach(btn => {
        btn.onclick = function () {
            btn.style.diplay = 'none';
            console.log(btn.dataset.postid);
            let EditcontentDiv = document.querySelector(`#content${btn.dataset.postid}`);
            EditcontentDiv.innerHTML=
            `<form id="edit-post">
                <textarea type="text" id="edit-content" class="form-control">${EditcontentDiv.innerHTML}</textarea>
                <input type="submit" class="btn btn-primary post-submit" value="Save"/>
            </form> `;
        
    document.querySelector('#edit-save').onsubmit = function () {
        const newContent = document.querySelector('#edit-content').value;
        const post_id = btn.dataset.postid

        fetch('/postedit', {
            method: 'PUT',
            body: JSON.stringify({
                content: newContent,
                post_id: post_id
            })
            .then(response => response.json())
            .then(result => {
                if(result.error){
                    console.log(`Error: editing${result.error}`);
                }else {
                    console.log("Edit sucess");
                    EditcontentDiv.innerHTML = content;
                    btn.style.diplay = 'block';
                    }
                })
            })
            .catch(err=>{
                console.log(err);
            })
        return false;
        }
    }
})


    document.querySelector('.like').forEach(btn => {
        btn.onclick = function() {
            fetch('/postedit', {
                method: 'PUT',
                body: JSON.stringify({
                    liked: true,
                    post_id: btn.dataset.postid
                })
                .then(response => response.json())
                .then(result => {
                    if(result.error){
                        console.log(`Liked error: ${result.error}`)
                    } else {
                        console.log('likes changed')
                        let likes_count = document.querySelector(`#likes${btn.dataset.postid}`)
                        if (parseInt(result.likes_num) < parseInt(likes_count.innerHTML)) {
                            btn.innerHTML = "<i class='mr-2 far fa-thumbs-up'></i>Like"
                        } else if (parseInt(result.likes_num) > parseInt(likes_count.innerHTML)) {
                            btn.innerHTML = "<div style='color: rgb(32, 120, 244);'><i class='mr-2 fas fa-thumbs-up'></i>Unlike</div>"
                        }
                        document.querySelector(`#likes${btn.dataset.postid}`).innerHTML = result.likes_num
                    }
                })
            })
        }
    })
});