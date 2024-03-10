// serviceworker.js
const cacheName = 'your-app-cache';

const filesToCache = [
    '/',  // Add all your static files here 
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(cacheName)
            .then((cache) => {
                return cache.addAll(filesToCache);
            })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Cache hit - return response
                if (response) {
                    return response;
                }

                // Clone the request
                let fetchRequest = event.request.clone();

                return fetch(fetchRequest)
                    .then((response) => {
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clone the response
                        let responseToCache = response.clone();

                        caches.open(cacheName)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });

                        return response;
                    });
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
