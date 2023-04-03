function initSlideshow(imagePath) {
    const images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg'];
    images.sort(() => Math.random() - 0.5);
    const slideshow = document.querySelector(".slideshow");

    images.forEach((image, index) => {
        const img = document.createElement("img");
        img.src = imagePath + image;
        img.style.opacity = index === 0 ? 1 : 0;
        slideshow.appendChild(img);
    });

    let currentImage = 0;
    setInterval(() => {
        images.forEach((image, index) => {
            slideshow.children[index].style.opacity = index === currentImage ? 1 : 0;
        });
        currentImage = (currentImage + 1) % images.length;
    }, 7500);
}