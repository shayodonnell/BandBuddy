document.addEventListener('DOMContentLoaded', function() {
   
    document.querySelectorAll('.like').forEach(function(button) {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('post-id');
            const likeCountSpan = this.parentElement.querySelector('.like-count');

            $.ajax({
                url: `/like/${postId}`,
                type: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                success: (data) => {
                    if(data.error) {
                        alert(data.error);
                    } else {
                        likeCountSpan.textContent = data.like_count;
                        if(data.liked) {
                            this.classList.add('bi-heart-fill');
                            this.classList.remove('bi-heart');
                        } else {
                            this.classList.add('bi-heart');
                            this.classList.remove('bi-heart-fill');
                        }
                    }
                },
                error: (xhr, status, error) => {
                    if(xhr.status === 403) {
                        alert('You must be logged in to like a post');
                    }
                }
            });
        });
    });

    document.querySelectorAll('.btn-regint').forEach(button => {
        console.log("hi");
        button.addEventListener('click', function() {
            console.log("hi");
            const adId = this.getAttribute('ad-id');
            $.ajax({
                url: `/band_ad/${adId}/register_interest`,
                type: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                },
                success: (data) => {
                    if(data.success) {
                        this.textContent = 'Interest Registered';
                        this.disabled = true;
                    } else if(data.error) {
                        alert(data.error);
                    } else {
                        alert('Something went wrong');
                    }
                },
                error: (error) => {
                    console.error('Error:', error);
                    alert('Something went wrong');
                }
            });
        });
    });
});