document.addEventListener('DOMContentLoaded', function() {
   
    document.querySelectorAll('.like').forEach(function(button) {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('post-id');
            const likeCountSpan = this.parentElement.querySelector('.like-count');

            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })

            .then(response => response.json())
            .then(data => {
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
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    });

    document.querySelectorAll('.btn-regint').forEach(buttton => {
        console.log("hi");
        buttton.addEventListener('click', function() {
            console.log("hi");
            const adId = this.getAttribute('ad-id');
            fetch(`/band_ad/${adId}/register_interest`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    this.textContent = 'Interest Registered';
                    this.disabled = true;
                } else if(data.error) {
                    alert(data.error);
                } else {
                    alert('Something went wrong');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Something went wrong');
            });
        });
    });
});