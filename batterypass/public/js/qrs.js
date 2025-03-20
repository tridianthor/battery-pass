document.addEventListener('DOMContentLoaded', function() {
    ///camera scan
    var isScanning = false;
    let stream = null; 
    const qrScanButton = document.getElementById('qr-scan-button');
    const cameraFeedDiv = document.getElementById('cameraFeed').querySelector('div');
    const qrPopup = document.getElementById('qrPopup');

    qrScanButton.addEventListener('click', function() {
        if (!isScanning) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function(videoStream) {
                    stream = videoStream;
                    const video = document.createElement('video');
                    video.srcObject = stream;
                    video.play();

                    cameraFeedDiv.innerHTML = '';
                    cameraFeedDiv.appendChild(video);

                    isScanning = true;
                    qrScanButton.textContent = "Stop scanning";

                    video.addEventListener('loadedmetadata', function() {
                        const canvas = document.createElement('canvas');
                        const context = canvas.getContext('2d');
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;

                        function scanQRCode() {
                            if (!isScanning) return;
                            context.drawImage(video, 0, 0, canvas.width, canvas.height);
                            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                            const code = jsQR(imageData.data, imageData.width, imageData.height);

                            if (code) {
                                window.location.href = code.data;
                                $(qrPopup).modal('hide'); //hide using jQuery
                                stopCamera();
                            } else {
                                requestAnimationFrame(scanQRCode);
                            }
                        }
                        requestAnimationFrame(scanQRCode);
                    });
                })
                .catch(function(error) {
                    handleCameraError(error);
                });
        } else {
            stopCamera();
        }
    });

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null; // Clear the stream
        }
        isScanning = false;
        qrScanButton.textContent = "Start scanning";
        cameraFeedDiv.innerHTML = '<div style="background-color: #495057; height: 200px; margin-bottom: 20px;"></div>'; //clear the video
    }

    function handleCameraError(error) {
        console.error("Camera error:", error);
        cameraFeedDiv.innerHTML = "<p>Camera access failed: " + error.message + "</p>";
        isScanning = false;
        qrScanButton.textContent = "Start scanning";
        fileUpload.click();
    }

    qrPopup.addEventListener('hidden.bs.modal', function() {
        stopCamera();
    });

    ///file upload

    const fileInputButton = document.getElementById('qr-image-upload-button');
    const fileInput = document.getElementById('qr-image-upload');

    fileInputButton.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);

                    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                    const code = jsQR(imageData.data, imageData.width, imageData.height);

                    if (code) {
                        window.location.href = code.data;
                    } else {
                        qrResultDiv.textContent = 'QR code not found.';
                    }
                };
                img.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    });
});