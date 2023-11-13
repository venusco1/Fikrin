"use strict";
console.clear();

function fetch()
{
   var arr = [],
       i = 0,
       l = 6;
   
   for(; i < l; i++)
   {
      arr.push({
         "quote": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis.",
         "name": "Studio KonKon",
         "info": "Administrator, DRPDM",
         "image": "https://s.cdpn.io/profiles/user/2598789/512.jpg"
      });
   }
   
   return arr;
}

var app = {};

app = new Vue({
   el: "#app",
   data: {
      items: fetch()
   },
   components: {
      "skk-card-item": {
         "props": {
            "quote": { type: String },
            "name": { type: String },
            "info": { type: String },
            "image": { type: String, default: "https://s.cdpn.io/profiles/user/2598789/512.jpg" }
         },
         template: "#card"
      }
   }
});