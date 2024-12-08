/*
 * ログインのためのスクリプト
 *
*/
import {reqfunc} from "./script.js";

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const uploadButton = document.getElementById('upload');
const usernameInput = document.getElementById('username');

// カメラ映像を取得
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing webcam: ", err);
    });

// 写真を撮る
captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // アップロードボタンを有効化
    uploadButton.disabled = false;
});

// 写真をサーバーに送信
uploadButton.addEventListener('click', () => {
    let username = usernameInput.value;
    reqfunc(canvas, username, "login")
    .then(response => {
        if (response.ok) {
            alert("Image uploaded successfully!");
        } else {
            alert("Failed to upload image.");
        }
    })
    .catch(err => console.error("Error uploading image: ", err));
});

