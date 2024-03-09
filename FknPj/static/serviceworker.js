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
