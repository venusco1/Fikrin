var CACHE_NAME = 'my-site-cache-v1';

var urlsToCache = [
  '/', '/static/css/bootstrap.min.css', '/static/css/comment-styles.css', '/static/css/index-styles.css', '/static/css/login-styles.css',  '/static/css/profile-styles.css',  '/static/css/styles.css',
  '/static/js/app.js','/static/js/bootstrap.bundle.min.js',  '/static/js/cropper.js',  '/static/js/index.js', '/static/js/ui.js',
]

self.addEventListener('install', function(event) { 
    event.waitUntil(
        caches.open(CACHE_NAME) .then(function(cache) {
            console.log('Opened cache'); 
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
        .then(function(result) { 
            return caches.open(CACHE_NAME)
            .then(function(c){
                c.put(event.request.url, result.clone());
                return result;
            })
        })

        .catch(function(e){
            return caches.match(event.request)
        })
    );
});


importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js") ;
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-analytics.js") ;
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js") ; 

const firebaseConfig = {
  apiKey: "AIzaSyDkyNO4aWT4qVCVJwkcb354_Rtc-TdFybk",
  authDomain: "fknpj-9c7bb.firebaseapp.com",
  projectId: "fknpj-9c7bb",
  storageBucket: "fknpj-9c7bb.appspot.com",
  messagingSenderId: "624374608791",
  appId: "1:624374608791:web:143bdac26d9762dcbb0ad2",
  measurementId: "G-93ZXLVMBCF"
};


firebase.initializeApp(firebaseConfig);   // Initialize Firebase
let messaging = firebase.messaging();   // Get Firebase Messaging instance

    messaging.setBackgroundMessageHandler(function (payload){
        let title = "from  Fikrin";
        let option = {
            body : 'YOu have a notification',
            icon : '/static/img/fikr.png'
        }

        self.ServiceWorkerRegistration.showNotifications(title, option)
    });


