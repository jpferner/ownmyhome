/**
 * Initialize a slideshow with randomized images.
 * @param {string} imagePath - The path to the images folder.
 */
function initSlideshow(imagePath) {
    // List of image file names
    const images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg'];
    // Randomize the order of the images
    images.sort(() => Math.random() - 0.5);
    // Get the slideshow container element
    const slideshow = document.querySelector(".slideshow");
    // Iterate over the images and add them to the slideshow container
    images.forEach((image, index) => {
        const img = document.createElement("img");
        img.src = imagePath + image;
        img.style.opacity = index === 0 ? 1 : 0;
        slideshow.appendChild(img);
    });
    // Initialize the current image index
    let currentImage = 0;
    // Set an interval to change the displayed image
    setInterval(() => {
        // Update the opacity of each image based on the current image index
        images.forEach((image, index) => {
            slideshow.children[index].style.opacity = index === currentImage ? 1 : 0;
        });
        // Move to the next image, wrapping around if necessary
        currentImage = (currentImage + 1) % images.length;
    }, 7500);
}
