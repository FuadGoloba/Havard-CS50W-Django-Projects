document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#post-content').disabled = true;

    document.querySelector('#postContent').onkeyup = () => {
        if (document.querySelector('#postContent').value.length > 0) {
            document.querySelector('#post-content').disabled = false;
        }
        else {
            document.querySelector('#post-content').disabled = true;
        }
    }
})