document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit').forEach(edit_button => editPost(edit_button));
    document.querySelectorAll('.like').forEach(like_button => like_unlike_post(like_button))


});

// Function to Edit post content and submit
function editPost(edit_button) {
    edit_button.onclick = () => {
        // Do not display the edit button after being clicked
        edit_button.style.display = 'none'

        // Get content of the post
        let content = document.querySelector(`#contentPost${edit_button.dataset.postid}`)
        // Edit content using a form
        content.innerHTML = 
                            `<form id="post-edit-form" class="card-text" style="margin-top: 1rem; margin-bottom: 1.6rem">
                            <div class="form-group" style="margin-bottom: .7rem">
                                <textarea 
                                    style="overflow: hidden; resize: none"
                                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                                    class="form-control"
                                    id="post-edit-textarea">${content.innerHTML}</textarea>
                            </div>
                            <input type="submit" id="save-post" class="btn btn-primary post-submit" value="Save"/>
                        </form>`

        // By default submit button is disabled
        document.querySelector('#save-post').disabled = true;
        // On editing the form, enable the submit button else disable if user doesn't type at least a letter
        document.querySelector('#post-edit-textarea').onkeyup = () => {
            if  (document.querySelector('#post-edit-textarea').value.length > 0) {
                document.querySelector('#save-post').disabled = false;
            }
            else {
                document.querySelector('#save-post').disabled = true;
            }
        }
        
        // Submit the edited content
        document.querySelector('#post-edit-form').onsubmit = () => {
            fetch('/editpost', {
                method: 'PUT',
                body: JSON.stringify({
                    content: document.querySelector('#post-edit-textarea').value,
                    post_id: edit_button.dataset.postid
                })
            })
            .then(response => response.json())
            .then(res => {
                if (res.error) {
                    console.log(`Error editing post: ${res.error}`);
                }
                else {
                    console.log(res.message)
                    content.innerHTML = document.querySelector('#post-edit-textarea').value
                    edit_button.style.display = 'block'
                }
            })
            .catch(err => {
                console.log(err)
            })
            return false;
        }
    }
}

// Function to Like and Unlike post
function like_unlike_post(like_button) {
    like_button.onclick = () => {
        // Update the post like count and return the count to display on the page
        fetch('/likepost', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: like_button.dataset.postid
            })
        })
        .then(response => response.json())
        .then(res => {

            if (res.error) {
                console.log(`Error liking/unliking post: ${res.error}`)
            }
            else {
                // Update the like/unlike toggle button
                if (res.message === 'Like successful') {
                    like_button.innerHTML = "<div style='color: rgb(32, 120, 244);'><i class='mr-2 fas fa-thumbs-down'></i>Unlike</div>"
                }
                else if (res.message === 'Unlike successful') {
                    like_button.innerHTML = "<i class='mr-2 far fa-thumbs-up'></i>Like"
                }
                // Update like count on the page
                document.querySelector(`#likes${like_button.dataset.postid}`).innerHTML = res.like_count
            }
        })
    }
}