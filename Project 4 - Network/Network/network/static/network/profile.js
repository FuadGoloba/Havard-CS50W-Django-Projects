document.addEventListener('DOMContentLoaded', function () {

    var user_follows_profile_owner = getBool(document.querySelector('#user-follows-profile-owner').innerHTML);
    
    // Load follow/unfollw profile by default
    load_profile(user_follows_profile_owner)
   
    // Event Listener to follow or unfollow a profile
    document.querySelector('#follow-unfollow').addEventListener('click', () => {

        // Get profile selected and current condition if user follows profile
        let profile_owner = document.querySelector('#profile-owner').innerHTML.slice(1);
        let user_follows_profile_owner = getBool(document.querySelector('#user-follows-profile-owner').innerHTML);

        // Update User to follow or unfollow profile
        fetch(`/profile/${profile_owner}`, {
            method: 'PUT',
            body: JSON.stringify({
                user_wants_to_follow_profile_owner: user_follows_profile_owner
            })
        })
        .then(response => {
            
            // Update profile's follower count
            if (user_follows_profile_owner === true) {
                document.querySelector('#follower-count').innerHTML = parseInt(document.querySelector('#follower-count').innerHTML) + 1
            }
            else {
                document.querySelector('#follower-count').innerHTML = parseInt(document.querySelector('#follower-count').innerHTML) - 1 
            }
            load_profile(user_follows_profile_owner);
        })

    })

});

// Function to convert string to boolean 
function getBool(val) {
    return !!JSON.parse(String(val).toLowerCase());
}

// load profile
function load_profile(user_follows_profile_owner) {
    // Don't display any buttons on loading the profile
    document.querySelector('#toggle-follow-view').style.display = 'none';

    let profile_owner = document.querySelector('#profile-owner').innerHTML.slice(1);
    let request_user = document.querySelector('#user').innerHTML;

    // Display Follow/Unfollow button by checking if user follows profile
    if (request_user ) {
        document.querySelector('#toggle-follow-view').style.display = 'block';

        // If user doesn't follow profile, display Follow button
        if (request_user != profile_owner && user_follows_profile_owner === false) {
            document.querySelector('#follow-unfollow').innerHTML = 'Follow';
            document.querySelector('#user-follows-profile-owner').innerHTML = true
        }
        // If user follows profile, display unfollow button
        else if (request_user != profile_owner && user_follows_profile_owner === true) {
            document.querySelector('#follow-unfollow').innerHTML = 'Unfollow';
            document.querySelector('#user-follows-profile-owner').innerHTML = false
        }
        // If it's user's profile, don't display any buttons
        else {
            document.querySelector('#toggle-follow-view').style.display = 'none'
        }
    }
}