/* ========= BASIC SERVICE WORKER ========= */

self.addEventListener('install', event => {
  console.log('SW: Installed');
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  console.log('SW: Activated');
  event.waitUntil(self.clients.claim());
});

/* ========= OPTIONAL SAFE CACHE ========= */

const CACHE_NAME = 'fikrin-static-v1';

const STATIC_FILES = [
  '/static/css/bootstrap.min.css',
  '/static/css/index-styles_v1.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/img/fkrnlogo.png',
];

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(response => {
      return (
        response ||
        fetch(event.request).then(fetchResponse => {
          if (
            fetchResponse &&
            fetchResponse.status === 200 &&
            fetchResponse.type === 'basic'
          ) {
            const clone = fetchResponse.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, clone);
            });
          }
          return fetchResponse;
        })
      );
    })
  );
});

/* ========= FIREBASE BACKGROUND PUSH ========= */

importScripts('https://www.gstatic.com/firebasejs/10.8.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.8.1/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyDkyNO4aWT4qVCVJwkcb354_Rtc-TdFybk",
  authDomain: "fknpj-9c7bb.firebaseapp.com",
  projectId: "fknpj-9c7bb",
  messagingSenderId: "624374608791",
  appId: "1:624374608791:web:143bdac26d9762dcbb0ad2",
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(payload => {
  console.log('FCM Background Message:', payload);

  const title = payload.notification?.title || 'Fikrin';
  const options = {
    body: payload.notification?.body || 'New notification',
    icon: '/static/img/fkrnlogo.png',
  };

  self.registration.showNotification(title, options);
});
