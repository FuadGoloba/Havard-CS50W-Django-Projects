document.addEventListener('DOMContentLoaded', function () {
    let pathName = window.location.pathname // Get the current url of the window
    let allPosts = document.querySelector('#all-posts')
    let topTitle = document.querySelector('#top-title')
    let bodyDiv = document.querySelector(".body")
    let topNav = document.querySelector('.top-nav')
    let following = document.querySelector('#following')
    let profile = document.querySelector('#profile')
    let profile_owner_post_count = document.querySelector('#profile-owner-post-count').innerHTML
    let profile_owner = document.querySelector('#profile-owner-names').innerHTML


    if (pathName === '/') {
        allPosts.classList.add("display")
        topTitle.innerHTML = "All Posts"
    }
    else {
        allPosts.classList.remove("display")
    }

    if (pathName === '/login' || pathName === '/register') {
        bodyDiv.style.backgroundColor = "white"
        topNav.style.borderbottom = 'none'
    }
    else {
        bodyDiv.style.backgroundColor = '#F0F2F5'
        topNav.style.borederbottom = "1px solid #e2e2e2"
    }
    
    if (pathName.startsWith("/profile/")) {
        if (pathName === "/profile/{{ request.user.username }}") {
            profile.classList.add("display")
        }
        profile.innerHTML = `<i class="mr-4 fas fa-user"></i>Profile`
        topTitle.innerHTML = `<span style="margin: 0">${profile_owner}</span><br><span class="text-muted" style="font-size: 13px; font-weight: normal">${profile_owner_post_count} Tweets</span>`
        topTitle.style.lineHeight = "18px";
        topTitle.style.padding = "0";

    } else {
        profile.classList.remove("display")
        profile.innerHTML = `<i class="mr-4 far fa-user"></i>Profile`
    }

    if (pathName === '/following') {
        following.classList.add('display')
        topTitle.innerHTML = "Following"
    }
    else {
        following.classList.remove('display')
    }
    
})